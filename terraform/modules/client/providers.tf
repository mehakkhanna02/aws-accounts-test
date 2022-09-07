terraform {
  required_providers {
    okta = {
      source  = "okta/okta"
      version = "~> 3.10"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}