# SNS Topic for transaction failure alerts
resource "aws_sns_topic" "transaction_alerts" {
  name = "TransactionAlerts"
}
