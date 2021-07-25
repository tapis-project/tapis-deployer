# misc admin stuff

## nginx proxy config gen

- Create the cert bundle from the cert and intermediates, e.g.:
 
    cat /etc/pki/tls/certs/tacc.develop.tapis.io.cer /etc/pki/tls/certs/IncommonIntermediateBundle.cer > /etc/pki/tls/certs/tacc.develop.tapis.io.bundle.pem

- Put that and the domain in proxy.json.
- Run `genproxyconfig`
