https://atomstar.tweakblogs.net/blog/16983/reading-out-tp-link-hs110-on-linux-raspberry-pi

# Preliminaries
- plug in
- potentially reset
- Connect to smartplug wifi hotspot

# Get initial information:
    tplink-smartplug-master/tplink_smartplug.py -t 192.168.0.1 -c info

# Set cloud address to dummy
    tplink-smartplug-master/tplink_smartplug.py -t 192.168.0.1 -j '{"cnCloud":{"set_server_url":{"server":"poop.com"}}}'

err_code:0 means NO error

# Connect to wifi
    tplink-smartplug-master/tplink_smartplug.py -t 192.168.0.1 -j '{"netif":{"set_stainfo":{"ssid":"HolyRomanEmperors","password":"jeffstoopicky","key_type":3}}}'


# Set static IP for smartplug in router

# Read out data

    tplink-smartplug-master/tplink_smartplug.py -t 192.168.2.105 -c energy

    
    
# download SCE
    sudo apt install chromium-chromedriver
    sudo apt install xserver-xephyr
    sudo apt install xvfb
    pip install selenium-wire


    
## For plotting
    sudo apt install texlive-latex-extra
    sudo apt install cm-super
    sudo apt install dvipng/focal
    

# raspberry pyvirtualdisplay
## Packages
    sudo apt install python3-pandas 
    sudo apt install python3-sqlalchemy
    sudo apt install python3-pip
    sudo apt install python3-dropbox
    sudo apt install chromium-chromedriver
    sudo apt install nginx
    sudo apt install locate
    pip3 install selenium-wire
    
    
## webserver 

### Skeleton
    https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-server-blocks-virtual-hosts-on-ubuntu-16-04
    
    sudo apt install nginx
    sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/holyromanpv.duckdns.org
    sudo nano /etc/nginx/sites-available/holyromanpv.duckdns.org
    sudo ln -s /etc/nginx/sites-available/holyromanpv.duckdns.org /etc/nginx/sites-enabled    
    sudo nginx -t
    sudo systemctl restart nginx
    
    
### Config 
sudo nano /etc/nginx/sites-available/holyromanpv.duckdns.org

server {
        listen 8080;
        listen [::]:8080;

        root /var/www/holyromanpv/html;

        index index.html index.htm index.nginx-debian.html;

        server_name www.holyromanpv.duckdns.org holyromanpv.duckdns.org;

        location / {    
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri $uri/ =404;
        }

        # Disabling cache
        location ~* \.(jpg|pdf|jpeg)$ {
            expires -1;
        }
}


server {
        listen 8043 http2 default_server;
        listen [::]:8043 http2 default_server;

        root /var/www/holyromanpv/html;

        ssl_certificate /etc/letsencrypt/live/holyromanpv.duckdns.org/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/holyromanpv.duckdns.org/privkey.pem;

        gzip on;
        gzip_types
            image/*
            text/*
            text/csv;
        gunzip on;

        location ~* \.(jpg|pdf|jpeg)$ {
            expires -1;
        }

        ssl on;

}



    sudo mkdir -p /var/www/holyromanpv/html
    
    sudo ln -s /home/griessbaum/smartplug/www/index.html /var/www/holyromanpv/html/    
    sudo ln -s /home/griessbaum/smartplug/www/avg_prodcons.png /var/www/holyromanpv/html/
    sudo ln -s /home/griessbaum/smartplug/www/days.png /var/www/holyromanpv/html/
    sudo ln -s /home/griessbaum/smartplug/www/prodcons.png /var/www/holyromanpv/htm
    sudo ln -s /home/griessbaum/smartplug/www/production.png /var/www/holyromanpv/html/
    
    

## increase swap
    sudo dphys-swapfile swapoff
    sudo nano /etc/dphys-swapfile 
    
Change to: CONF_SWAPSIZE=500

    sudo dphys-swapfile setup
    sudo dphys-swapfile swapon
    

    
