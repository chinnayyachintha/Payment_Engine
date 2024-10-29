# DynamoDB will be used to log transaction data from the Payment Engine Lambda.

# DynamoDB Table for logging transactions
resource "aws_dynamodb_table" "transaction_logs" {
  name         = "TransactionLogs"
  hash_key     = "TransactionID"
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "TransactionID"
    type = "S"
  }
}
