import os
from pymongo import MongoClient
import conf
from conf import db_host
import subprocess
import conf
import os
import time

def mainloop():
    files = '../starter-files/*'
    db_host = os.environ.get('DB_HOST', 'mongodb://192.168.1.105:27017/')
    client=MongoClient(db_host)
    db=client.autotest
    os.system("cd ..")
    os.chdir("/participants")  
    user_coll=db.contestant.find({'contestname':"VR_Auto_Test"},{'username':1,'_id':0,'password':1,'email':1})
    for user in user_coll: 
        un=user['username']
        pswd=user['password']
        if os.path.isdir(os.path.join(direct, user)):
        	continue
    	subprocess.call(['git','clone',
                     "http://{u}:{p}@{h}/git/{u}.git".format(u=un, h=conf.git_host, p=pswd)],
                    cwd=direct)
    	subprocess.call('cp -r %s %s' % (files, un), shell=True)
    	subprocess.call(['git','add','.'], cwd=un)
    	subprocess.call(['git','commit','-m',"Commiting the initial files"], cwd=un)
        subprocess.call(['git','push','origin','master'], cwd=un)
        

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