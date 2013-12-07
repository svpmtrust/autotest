#!/bin/bash


# Check if the script is run as root
EUID=`id -u`
if [ $EUID -ne 0 ] ; then
  echo You must run this as root
  exit 1
fi

# Add the user and set password
useradd $1
passwd $1 <<EOF
$1
$1
EOF

# Setup apache
cat > /etc/apache2/sites-enabled/$1 <<EOF
<Location /git/$1.git>
  DAV on
  AuthType Basic
  AuthName "Git for $1"
  AuthUserFile /etc/apache2/passwd.$1.git
  Require user $1
</Location>
EOF

htpasswd -bc /etc/apache2/passwd.$1.git $1 $1
htpasswd -b /etc/apache2/passwd.$1.git tester tester

# Setup git repository
cd /opt/git
mkdir $1.git
cd $1.git
git init --bare
chown -R www-data.www-data .
