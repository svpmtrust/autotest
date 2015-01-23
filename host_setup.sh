echo Installing packages
sudo apt-get install vagrant virtualbox mongodb rabbitmq-server

echo Populating Test Data
mongodbsetting=$(grep '"mongodb"' settings.json || grep '"mongodb"' default_settings.json)
mongodb=echo $mongodbsetting | sed -r 's/^.*"([^"]*)"[,\r\n ]*$/\1/'

# TODO: Remove hardcoded autotest and use the sed above to find details
mongo autotest testdata/contest.js
mongo autotest testdata/problemrepository.js

# Install the required vagrant box
vagrant box add precise64 http://files.vagrantup.com/precise64.box
