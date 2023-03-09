# See https://learn.hashicorp.com/vault/getting-started/policies
#     https://learn.hashicorp.com/vault/identity-access-management/iam-policies
#     https://learn.hashicorp.com/vault/identity-access-management/iam-authentication
#     https://learn.hashicorp.com/vault/identity-access-management/policy-templating
#     https://www.vaultproject.io/api/system/policy.html
#     https://www.vaultproject.io/guides/identity/policies
#     https://www.vaultproject.io/docs/concepts/policies.html

# NOTE: It appears that the sys/policies/acl/* endpoints are tailored for REST API usage
#       whereas sys/policy/* endpoints are tailored for CLI usage.  Until we find a need
#       for the latter endpoints, we're going to mostly limit ourselves to the former.  
#       See https://www.vaultproject.io/guides/identity/policies for clues.

# Write ACL policies
path "sys/policies/acl/tapis/*" {
  capabilities = [ "create", "read", "update", "delete", "list", "sudo" ]
}

# List existing policies. Note this is not tapis limited.
path "sys/policy"
{
  capabilities = ["list"]
}

# Read existing policy content. Note this is not tapis limited.
path "sys/policy/*"
{
  capabilities = ["read"]
}

