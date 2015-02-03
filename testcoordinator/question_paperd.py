import os
from pymongo import MongoClient
import conf
from conf import db_host
import subprocess
import time

def mainloop():
    files = '/vagrant/starter-files/*' 
    db_host = os.environ.get('DB_HOST', 'mongodb://192.168.1.103:27017/')
    client=MongoClient(db_host)
    db=client.autotest
    direct=conf.participant_dir
    user_coll=db.contestant.find({'contestname':"VR_Auto_Test"},{'username':1,'_id':0,'password':1,'email':1})
    
    for user in user_coll:
        un=user['username']
        pswd=user['password']
        email=user['email']
        if os.path.isdir(os.path.join(direct,un)):
            print "omitted {} directory".format(un)
            continue
        subprocess.call('git config --global user.name "{}"'.format(un),shell=True,executable='/bin/bash')
        subprocess.call('git config --global user.email {}'.format(email),shell=True,executable='/bin/bash')
        cmnd="git clone http://"+un+":"+pswd+"@"+conf.git_host+"/git/"+un+".git"               
        subprocess.call(cmnd , shell=True, executable='/bin/bash', cwd=direct,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        print 'cloned {} successfully'.format(un+".git")
        copycmnd="cp -r %s %s" %(files,os.path.join(direct,un))	
        subprocess.call(copycmnd , shell=True, executable='/bin/bash',stdout=subprocess.PIPE,stderr=subprocess.PIPE)  
        subprocess.call("git add -A",shell=True, executable='/bin/bash',cwd=os.path.join(direct,un))
        commitcmnd='git commit -m '+'"comitting initial files"'
        print "Added questions for {} ".format(un)        
        subprocess.call(commitcmnd,shell=True, executable='/bin/bash',cwd=os.path.join(direct,un))
        subprocess.call("git push origin master", shell=True, executable='/bin/bash',cwd=os.path.join(direct,un),stdout=subprocess.PIPE,stderr=subprocess.PIPE)	
        print "pushed {} directory to origin".format(un)
        
        

# Python main routine to run the mainloop in a loop :-) 
# We have a minimum delay of 10 seconds between checks
# printing results for debugging purpose
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
