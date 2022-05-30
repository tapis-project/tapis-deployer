# Tapis setup on Minikube
This folder contains everything needed to run a Tapis associate site on a single machine running Minikube.

## Requirements
- A publicly-accessible machine
- Docker + Minikube
- HAProxy

### 1. Generate SSL certs for your Tapis tenant domains
Before we begin, we first have to generate SSL certs for all of the tenant domains we plan to run on our associate site setup. This is a required step, and will enable our associate site's Tapis APIs to be accessible over HTTPS, instead of HTTP.

Run the following commands:

```bash
cd certs/certbot
./fetch_certs.sh -d <your 1st domain> -d <your 2nd domain> # -d tenant1.edu -d www.tenant1.edu -d tenant2.edu ...
./copy_certs.sh <your 1st domain> # tenant1.edu
```
Now, you should have a `cert.key` and `cert.pem` file inside the `./certs/` folder. Be sure to use these files in the next step (when `tapis-deployer` asks for the paths to the SSL certificate & private key for your tenant domains).

To renew the certs at a later time, run the following commands:
```bash
cd ./certs/certbot
./renew_certs.sh
./copy_certs.sh <your 1st domain>
```

### 2. Generate the k8s manifests for Tapis
In this step, you should generate the setup & configuration files for the Tapis associate site. To do this, follow the steps mentioned in the [tapis-deployer](https://github.com/tapis-project/tapis-deployer) repo. All of the generated files should be placed within a `./output/` subfolder inside this current folder. 

Once the **tapis-deployer** has been run, ensure that the following output files/folders exist (w.r.t this folder):
- `./output/raw_inputs_file.yml`
- `./output/deploygen/`
    - Inside this folder, you should see the `burnup` & `burndown` scripts for all necessary Tapis services, in addition to some other files.

### 3. Deploy Minikube-specific manifest files
The following command will create a `ClusterRole` and `ClusterRoleBinding` that will allow pods in the `default` namespace to perform various actions using k8s secrets. This is necessary for the Tapis-related pods to properly function.
```kubectl apply -f ./minikube_customizations/security.yaml```

### 4. Deploy the initial services to Minikube
This step will deploy the `proxy`, `vault`, and `skadmin` (security kernel admin) services on Minikube.

```bash
cd ./output/deploygen
./burnup init
```

### 5. Deploy the primary services to Minikube
Once the previous step is finished, deploy the `authenticator`, `tokens`, and `security kernel` services to Minikube using the following commands:

```bash
cd ./output/deploygen
./burnup primary_services
```

### 6. Start a tunnel for the `tapis-nginx` service running on Minikube
To access the Tapis services running in our cluster, we have to create a tunnel to the `tapis-nginx` service on our machine. To do this, run the following commands (in a separate terminal session):

```bash
minikube service --url tapis-nginx
```

In the output shown, you should see two forwarded ports. One of them will be for HTTP traffic and the other one will be for HTTPS traffic. To figure out which is which, try accessing them on `localhost` via HTTP.

### 7. Run HAProxy to make our Tapis services publicly accessible
Once you know the HTTP and HTTPS ports tunelling traffic to the `tapis-nginx` service running on Minikube, open the `./haproxy/config/haproxy.cfg` file and change the ports used for `127.0.0.1` (in the `backend http_backend` and `backend https_backend` sections) to use your corresponding HTTP and HTTPS ports instead.

Next, start HAProxy using the following command:

`haproxy -f ./haproxy/config/haproxy.cfg`

Your associate services should now be publicly accessible over HTTPS. One way to check would be to try going to the following URL in a browser:

<a href="https://(your domain)/v3/security/healthcheck">https://(your domain)/v3/security/healthcheck</a>

### 8. Retrive public keys and give them to the primary site provider (e.g., TACC)
Now that our associate site services are running, the final step is to retrieve the generated public keys and give them to our primary site provider (which may be TACC, if you will be connecting to their primary site's Tapis API).

You can retrieve your associate site's public keys using the following commands:

```bash
cd ./output/deploygen
./burnup get_public_keys
```