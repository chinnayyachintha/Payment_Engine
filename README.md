**Decrypt Payment Process Lambda**: 
The Terraform and Lambda code securely decrypts the payment data before it’s passed on for further processing by:

- Using AWS Secrets Manager to retrieve the decryption key securely.
- Implementing decryption logic within the Lambda function.

**Payment Engine Lambda**: 
The Terraform and Lambda code handle the core payment processing and communication with:

- `Elavon`: By calling Elavon’s API for the payment transaction.
- `DynamoDB`: By logging transaction details.
- `3DS API`: By including a placeholder function for 3D Secure authentication.
- `PaymentGateway Rule Engine`: By including a placeholder function to apply business rules before finalizing the transaction.