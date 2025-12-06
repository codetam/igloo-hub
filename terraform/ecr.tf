resource "aws_ecr_repository" "igloo_repository" {
  name                 = var.backend_image_name
  image_tag_mutability = "MUTABLE"
}