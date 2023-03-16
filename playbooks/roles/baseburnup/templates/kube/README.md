# Tapis Deployment


## To Deploy Tapis (burn up)

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


## To Take Down Tapis (burn down) 

To take down the higher level services:

    # ./burndown secondary_services
    ...

To take down the basic api token services:

    # ./burndown primary_services
    ...

To take down the authorization stack and required services:

    # ./burndown authstack
    ...
    

**Note that the main nginx proxy will not be taken down by the above. To take down the proxy also run:**

    # ./burndown proxy
    ...
    

