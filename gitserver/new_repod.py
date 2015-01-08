import os
from pymongo import Connection

cn = Connection()
db1 = cn.vrdbautotest

while(True):
    coll=db1.contestant.find()
    for c in coll:
        user1=c["username"]+".git"
        print user1
        directory = '/opt/git'
        ls = os.listdir(directory)
        print ls
        for u in ls :
            if( u == user1):
                print "ok"
            else: 
                print "notok"
                os.chdir("/opt/git")
                cmnd="mkdir "+user1
                print cmnd
                os.system(cmnd)
                os.system("ls")
                os.chdir(user1)
                os.system("git init")
                os.system("chown -R www-data.www-data .")
