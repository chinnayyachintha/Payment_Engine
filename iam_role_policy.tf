# IAM Role for Decrypt Payment Process Lambda
resource "aws_iam_role" "decrypt_payment_role" {
  name = "DecryptPaymentProcessRole"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [{
      "Action" : "sts:AssumeRole",
      "Principal" : {
        "Service" : "lambda.amazonaws.com"
      },
      "Effect" : "Allow",
      "Sid" : ""
    }]
  })
}

# Policy for accessing Secrets Manager and KMS for decryption
resource "aws_iam_policy" "decrypt_payment_policy" {
  name = "DecryptPaymentProcessPolicy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : [
          "secretsmanager:GetSecretValue",
          "kms:Decrypt"
        ],
        "Resource" : "*",
        "Effect" : "Allow"
      }
    ]
  })
}

# Attach the policy to the Decrypt Payment Role
resource "aws_iam_role_policy_attachment" "decrypt_policy_attachment" {
  role       = aws_iam_role.decrypt_payment_role.name
  policy_arn = aws_iam_policy.decrypt_payment_policy.arn
}

# IAM Role for Payment Engine Lambda
resource "aws_iam_role" "payment_engine_role" {
  name = "PaymentEngineRole"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [{
      "Action" : "sts:AssumeRole",
      "Principal" : {
        "Service" : "lambda.amazonaws.com"
      },
      "Effect" : "Allow",
      "Sid" : ""
    }]
  })
}

# Policy for accessing Secrets Manager, DynamoDB, SNS, and external APIs
resource "aws_iam_policy" "payment_engine_policy" {
  name = "PaymentEnginePolicy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : [
          "secretsmanager:GetSecretValue",
          "dynamodb:PutItem",
          "sns:Publish"
        ],
        "Resource" : "*",
        "Effect" : "Allow"
      }
    ]
  })
}

# Attach the policy to the Payment Engine Role
resource "aws_iam_role_policy_attachment" "payment_engine_policy_attachment" {
  role       = aws_iam_role.payment_engine_role.name
  policy_arn = aws_iam_policy.payment_engine_policy.arn
}
