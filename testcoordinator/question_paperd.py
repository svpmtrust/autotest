import os
from pymongo import MongoClient
import conf
from conf import db_host
import subprocess
import time

def mainloop():
    files = '/vagrant/starter-files/*' 
    db_host = os.environ.get('DB_HOST', 'mongodb://192.168.1.100:27017/')
    client=MongoClient(db_host)
    db=client.autotest
    direct=conf.participant_dir
    user_coll=db.contestant.find({'contestname':"VR_Auto_Test"},{'username':1,'_id':0,'password':1,'email':1})
    print user_coll
    print direct
    for user in user_coll:
        un=user['username']
        pswd=user['password']
	print direct+un
        if os.path.isdir(os.path.join(direct,un)):
	    print os.path.join(direct,un)
            continue
        cmnd="git clone http://"+un+":"+pswd+"@"+conf.git_host+"/git/"+un+".git"
        print "cmnd", cmnd       
	subprocess.call(cmnd , shell=True, executable='/bin/bash', cwd=direct)
        copycmnd="cp -r %s %s" %(files,os.path.join(direct,un))
	print "copycmnd",copycmnd
        subprocess.call(copycmnd , shell=True, executable='/bin/bash')       
        subprocess.call("git add -A",shell=True, executable='/bin/bash',cwd=os.path.join(direct,un))
        commitcmnd='git commit -m '+'"comitting initial files"'
	print "commitcmnd",commitcmnd        
        subprocess.call(commitcmnd,shell=True, executable='/bin/bash',cwd=os.path.join(direct,un))
        subprocess.call("git push origin", shell=True, executable='/bin/bash',cwd=os.path.join(direct,un))
        
        

# Python main routine to run the mainloop in a loop :-) 
# We have a minimum delay of 10 seconds between checks
if __name__ == '__main__':
    while True:
        start_time=time.time()
        mainloop()
        exec_time = time.time()-start_time
        print exec_time
        
        if exec_time > 10:
            pass
        else:
            time.sleep(10-exec_time)
