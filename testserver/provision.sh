#!/usr/bin/env bash

echo Installing Python
echo -----------------
sudo apt-get update
sudo apt-get install python python-pip -y

echo Installing Celery
echo -----------------
sudo pip install celery 

cd /vagrant
cd testserver
echo RabbitMQ Server Starting 
echo --------------------------
sudo -u vagrant celery -A tasks worker --queue=testing &
echo secceded


cd /vagrant
mkdir tsparticipants
mkdir tsprograms