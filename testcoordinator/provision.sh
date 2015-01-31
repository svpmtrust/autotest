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

echo creating Participants,mails,programs directories
echo -------------------------------------------------
cd /vagrant
mkdir mails
mkdir programs
mkdir participants


echo Installing git
echo --------------
sudo apt-get install git -y




echo configuring git
echo ---------------
sudo git config --global user.name "SujithKandamuri"
sudo git config --global user.email "ksnvsujith@gmail.com"
echo completed configuring git
echo -----------------------

echo Upstart the Test Coordinator
echo ----------------------------
cp /vagrant/testcoordinator/test-coordinator.Upstart.templ /etc/init/testcoordinator.conf
sudo service testcoordinator start

echo Running the QuestionPaper Deamon
echo --------------------------------
cp /vagrant/testcoordinator/question-paper.Upstart.templ /etc/init/questionpaper.conf
sudo service questionpaper start


