#!/usr/bin/env bash

echo Installing Python
echo -----------------
sudo apt-get update
sudo apt-get install python python-pip -y

echo Installing Pymongo..
echo ------------------
sudo pip install pymongo

echo Installing Celery..
echo -----------------
sudo pip install celery

echo creating Participants,programs directories
echo -------------------------------------------------
cd $1
mkdir programs
mkdir participants

echo Installing git
echo --------------
sudo apt-get install git -y

echo Upstart the Test Coordinator
echo ----------------------------
echo env GITSERVER_ROOT=$1 > /etc/init/testcoordinator.conf
echo env DB_HOST=$2 >> /etc/init/testcoordinator.conf
echo env CONTEST_NAME=$3 >> /etc/init/testcoordinator.conf
echo env GIT_HOST=$4 >> /etc/init/testcoordinator.conf
cat $1/testcoordinator/test-coordinator.Upstart.templ >> /etc/init/testcoordinator.conf
sudo service testcoordinator start

echo Running the QuestionPaper Deamon
echo --------------------------------
echo env GITSERVER_ROOT=$1 > /etc/init/questionpaper.conf
echo env DB_HOST=$2 >> /etc/init/questionpaper.conf
echo env CONTEST_NAME=$3 >> /etc/init/questionpaper.conf
echo env GIT_HOST=$4 >> /etc/init/questionpaper.conf
cat $1/testcoordinator/question-paper.Upstart.templ >> /etc/init/questionpaper.conf
sudo service questionpaper start
