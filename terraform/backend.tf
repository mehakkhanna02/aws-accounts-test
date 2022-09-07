terraform {
  backend "s3" {
    bucket = "itoc-terraform-state"
    key    = "aws-accounts/terraform.tfstate"
    region = "ap-southeast-2"
  }
}
