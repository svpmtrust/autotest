#!/usr/bin/env bash

echo Installing Python
echo -----------------
sudo apt-get update
sudo apt-get install python python-pip -y

echo Installing Celery..
echo -----------------
sudo pip install celery

echo Installing Pymongo..
echo ------------------
sudo pip install pymongo

echo creating Participants,programs directories
echo -------------------------------------------------
cd $1
mkdir programs
mkdir participants

echo Installing git
echo --------------
sudo apt-get install git -y

echo Installing javac..
echo --------------
sudo apt-get install default-jre -y

echo Installing java..
echo --------------
sudo apt-get install default-jdk -y

echo Upstart the Test Server
echo ----------------------------
echo env GITSERVER_ROOT=$1 > /etc/init/testserver.conf
echo env DB_HOST=$2 >> /etc/init/testserver.conf
echo env CONTEST_NAME=$3 >> /etc/init/testserver.conf
echo env GIT_HOST=$4 >> /etc/init/testserver.conf
echo ----------------------------
cat $1/testserver/test-server.Upstart.templ >> /etc/init/testserver.conf
sudo service testserver start

echo DONE
