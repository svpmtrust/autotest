import os
from pymongo import Connection
import conf
from conf import db_host

def mainloop():
    cn = Connection()
    db1 = cn.autotest
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

