# Secrets Manager will securely store sensitive data, like API keys, needed by the Lambdas.

# Secret for Elavon API Key
resource "aws_secretsmanager_secret" "elavon_api_key" {
  name        = "elavon_api_key"
  description = "API key for Elavon payment processing"
}

resource "aws_secretsmanager_secret_version" "elavon_api_key_value" {
  secret_id = aws_secretsmanager_secret.elavon_api_key.id
  secret_string = jsonencode({
    "apiKey" = var.elavon_api_key_value
  })
}
