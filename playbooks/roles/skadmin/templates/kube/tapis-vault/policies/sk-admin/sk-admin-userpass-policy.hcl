# See https://www.vaultproject.io/docs/auth/userpass.html
#     https://www.vaultproject.io/api/auth/userpass/index.html
      
# All permissions on 'auth/userpass/tapis/*'. 
path "auth/userpass/tapis/*" {
  capabilities = [ "create", "read", "update", "delete", "list", "sudo" ]
}

