Provisionig a new site
========================

## Required:
* nginx
* Python 3.6
* virtualenv + pip
* Git

## on Ubuntu:
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install nginx git python36 python3.6-venv
    
## Nginx virtual host config:
* in nginx.template.conf replace *DOMAIN* with real domain name
* rename the template it to *DOMAIN*
* save it as */etc/nginx/sites-available/<*DOMAIN*>*
* create symlink to the previous file in */etc/nginx/sites-enabled/<*DOMAIN*>*

## Systemd service:
* in gunicorn-systemd.template.service replace *DOMAIN* with real domain name
* rename the template to *DOMAIN.service*
* save it as */etc/systemd/system/<*DOMAIN.service*>* and reload systemctl daemon
* then you can enable it and start it

## Folder structure:
* for each DOMAIN, corresponding repository is to be cloned into /home/luser/sites/DOMAIN 