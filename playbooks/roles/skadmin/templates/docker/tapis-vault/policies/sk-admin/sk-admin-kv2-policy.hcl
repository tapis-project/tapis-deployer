# See https://www.vaultproject.io/docs/secrets/kv/kv-v2.html
#     https://www.vaultproject.io/api/secret/kv/kv-v2.html.

# Most permissions on 'secret/data/tapis/*'.  Note that delete here
# applies to the latest version of a key only.  
path "secret/data/tapis/*" {
  capabilities = [ "create", "read", "update", "delete", "sudo" ]
}

# Allow the policy to delete any version of a key.
path "secret/delete/tapis/*" {
  capabilities = ["update"]
}

# Allow the policy to undelete data.
path "secret/undelete/tapis/*" {
  capabilities = ["update"]
}

# Allow the policy to destroy any version of a key.
path "secret/destroy/tapis/*" {
  capabilities = ["update"]
}

# Allow the policy to list, view metadata and permanently remove 
# all versions and metadata of a key.
path "secret/metadata/tapis/*" {
  capabilities = ["list", "read", "delete"]
}

