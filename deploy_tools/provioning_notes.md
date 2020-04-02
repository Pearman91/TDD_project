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

## Systemd service:
* in gunicorn-systemd.template.service replace *DOMAIN* with real domain name

## Folder structure:
* for each DOMAIN, corresponding repository is to be cloned into /home/luser/sites/DOMAIN 