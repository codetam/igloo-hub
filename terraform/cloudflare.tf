provider "cloudflare" {
  api_token = var.api_token
}

resource "cloudflare_dns_record" "igloo" {
  zone_id = var.zone_id
  name    = "igloo"
  content = aws_cloudfront_distribution.static_site_distribution.domain_name
  type    = "CNAME"
  ttl     = 60
  proxied = false
  comment = "cloudfront domain"
}

locals {
  first_validation_option = tolist(aws_acm_certificate.ssl_cert.domain_validation_options)[0]
}

resource "cloudflare_dns_record" "acm_validation" {
  zone_id = var.zone_id
  name    = local.first_validation_option.resource_record_name
  type    = local.first_validation_option.resource_record_type
  content = local.first_validation_option.resource_record_value
  ttl     = 60
}



