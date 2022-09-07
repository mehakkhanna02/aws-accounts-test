locals {
  client_files = fileset("../clients", "*.json")
  clients      = toset([for s in local.client_files : replace(s, ".json", "")])
}

module "client" {
  for_each = local.clients
  source   = "./modules/client"

  client_name = each.value

  providers = {
    aws = aws.identity
  }
}