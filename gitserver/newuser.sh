#!/bin/bash


# Check if the script is run as root
EUID=`id -u`
if [ $EUID -ne 0 ] ; then
  echo You must run this as root
  exit 1
fi

# Setup apache
cat > /etc/apache2/sites-enabled/$1 <<EOF
<Location /git/$1.git>
  AuthType Basic
  AuthName "Git for $1"
  AuthUserFile /etc/apache2/passwd.$1.git
  Require user $1
  AuthBasicProvider file
  Options +ExecCGI +FollowSymLinks
</Location>
EOF

# Pick a random password from the file
pwd=$(head -1 random_passwords)
sed '1d' random_passwords > random_password1
mv random_passwords1 random_passwords

htpasswd -bc /etc/apache2/passwd.$1.git $1 $pwd
htpasswd -b /etc/apache2/passwd.$1.git tester tester

echo $1,$pwd >> pwdlist

# Setup git repository
cd /opt/git
mkdir $1.git
cd $1.git
git init --bare
chown -R www-data.www-data .
