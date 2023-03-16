# tokens



## add token roles

Token roles must be added before service can start first time

    docker run -it -e tenants_service_password='<password>' -e primary_site_admin_tenant_base_url='<url>' {{ tokens_add_token_roles_image }}

so, for ex:

    docker run -it -e tenants_service_password='changeme' -e primary_site_admin_tenant_base_url='{{tokens_service_tenant_id}}' {{ tokens_add_token_roles_image }}




    
    
