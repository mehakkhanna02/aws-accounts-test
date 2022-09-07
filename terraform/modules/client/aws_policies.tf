
locals { 
  default_roles = jsondecode(file("../default_roles.json"))
  client_json = jsondecode(file("../clients/${var.client_name}.json"))
  
  roles = merge(lookup(local.client_json, "roles", {}), local.default_roles)

  client_all_roles = flatten([
    for k, v in local.client_json.accounts : 
    [ for g in v.roles : { account_id = v.account_id, role = g } ]
  ])

  client_roles_readonly = [
    for g in local.client_all_roles :
    "arn:aws:iam::${g.account_id}:role/${g.role}"
    if !lookup(local.default_roles, g.role, {is_write = true}).is_write
  ]

  client_roles_write = [
      for g in local.client_all_roles :
      "arn:aws:iam::${g.account_id}:role/${g.role}"
    ]
}


resource "aws_s3_bucket_object" "read_only" {
  bucket = "itoc-client-roles"
  key    = "client_aws_${var.client_name}_readonly.json"
  content = jsonencode({
        Roles = local.client_roles_readonly
      })
}

resource "aws_s3_bucket_object" "write" {
  bucket = "itoc-client-roles"
  key    = "client_aws_${var.client_name}_write.json"
  content = jsonencode({
        Roles = local.client_roles_write
      })
}
