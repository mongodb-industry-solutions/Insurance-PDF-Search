import random
from datetime import datetime, timedelta

def generate_random_date(start, end):
    """Generate a random date between start and end dates."""
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    time_between_dates = end_date - start_date
    random_number_of_days = random.randrange(time_between_dates.days)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime("%Y-%m-%d")

def create_documents(n):
    documents = []
    coverage_codes = ["999", "888", "777", "666", "555"]
    coverage_descriptions = {
        "999": "accidental driver-responsible damage",
        "888": "3rd party responsible",
        "777": "Vehicle rental/loaner service for customer",
        "666": "Glass windshield repair",
        "555": "Autobody and paint repair"
    }
    claim_status_codes = ["Active", "Closed", "Subrogation"]

    for i in range(n):
        customer_id = f"c{i:03}"
        policy_number = f"p{i:03}"
        claim_id = f"cl{i:03}"
        insurable_object_id = f"abc{i:03}"
        claim_description = " ".join([f"Line {j+1} of detailed claim description." for j in range(random.randint(6, 7))])
        total_loss_amount = random.randint(100, 5000)
        claim_fnol_date = generate_random_date("2020-01-01", "2021-12-31")
        claim_closed_date = generate_random_date("2022-01-01", "2022-12-31")
        claim_line_code = "Auto"
        damage_description = "Detailed damage description."
        vehicle_make = "Make" + str(random.randint(1, 5))
        vehicle_model = "Model" + str(random.randint(1, 5))
        coverage_code = random.choice(coverage_codes)
        coverage_description = coverage_descriptions[coverage_code]
        claim_status_code = random.choice(claim_status_codes)

        document = {
            "customerID": customer_id,
            "policyNumber": policy_number,
            "claimID": claim_id,
            "claimStatusCode": claim_status_code,
            "claimDescription": claim_description,
            "totalLossAmount": total_loss_amount,
            "claimFNOLDate": claim_fnol_date,
            "claimClosedDate": claim_closed_date,
            "claimLineCode": claim_line_code,
            "damageDescription": damage_description,
            "insurableObject": {
                "insurableObjectId": insurable_object_id,
                "vehicleMake": vehicle_make,
                "vehicleModel": vehicle_model
            },
            "coverages": [
                {
                    "coverageCode": coverage_code,
                    "description": coverage_description
                }
            ]
        }
        documents.append(document)
    return documents

# Generate 50 documents
documents = create_documents(50)
# Output the first document to check the structure
documents[0]
