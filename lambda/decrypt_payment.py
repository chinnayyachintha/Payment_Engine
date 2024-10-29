import boto3
import json
import os
from botocore.exceptions import ClientError

# Initialize AWS clients
secrets_client = boto3.client('secretsmanager')
kms_client = boto3.client('kms')

def lambda_handler(event, context):
    try:
        # Retrieve the encrypted payment data from the input event
        encrypted_data = event['encryptedData']
        
        # Fetch the decryption key from Secrets Manager
        secret_name = os.getenv('SECRET_NAME')
        secret = secrets_client.get_secret_value(SecretId=secret_name)
        secret_value = json.loads(secret['SecretString'])
        decryption_key_id = secret_value.get("decryptionKeyId")
        
        # Decrypt the payment data using AWS KMS
        decrypted_data = kms_client.decrypt(
            CiphertextBlob=bytes.fromhex(encrypted_data),
            KeyId=decryption_key_id
        )['Plaintext'].decode('utf-8')
        
        # Return the decrypted data
        return {
            "statusCode": 200,
            "decryptedData": decrypted_data
        }
    
    except ClientError as e:
        print(f"Error decrypting payment data: {e}")
        return {
            "statusCode": 500,
            "error": "Failed to decrypt payment data"
        }

# Explanation:

# This function fetches the decryption key from AWS Secrets Manager, decrypts the encrypted data using AWS KMS, and returns the decrypted data.
# Make sure to replace encryptedData in the event payload with the actual name used in your process.