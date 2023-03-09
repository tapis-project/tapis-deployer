# vault

# first time setup

Create configmap & pvc:

    kubectl create configmap vaultconf --from-file vault.hcl 
    kubectl apply -f pvc.yml 
    kubectl wait --for=condition=complete job/prep-vault-pvc

Start vault:

    kubectl apply -f vault.yml
    kubectl wait --for=condition=available deploy/vault  

Enter the pod and init the vault:

    pod=`kubectl get pods --selector=app=vault -o jsonpath='{.items[*].metadata.name}'` 
    kubectl exec -it $pod sh
    # vault operator init 

**You will now see a big thing like this. Copy and paste into a safe place. You will never see it again. If it is lost, your vault is sealed forever.**

[https://media.giphy.com/media/MJWLVaxzeq8gg/giphy.gif]

    Unseal Key 1: Rd1oHIGin+NirnhNVF5c1x1GacRhQtMv0/x/6UfCVMjS
    Unseal Key 2: thdWxkdPwEvu+d0hEoVb3Vr/7qeRXF94Gbwdt1lOGpf6
    Unseal Key 3: YlH7PoL36u90IW90IlKbUnqktyqXdRD8z8usP9xT3Raw
    Unseal Key 4: +eCjOJrKJj5DNACstaXUFRYetV+wCBZglNIEf1RnrP9T
    Unseal Key 5: Vn1WhEzj0nvXFHBPZ6W01v8iw9J9699aMRlJh4VAJkOb
    
    Initial Root Token: s.8RsbB1dUX0eg1kuOUfktcXim
    
    Vault initialized with 5 key shares and a key threshold of 3. Please securely
    distribute the key shares printed above. When the Vault is re-sealed,
    restarted, or stopped, you must supply at least 3 of these keys to unseal it
    before it can start servicing requests.
    
    Vault does not store the generated master key. Without at least 3 key to
    reconstruct the master key, Vault will remain permanently sealed!
    
    It is possible to generate new unseal keys, provided you have a quorum of
    existing unseal keys shares. See "vault operator rekey" for more information.
    
 
You can enable kv secrets   

    export VAULT_TOKEN=s.8RsbB1dUX0eg1kuOUfktcXim
    vault secrets enable -path=secret/ kv

# Using vault

Now start following along here: [https://learn.hashicorp.com/vault/getting-started/first-secret]

# Restarting

BTW now you can stop and start the vault deployment:

    kubectl delete -f vault.yml
    kubectl wait --for=condition=available deploy/vault  
    kubectl apply -f vault.yml

You will have to exec into the new pod and "unseal" the vault *3* time using the keys you saved:

    pod=`kubectl get pods --selector=app=vault -o jsonpath='{.items[*].metadata.name}'` 
    kubectl exec -it $pod sh
    # vault operator unseal 
    Unseal Key (will be hidden): 
    Key                Value
    ---                -----
    Seal Type          shamir
    Initialized        true
    Sealed             true
    Total Shares       5
    Threshold          3
    Unseal Progress    1/3
    Unseal Nonce       720d3003-1de7-1528-54d8-64ff0da68d12
    ...

# test 

    pod=`kubectl get pods --selector=app=vault -o jsonpath='{.items[*].metadata.name}'` 
    vtok="s.koXrQzSGUtRXe9JvvOoabAvq"
    curl --header "X-Vault-Token: $vtok" --data '{"type": "approle"}' -X POST http://mykube.example.com:30907/v1/sys/auth/init



