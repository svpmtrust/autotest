import os
#import conf
from conf import db_host
from pymongo import MongoClient
import subprocess
import time

def mainloop(): 
    db_host = os.environ.get('DB_HOST', None)
    client=MongoClient(db_host)
    db=client.autotest
    user_coll=db.contestant.find({},{'username':1,'_id':0,'password':1,'email':1})
    for user in user_coll: 
        un=user['username']
        p=user['password']
        e=user['email'] 
        user1=c["un"]+".git"
        directory = '/opt/git'
        ls = os.listdir(directory)
        if user1 in ls :
           continue
	cmnd='sh newuser.sh '+un+' '+p+' '+e
       	subprocess.Popen(cmnd , shell=True, executable='/bin/bash')


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

