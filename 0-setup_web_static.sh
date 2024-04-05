#!/usr/bin/env bash
# Script that sets up web servers from the deployment of web_static.

# install nginx if not exists
apt update
apt install nginx -y

# create necessary directories and indes file
mkdir -p /data/web_static/releases/test/
if [ ! -d "/data/web_static/shared/" ]; then
    mkdir /data/web_static/shared/
fi
touch /data/web_static/releases/test/index.html
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# create a symbolik link
link_path="/data/web_static/current"
release_path="/data/web_static/releases/test/"
if [ -L "$link_path" ]; then
        rm "$link_path"
fi
ln -s "$release_path" "$link_path"

# give recursive ownership for the data directory
chown -R ubuntu:ubuntu /data/

# updating the nginx configuration
sed -i '57i\\n\tlocation \/hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# restart web server
service nginx restart

