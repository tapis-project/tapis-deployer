# tokens



## add token roles

Token roles must be added before service can start first time

    docker run -it -e tenants_service_password='<password>' -e service_tenant_base_url='<url>' tapis/add_token_roles

so, for ex:

    docker run -it -e tenants_service_password='changeme0123456789' -e service_tenant_base_url='{{tokens_service_tenant_id}}' tapis/add_token_roles




    
    
