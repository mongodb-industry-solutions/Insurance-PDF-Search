from abc import ABC, abstractmethod
from typing import Dict
import json
import os.path as op
import yaml
import boto3
from botocore.exceptions import ClientError
import logging

import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig(ABC):
    """
    BaseConfig is an abstract base class that provides common configuration
    and AWS utility methods for derived classes. It is designed to handle
    configuration loading, secret management, and AWS S3 interactions.

    Attributes:
    config_path (str): Path to the configuration file. Defaults to "config.yaml".
    industry (str): Name of the industry for which to load the configuration.
    demo_name (str): Name of the demo for which to load the configuration.
    config (Dict): The entire configuration dictionary.
    industry_config (Dict): Configuration dictionary for the specified industry.
    demo_config (Dict): Configuration dictionary for the specified demo.
    aws_region (str): AWS region for the S3 bucket and other AWS services.
    secret_manager (boto3.client): Boto3 Secrets Manager client.
    aws_user_secret (Dict): AWS user secret containing access key ID and secret access key.
    aws_access_key_id (str): AWS access key ID.
    aws_secret_access_key (str): AWS secret access key.
    mdb_url_secret (Dict): MongoDB URL secret containing cluster name, username, and password.
    mdb_clustername (str): MongoDB cluster name.
    mdb_username (str): MongoDB username.
    mdb_password (str): MongoDB password.
    mdb_uri_no_db (str): MongoDB URI without the database name.
    mdb_database (str): MongoDB database name.
    mdb_uri (str): MongoDB URI with the database name.
    s3 (boto3.client): Boto3 S3 client.
    """
    # This helps to abstract the config extraction for every child class
    # Assumes "config.yaml" in same folder of derived class. Can be customised.
    config_path = "config.yaml"

    def __init__(
            self,
            industry: str = None,
            demo_name: str = None,
    ):
        self.industry = industry
        self.demo_name = demo_name
        self.config = self.get_configuration()

        # Load the configuration for the specified industry and demo
        self.industry_config = self.config[self.industry] or None
        self.demo_config = self.industry_config[self.demo_name] or None

        self.aws_region = self.demo_config["aws_region"] or os.getenv("AWS_REGION")
        self.aws_access_key_id = self.demo_config["aws_access_key_id"] or os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = self.demo_config["aws_secret_access_key"] or os.getenv("AWS_SECRET_ACCESS_KEY")

        # Create a AWS Boto3 Session
        self.session = boto3.session.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region
        )

        # Create a Secrets Manager client
        self.secret_manager = self.session.client('secretsmanager',
                                region_name=self.aws_region,
                                aws_access_key_id=self.aws_access_key_id,
                                aws_secret_access_key=self.aws_secret_access_key)

        # Get the MongoDB URL secret
        if self.demo_config["mdb_url_secret"]:
            self.mdb_url_secret = self.get_secret(secret_name=self.demo_config["mdb_url_secret"], aws_region=self.aws_region)
            self.mdb_clustername = self.mdb_url_secret["clustername"]
            self.mdb_username = self.mdb_url_secret["username"]
            self.mdb_password = self.mdb_url_secret["password"]
            # Construct the MongoDB URI
            self.mdb_uri_no_db = f"mongodb+srv://{self.mdb_username}:{self.mdb_password}@{self.mdb_clustername}/"
            # Get the MongoDB database name
            self.mdb_database = self.demo_config["mdb_database"]
            # Construct the MongoDB URI with the database name
            self.mdb_uri = f"mongodb+srv://{self.mdb_username}:{self.mdb_password}@{self.mdb_clustername}/{self.mdb_database}"
        else:
            self.mdb_url_secret = None
            self.mdb_clustername = None
            self.mdb_username = None
            self.mdb_password = None
            self.mdb_uri = os.getenv("MONGODB_URI")

        # Create an S3 client
        self.s3 = self.session.client(service_name='s3',
                                region_name=self.aws_region,
                                aws_access_key_id=self.aws_access_key_id,
                                aws_secret_access_key=self.aws_secret_access_key)
        
        if self.config["hosting"]["origins"]:
            # Origins
            self.origins = self.config["hosting"]["origins"]
            
            # Local and Prod origins
            self.origins_local = self.origins["local"]
            self.origins_prod = self.origins["prod"]
        else:
            self.origins = os.getenv("ORIGINS")
            self.origins_local = os.getenv("ORIGINS")
            self.origins_prod = os.getenv("ORIGINS")

    @abstractmethod
    def execute(self):
        """
        Abstract method that must be implemented by child classes.
        This method should contain the main logic to be executed.
        """
        ...

    def get_configuration(self, industry: str ='') -> Dict:
        """
        Load the configuration for the specified industry.

        Parameters:
        industry (str): The name of the industry for which to load the configuration.

        Returns:
        Dict: The configuration dictionary for the specified industry.
        """
        import inspect
        configuration_path = op.join(
            op.dirname(inspect.getfile(self.__class__)),
            industry,
            self.config_path
        )
        try:
            with open(configuration_path) as conf:
                return yaml.load(conf, Loader=yaml.FullLoader) or {}
        except FileNotFoundError:
            # no point in creating a yaml config if there is no need for one.
            # we accept the scenario and return empty dict instead
            logging.info(
                f"Config file '{self.config_path}' not found")
            return {}

    def get_secret(self, secret_name: str, aws_region: str) -> Dict:
        """
        Retrieve a secret from AWS Secrets Manager.

        Parameters:
        secret_name (str): The name of the secret to retrieve.
        aws_region (str): The AWS region where the secret is stored.

        Returns:
        Dict: The secret dictionary.
        """
        # we create the secret manager if it was not created before
        if self.secret_manager is None:
            session = boto3.session.Session()
            self.secret_manager = session.client(
                service_name='secretsmanager',
                region_name=aws_region,
            )
        try:
            secret_response = self.secret_manager.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            error_code = e.response['Error']['Code']
            raise e

        # Only returning SecretString. todo: See if SecretBinary makes sense
        try:
            return json.loads(secret_response['SecretString'])
        # Allow getting string secrets
        except ValueError:
            return secret_response['SecretString']

    def upload_file_to_s3(
            self,
            file_name: str,
            bucket: str,
            object_name: str = None,
            s3_client=None
    ):
        """
        Upload a file to an S3 bucket.

        Parameters:
        file_name (str): File to upload.
        bucket (str): Bucket to upload to.
        object_name (str, optional): S3 object name. If not specified, file_name is used.
        s3_client: Optional S3 client to use. If not provided, the default client is used.

        Returns:
        bool: True if file was uploaded, else False.
        """
        if s3_client is not None:
            s3 = s3_client
        else:
            if self.s3 is None:
                self.s3 = boto3.client('s3')
            s3 = self.s3

        if object_name is None:
            object_name = file_name

        try:
            s3.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def download_file_from_s3(
            self,
            bucket_name: str,
            object_name: str,
            filename: str,
            s3_client=None
    ):
        """
        Download a file from an S3 bucket.

        Parameters:
        bucket_name (str): Name of the S3 bucket.
        object_name (str): Name of the object to download.
        filename (str): Name of the file to save the downloaded object to.
        s3_client: Optional S3 client to use. If not provided, the default client is used.

        Returns:
        str: The filename where the object was saved.
        """
        if s3_client is not None:
            s3 = s3_client
        else:
            if self.s3 is None:
                self.s3 = boto3.client('s3')
            s3 = self.s3
        s3.download_file(bucket_name, object_name, filename)
        return filename

    def list_s3_objects(self, bucket, prefix="", s3_client=None):
        """
        List objects in an S3 bucket.

        Parameters:
        bucket (str): Name of the S3 bucket.
        prefix (str, optional): Prefix to filter the objects. Defaults to "".
        s3_client: Optional S3 client to use. If not provided, the default client is used.

        Returns:
        list: List of object keys in the specified S3 bucket.
        """
        if s3_client is not None:
            s3 = s3_client
        else:
            if self.s3 is None:
                self.s3 = boto3.client('s3')
            s3 = self.s3

        s3_objects = []
        params = dict(Bucket=bucket, Prefix=prefix)
        while True:
            response = s3.list_objects_v2(**params)
            for s3_key in response["Contents"]:
                s3_objects.append(s3_key["Key"])

            if not response.get("NextContinuationToken"):
                break

            params["ContinuationToken"] = response["NextContinuationToken"]
        return s3_objects
