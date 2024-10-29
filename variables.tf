# Variable to specify the AWS Region where resources will be deployed
variable "aws_region" {
  type        = string
  description = "AWS Region to deploy resources"
}

# specifying elavon api key value
variable "elavon_api_key_value" {
  type        = string
  description = "value of api_key value"
}

