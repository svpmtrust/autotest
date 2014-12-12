#!/bin/bash

for l in `cat user_list.csv`
do
  u=$(echo $l|cut -f1 -d,)
  m=$(echo $l|cut -f2 -d,)
  echo Creating user $u with mail $m
  bash newuser.sh $u $m
  echo 
  echo
done

service apache2 restart
