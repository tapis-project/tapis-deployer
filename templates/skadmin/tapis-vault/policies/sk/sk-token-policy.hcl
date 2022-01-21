# See https://www.vaultproject.io/api/auth/token/index.html
#
# These policies are not tapis limited.     

# Manage token methods broadly across Vault.  It's not obvious
# what permissions are needed for what actions, so we liberally
# assign permissions for now.
path "auth/token/*"
{
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

# Manage auth methods broadly across Vault
path "auth/*"
{
  capabilities = ["read", "list"]
}

