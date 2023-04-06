#!/usr/bin/env bash
# This Script Performs an apt update
# Installs nginx web server
# adds some content to the landing page
# Finally Starts the nginx service

apt-get -y update
apt-get install -y nginx

# create tree directory structure
mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared/test/

# populate sample index file with content


echo -e "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html
rm -rf /data/web_static/current
ln -s /data/web_static/releases/test /data/web_static/current

# Assign ownership of /data directory and subdirectories to the user ubuntu & group ubuntu
chown -R ubuntu:ubuntu /data

# configure nginx Aliasing
# Resource: https://www.youtube.com/watch?v=8P2r0xSXk28
# shellcheck disable=SC2016
echo -e ' server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;

        index index.html index.htm index.nginx-debian.html;

        server_name _;
        add_header X-Served-By $hostname;

        location /current{
                root /data/web_static/;
        } # in above the value of location is appended to the root to be /home/tony/hello
        #http://localhost/hello/index.html

        # alias directive
        location  /hbnb_static {
                alias /data/web_static/current;
        }

        location / {
          try_files $uri $uri/ =404;
        }

        location = /redirect_me {
          return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
        }
      }
' > /etc/nginx/sites-enabled/default

#Custom_header='add_header X-Served-By $hostname;'
#sed -i "/^\s*server_name _*/a $Custom_header" /etc/nginx/sites-enabled/default

/etc/init.d/nginx reload
/etc/init.d/nginx restart
