docker run -p 80:80 -p 443:443 -it --rm \
            -v "$(pwd)/etc/letsencrypt:/etc/letsencrypt" \
            -v "$(pwd)/lib/letsencrypt:/var/lib/letsencrypt" \
            certbot/certbot \
            certonly \
            --standalone \
            $*