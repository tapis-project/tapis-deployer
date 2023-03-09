# See https://www.vaultproject.io/docs/auth/approle.html
#     https://www.vaultproject.io/api/auth/approle/index.html
#     https://learn.hashicorp.com/vault/identity-access-management/iam-authentication
#     https://www.hashicorp.com/blog/authenticating-applications-with-vault-approle/
      
# Create and manage roles
path "auth/approle/role/*" {
  capabilities = [ "read", "list" ]
}

