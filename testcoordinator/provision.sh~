#!/usr/bin/env bash

echo Installing Python
echo -----------------
sudo apt-get update
sudo apt-get install python python-pip -y

echo Installing Pymongo
echo ------------------
sudo pip install pymongo

echo Installing Celery
echo -----------------
sudo pip install celery

pwd
cd /vagrant
pwd
cd testcoordinator/
pwd
ls
sudo -u vagrant celery -A testserver worker --queue=testing &
echo secceded

echo Upstart the Test Coordinator
echo ----------------------------
cp /vagrant/testcoordinator/test-coordinator.Upstart.templ /etc/init/testcoordinator.conf
sudo service testcoordinator start

echo Running the QuestionPaper Deamon
echo --------------------------------
cp /vagrant/testcoordinator/question-paper.Upstart.templ /etc/init/questionpaper.conf
sudo service questionpaper start

