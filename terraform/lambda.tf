## Create IAM Role

data "aws_iam_policy_document" "assume_lambda_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_model_role" {
  name = "my-lambda-model-role"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda_role.json
}

## Add Cloudwatch logs policy

data "aws_iam_policy_document" "logs_policy_document" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = [
      "arn:aws:logs:*:*:*",
    ]
  }
}

resource "aws_iam_policy" "logs_policy" {
  name        = "logs-policy"
  description = "Allow cloudwatch logs"
  policy      = data.aws_iam_policy_document.logs_policy_document.json
}

resource "aws_iam_role_policy_attachment" "lambda_model_policy_attachement" {
  role       = aws_iam_role.lambda_model_role.name
  policy_arn = aws_iam_policy.logs_policy.arn
}

resource "aws_lambda_function" "lambda_model_function" {
    function_name = var.lambda_function_name
    role = aws_iam_role.lambda_model_role.arn
    package_type = "Image"

    image_uri    = "${aws_ecr_repository.igloo_repository.repository_url}:${var.backend_image_version}"

    memory_size = 256
    timeout     = 30

    environment {
      variables = {
        POSTGRES_SERVER   = var.POSTGRES_SERVER
        POSTGRES_PORT     = var.POSTGRES_PORT
        POSTGRES_DB       = var.POSTGRES_DB
        POSTGRES_USER     = var.POSTGRES_USER
        POSTGRES_PASSWORD = var.POSTGRES_PASSWORD
      }
    }
}




