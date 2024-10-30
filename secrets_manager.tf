# Secrets Manager will securely store sensitive data, like authorization tokens, needed by the Lambdas.

# Secret for Elavon Authorization Token
resource "aws_secretsmanager_secret" "elavon_auth_token" {
  name        = "elavon_auth_token"
  description = "Authorization token for Elavon payment processing"
}

resource "aws_secretsmanager_secret_version" "elavon_auth_token_value" {
  secret_id     = aws_secretsmanager_secret.elavon_auth_token.id
  secret_string = jsonencode({
    "authorization" = var.elavon_auth_token_value  # Change the key to 'authorization'
  })
}
