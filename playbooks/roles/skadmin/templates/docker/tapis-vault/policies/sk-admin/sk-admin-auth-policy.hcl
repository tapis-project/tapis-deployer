# See https://learn.hashicorp.com/vault/identity-access-management/iam-policies
#     https://www.vaultproject.io/guides/identity/policies
#
# These policies are not tapis limited.     

# Manage auth methods broadly across Vault
path "auth/*"
{
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Create, update, and delete auth methods
path "sys/auth/*"
{
  capabilities = ["create", "update", "delete", "sudo"]
}

# List auth methods.  
path "sys/auth"
{
  capabilities = ["read"]
}
