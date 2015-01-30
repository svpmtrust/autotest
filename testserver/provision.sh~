#!/usr/bin/env bash

echo Installing Python
echo -----------------
sudo apt-get update
sudo apt-get install python python-pip -y

echo Installing Celery
echo -----------------
sudo pip install celery 

pwd
cd /vagrant
pwd
cd testcoordinator/
ls
python project.py

echo Upstart the Test Server
echo ----------------------------
cp /vagrant/testserver/test-server.upstart.templ /etc/init/testserver.conf
sudo service testserver start



