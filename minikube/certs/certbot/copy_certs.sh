domain=$1
cp ./etc/letsencrypt/live/$domain/privkey.pem ../cert.key
cp ./etc/letsencrypt/live/$domain/fullchain.pem ../cert.pem