#!/usr/bin/env bash

echo Installing python
echo -----------------
sudo apt-get install python python-pip -y
 
echo Installing pymongo
echo ----------------
sudo pip install pymongo

echo Installing puppet
echo -----------------
sudo apt-get update
sudo apt-get install puppet -y

echo Copying all the puppet scripts
echo ------------------------------
sudo cp -r $1/* /etc/puppet

echo Running puppet
echo --------------
sudo apt-get install python-software-properties -y
sudo add-apt-repository ppa:ondrej/apache2 -y
sudo apt-get update
cd /etc/puppet
sudo puppet apply -v gitserver/gitserver.pp

echo Running the New Repository Creation Deamon
echo ------------------------------------------
echo env GITSERVER_ROOT=$1 > /etc/init/newrepo.conf
echo env DB_HOST=$2 >> /etc/init/newrepo.conf
echo env CONTEST_NAME=$3 >> /etc/init/newrepo.conf
cat $1/gitserver/new-repod.upstart.templ >> /etc/init/newrepo.conf
sudo service newrepo start

echo Restart Apache2
echo ---------------
echo ServerName localhost > /etc/apache2/sites-enabled/servername.conf
sudo a2enmod rewrite
sudo service apache2 restart

