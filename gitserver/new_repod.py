import os
# import conf
# from conf import db_host
from pymongo import MongoClient
import subprocess
import time
import traceback


def mainloop(client):
    try:
        contest_name = os.environ.get('CONTEST_NAME', None)
        if contest_name is None:
            raise Exception('No Contest Name Provided')
    
        db=client.autotest
        user_coll=db.contestant.find(
            {'contestname':contest_name}, {'username':1,'_id':0,'password':1,'email':1})
        for user in user_coll: 
            un=user['username']
            p=user['password']
            e=user['email'] 
            user1=un+".git"
            directory = '/opt/git'
            ls = os.listdir(directory)
            if user1 in ls :
                continue
            cmnd='sh newuser.sh '+un+' '+p+' '+e
            subprocess.Popen(cmnd , shell=True, executable='/bin/bash')

    except:
        #subprocess.call("cd $GITSERVER_ROOT/gitserver")
        #subprocess.call("python new_repod.py >> /var/log/gitserver.log 2>&1")
        print "Unable to run the main loop"
        traceback.print_exc()
        pass
        
# Python main routine to run the mainloop in a loop :-) 
# We have a minimum delay of 10 seconds between checks
if __name__ == '__main__':
    db_host = os.environ.get('DB_HOST', 'mongodb://192.168.1.101:27017/')
    client=MongoClient(db_host)
    while True:
        start_time=time.time()
        mainloop(client)
        exec_time = time.time()-start_time
        print exec_time        
        if exec_time > 10:
            pass
        else:
            time.sleep(10-exec_time)
