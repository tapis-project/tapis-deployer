# tokens



## add token roles

Token roles must be added before service can start first time

    docker run -it -e tenants_service_password='<password>' -e service_tenant_base_url='<url>' tapis/add_token_roles

so, for ex:

    docker run -it -e tenants_service_password='changeme989aa1ae4c12f92f41910a450a5b6c3f' -e service_tenant_base_url='https://admin.develop.tapis.io' tapis/add_token_roles




    
    
