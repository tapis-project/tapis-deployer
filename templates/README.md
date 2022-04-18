# Tapis Deployment


To deploy the base proxy and security services:


    # ./burnup init 
    ...
    
Only if deploying an associate site: you'll be asked to run a script to collect public keys and send to your tenant admin.

    "Collecting public keys for associate site tenants. Please send these to your tenants admin before next steps in deployment."
    
    # ./burnup get_public_keys
    ...
    
To deploy the basic api token services:
    
    # ./burnup primary_services
    ...
    
To deploy the higher level services:

    # ./burnup secondary_services
    ...
