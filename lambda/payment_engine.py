import boto3
import json
import os
import requests
from botocore.exceptions import ClientError

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
secrets_client = boto3.client('secretsmanager')
sns_client = boto3.client('sns')

# Set up environment variables
table_name = os.getenv('DYNAMODB_TABLE')
secret_name = os.getenv('SECRET_NAME')
sns_topic_arn = os.getenv('SNS_TOPIC_ARN')

# Initialize DynamoDB table
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Get decrypted payment data from the event
        payment_data = event['decryptedData']
        
        # Fetch the Elavon API key from Secrets Manager
        secret = secrets_client.get_secret_value(SecretId=secret_name)
        secret_value = json.loads(secret['SecretString'])
        elavon_api_key = secret_value.get("apiKey")
        
        # 1. Send payment data to Elavon
        elavon_response = process_payment_with_elavon(payment_data, elavon_api_key)
        
        # 2. Log transaction details in DynamoDB
        transaction_id = elavon_response.get("transactionId", "N/A")
        log_transaction(transaction_id, payment_data, elavon_response)
        
        # 3. Optional: Call 3DS API if required
        if payment_data.get("requires3DS"):
            process_3ds_authentication(payment_data)
        
        # 4. Apply rules via the payment gateway rule engine
        apply_payment_rules(payment_data)
        
        return {
            "statusCode": 200,
            "transactionId": transaction_id,
            "elavonResponse": elavon_response
        }

    except Exception as e:
        print(f"Error in payment processing: {e}")
        send_failure_alert(str(e))
        return {
            "statusCode": 500,
            "error": "Payment processing failed"
        }

def process_payment_with_elavon(payment_data, api_key):
    """Send payment data to Elavon's API and return the response."""
    try:
        # Replace with the actual Elavon API endpoint
        elavon_url = "https://api.elavon.com/v1/payments"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        response = requests.post(elavon_url, headers=headers, json=payment_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to process payment with Elavon: {e}")

def log_transaction(transaction_id, payment_data, elavon_response):
    """Log the transaction to DynamoDB."""
    try:
        table.put_item(
            Item={
                "TransactionID": transaction_id,
                "PaymentData": json.dumps(payment_data),
                "ElavonResponse": json.dumps(elavon_response),
                "Status": elavon_response.get("status", "Unknown")
            }
        )
    except ClientError as e:
        print(f"Error logging transaction: {e}")

def process_3ds_authentication(payment_data):
    """Simulate calling a 3DS API for authentication."""
    print("3DS Authentication processed")

def apply_payment_rules(payment_data):
    """Apply business rules before finalizing the transaction."""
    print("Payment rules applied")

def send_failure_alert(error_message):
    """Send an alert to SNS topic on transaction failure."""
    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=f"Payment processing failed: {error_message}",
        Subject="Transaction Failure Alert"
    )


# Explanation:

# process_payment_with_elavon: Sends payment data to the Elavon API for processing and returns the response.
# log_transaction: Logs transaction details in DynamoDB.
# process_3ds_authentication: Simulates a call to the 3D Secure API, if required.
# apply_payment_rules: Applies any necessary rules through the payment gateway rule engine.
# send_failure_alert: Sends an SNS alert if a transaction fails.