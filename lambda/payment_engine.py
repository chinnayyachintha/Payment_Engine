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
intilysis_url = os.getenv('INTILYSIS_URL')  # New environment variable for Intilysis endpoint

# Initialize DynamoDB table
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Get decrypted payment data from the event
        payment_data = event['decryptedData']
        
        # Fetch the Elavon authorization token from Secrets Manager
        secret = secrets_client.get_secret_value(SecretId=secret_name)
        secret_value = json.loads(secret['SecretString'])
        elavon_auth_token = secret_value.get("authorization")  # Fetch the authorization token
        
        # 1. Send payment data to Elavon
        elavon_response = process_payment_with_elavon(payment_data, elavon_auth_token)
        
        # 2. Log transaction details in DynamoDB
        transaction_id = elavon_response.get("transactionId", "N/A")
        log_transaction(transaction_id, payment_data, elavon_response)
        
        # 3. Optional: Call 3DS API if required
        if payment_data.get("requires3DS"):
            process_3ds_authentication(payment_data)
        
        # 4. Apply rules via the payment gateway rule engine
        apply_payment_rules(payment_data)
        
        # 5. Send transaction details to Intilysis
        send_to_intilysis(transaction_id, payment_data, elavon_response)
        
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

def process_payment_with_elavon(payment_data, auth_token):
    """Send payment data to Elavon's API and return the response."""
    try:
        # Replace with the actual Elavon API endpoint
        elavon_url = "https://api.elavon.com/v1/payments" # change these with original elavon_url
        headers = {"Authorization": auth_token, "Content-Type": "application/json"}  # Use auth_token
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

def send_to_intilysis(transaction_id, payment_data, elavon_response):
    """Send transaction details to the Intilysis API."""
    try:
        intilysis_payload = {
            "transactionId": transaction_id,
            "paymentData": payment_data,
            "elavonResponse": elavon_response
        }
        response = requests.post(intilysis_url, json=intilysis_payload)
        response.raise_for_status()  # Raise an error for bad responses
        print("Successfully sent data to Intilysis")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send data to Intilysis: {e}")
