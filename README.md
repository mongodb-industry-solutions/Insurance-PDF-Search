# Insurance-PDF-Search

## Prerequisites:

- **[MongoDB Atlas account](https://www.mongodb.com/products/platform/atlas-database)**: A cloud-based MongoDB account for creating the database and managing data.

## Setup Instructions

### Step 0: Set Up MongoDB Database and Collection

1. Log in to [MongoDB Atlas](https://account.mongodb.com/account/login) and create a new database named `insurance_pdf_rag`.
2. Inside this database, create a collection called `default`.

### Step 1: Configure the Environment Variables for the backend

### Add environment variables

> **_Note:_** Create a .env file within the backend directory.

```bash
MONGODB_URI="mongodb+srv://<REPLACE_USERNAME>:<REPLACE_PASSWORD>@<REPLACE_CLUSTER_NAME>.mongodb.net/<REPLACE_DATABASE_NAME>"
PDF_PATH="/data/pdfs"
PDF_IMAGES="/data/pdf-images"
ARTIFACT_STORE="/data/artifacts"
OPENAI_ACCESS_KEY=<REPLACE_OPENAI_ACCESS_KEY>
TITLE="PDF Search in Insurance with MongoDB Vector Search and Superduper"
ORIGINS=http://localhost:3000
```

### Create folder structure

1. Create `/artifacts` and `/pdf-images` folders within `backend/data/`

> **_Note:_** Notice that this is the same folders where the `/pdfs` are. You will end up having 3 folders inside `backend/data/`.

### Step 2. Configure the Environment Variables for the frontend

1. In the `frontend` folder, create a `.env.local` file.
2. Add the URL for the API using the following format:

```bash
NEXT_PUBLIC_ASK_THE_PDF_API_URL="http://localhost:8000/querythepdf"
```

### Step 3: Run the backend

1. Navigate to the `backend` folder.
2. Install dependencies using [Poetry](https://python-poetry.org/) by running:
```bash
poetry install
```
3. Start the backend server with the following command:
```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```
The backend will now be accessible at http://localhost:8000, ready to handle API requests for image vector search.

### Step 4 Run the frontend
1. Navigate to the `frontend` folder.
2. Install dependencies by running:
```bash
npm install
```
3. Start the frontend development server with:
````bash
npm run dev
````

The frontend will now be accessible at http://localhost:3000 by default, providing a user interface to interact with the image vector search demo.

## Docker Setup Instructions

To run the application using Docker, follow these setup steps:

### Build the Application
> **_NOTE:_** If you don’t have make installed, you can install it using `sudo apt install make` or `brew install make`

To build the Docker images and start the services, run the following command:
```bash
make build
```

> **_NOTE:_** Depending on the version of Docker Compose you have installed, you might need to modify the Makefile to use docker-compose (with a hyphen) instead of docker compose (without a hyphen), as the command format can vary between versions.

### Stopping the Application

To stop all running services, use the command:
```bash
make stop
```

### Cleaning Up

To remove all images and containers associated with the application, execute:
```bash
make clean
```

## **Deploy on AWS EC2 Instance**

In this guide, we'll deploy a **t2.micro** instance running **Ubuntu Server 24.04 LTS** with approximately **20 GB** of storage.

### **Step 1: Create the EC2 Instance**
- Launch a t2.micro EC2 instance with Ubuntu Server 24.04 LTS from the AWS Console.

> **_NOTE:_** Ensure that you open port 3000 for the frontend and port 8000 for the backend in your security group settings. Additionally, allow outbound traffic to port 27017, which is the default port for MongoDB.

### **Step 2: SSH into the Instance**
Once the instance is up and running, SSH into the machine using the following command:

```bash
ssh ubuntu@<your-ec2-ip-address>
```

### **Step 3: Update the Package Index**
Before installing any packages, it's good practice to update the package index:

```
sudo apt update
```

### **Step 4: Install Docker**
Install Docker on your EC2 instance by running the following command:

```
sudo apt install docker.io -y
```

Verify the installation by checking the Docker version:
```
docker --version
```

### **Step 5: Install Docker Compose**
Download Docker Compose:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Make Docker Compose executable:
```
sudo chmod +x /usr/local/bin/docker-compose
```

Check the Docker Compose version:
```
docker-compose --version
```

### **Step 6: Start and Enable Docker Service**
Start the Docker service:
```
sudo systemctl start docker
```

Enable Docker to start on boot:
```
sudo systemctl enable docker
```
