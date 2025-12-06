variable "environment" {
    description = "The deployment environment (e.g., dev, qa, prod)"
    type        = string
}

variable "domain" {
    description = "Landing page domain"
    type = string
}

variable "region" {
    description = "AWS region for the resources"
    default     = "us-east-1"
}

variable "api_token" {
    description = "Cloudflare API token"
    type = string
}

variable "zone_id" {
    description = "Cloudflare zone ID"
    type = string
}

variable "account_id" {
    description = "Cloudflare account ID"
    type = string
}

variable "backend_image_name" {
    description = "ECR backend image name"
    default = "igloo-fastapi-lambda-backend"
}

variable "api_name" {
    description = "API Gateway name"
    default = "igloo-api-gateway"
}

variable "lambda_function_name" {
    description = "Lambda function name"
    default = "igloo-lambda"
}

variable "backend_image_version" {
    default = "latest"
}


variable "POSTGRES_SERVER" {
    type = string
}
variable "POSTGRES_PORT" {
    type = string
}
variable "POSTGRES_DB" {
    type = string
}
variable "POSTGRES_USER" {
    type = string
}
variable "POSTGRES_PASSWORD" {
    type = string
}