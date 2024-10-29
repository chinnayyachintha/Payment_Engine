output "decrypt_payment_lambda_arn" {
  value = aws_lambda_function.decrypt_payment.arn
}

output "payment_engine_lambda_arn" {
  value = aws_lambda_function.payment_engine.arn
}

output "sns_topic_arn" {
  value = aws_sns_topic.transaction_alerts.arn
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.transaction_logs.name
}
