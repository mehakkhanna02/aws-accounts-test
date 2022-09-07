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

# Configure the Okta Provider
provider "okta" {}

# Configure the AWS Provider
provider "aws" {
  region = "ap-southeast-2"
}

provider "aws" {
  alias = "identity"
  region = "ap-southeast-2"
  assume_role {
    role_arn     = "arn:aws:iam::394966198205:role/ItocGitHubAWSAccounts"
    session_name = "github_actions_aws-accounts"
  }
}
