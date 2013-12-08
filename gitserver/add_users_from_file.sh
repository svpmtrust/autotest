#!/bin/bash

for x in `cut -f1 -d',' user_list.csv`
do
  echo Creating user $x
  echo ----------------
  bash newuser $x
  echo 
  echo
done
