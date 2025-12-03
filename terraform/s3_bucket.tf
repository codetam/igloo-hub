resource "aws_s3_bucket" "landing_page_bucket" {
  bucket = "igloo-hub-frontend-${var.environment}"

  tags = {
    Name        = "landing-page"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_public_access_block" "landing_page_public_access" {
  bucket = aws_s3_bucket.landing_page_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_website_configuration" "static_site" {
  bucket = aws_s3_bucket.landing_page_bucket.id

  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_policy" "landing_page_bucket_policy" {
  bucket = aws_s3_bucket.landing_page_bucket.id
  depends_on = [aws_s3_bucket_public_access_block.landing_page_public_access]

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowGetObj",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::${aws_s3_bucket.landing_page_bucket.id}/*"
    }
  ]
}
POLICY
}

resource "aws_s3_object" "files_upload" {
  for_each = fileset("${path.root}/../frontend/dist", "**/*.*")
  bucket      = aws_s3_bucket.landing_page_bucket.id
  key         = "${each.value}"
  source      = "${path.root}/../frontend/dist/${each.value}"
  source_hash = filebase64sha256("${path.root}/../frontend/dist/${each.value}")
  content_type = lookup(
    {
      html = "text/html",
      css  = "text/css",
      js   = "application/javascript",
      png  = "image/png",
      jpg  = "image/jpeg",
      svg  = "image/svg+xml"
    },
    lower(split(".", each.value)[length(split(".", each.value)) - 1]),
    "binary/octet-stream"
  )
}