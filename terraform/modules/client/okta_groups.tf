resource "okta_group" "aws_read_only" {
  name        = "client_aws_${var.client_name}_readonly"
  description = "Read only access to ${var.client_name} AWS accounts"
}

resource "okta_group" "aws_write" {
  name        = "client_aws_${var.client_name}_write"
  description = "Write access to ${var.client_name} AWS accounts"
}