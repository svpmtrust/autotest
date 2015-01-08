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
		user=c["username"]+".git"
		print user
		user1="/opt/git/"+user
	  	print user1
	  	directory = user1
	  	ls = os.listdir(directory)
		#ls = os.listdir("/opt/git/exmp")
		print ls
	  	if not ls:
	    		#print "emptyy"
	   		os.chdir(user1)
	    		os.system("mkdir ttest")
	    		os.chdir("ttest")
	    		os.system("cp -f /vagrant/starter-files/* .")


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

