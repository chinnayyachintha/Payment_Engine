# Lambda function to decrypt payment data
resource "aws_lambda_function" "decrypt_payment" {
  function_name = "DecryptPaymentProcessFunction"
  role          = aws_iam_role.decrypt_payment_role.arn
  handler       = "decrypt_payment.lambda_handler"
  runtime       = "python3.8"
  filename      = "lambda/decrypt_payment.zip" # Provide the actual path to your code

  environment {
    variables = {
      SECRET_NAME = aws_secretsmanager_secret.elavon_api_key.name
    }
  }
}

# Lambda function for payment processing
resource "aws_lambda_function" "payment_engine" {
  function_name = "paymentEngine"
  role          = aws_iam_role.payment_engine_role.arn
  handler       = "payment_engine.lambda_handler"
  runtime       = "python3.8"
  filename      = "lambda/payment_engine.zip" # Provide the actual path to your code

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.transaction_logs.name,
      SECRET_NAME    = aws_secretsmanager_secret.elavon_api_key.name
    }
  }
}
