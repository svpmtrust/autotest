import subprocess
import os
import conf
from conf import participant_dir
from conf import db_host
import xml.etree.ElementTree as ET
import time
from pymongo import MongoClient
import shlex
import timed_execution
import json
from celery import Celery
import testserver

def listofParticipants():
    """ This method will go through each user in the participant
    directory and looks for changes for the repository
    corresponding to each user.  
    
    Yields the username, and the subdirectory that changed as a
    tuple.
    """
    dirs1 = os.listdir(conf.participant_dir)
    for user in dirs1:
        direct=participant_dir + user + '/'
        previous={}
        print "Checking for user %s" % user
        for y in os.listdir(direct):
            if os.path.isdir(direct+'/'+y) and y[0] !='.':
                previous[y] = subprocess.check_output(['/usr/bin/git',
                                                 'log','-1',
                                                 '--oneline',y],
                                                cwd=direct)
        subprocess.call(['/usr/bin/git', 'reset', '--hard', 'HEAD'], cwd=direct)
        subprocess.call(['/usr/bin/git', 'clean',  '-d',  '-fx', '""'], cwd=direct)
        subprocess.call(['/usr/bin/git', 'pull', '-s', 'recursive', '-X', 'theirs'], cwd=direct)

        for y in os.listdir(direct):
            if os.path.isdir(direct+'/'+y) and y[0] !='.':
                after = subprocess.check_output(['/usr/bin/git',
                                                 'log','-1',
                                                 '--oneline',y],
                                                cwd=direct)
                if y not in previous or previous[y] != after:
                    yield user,y
def mainloop():
    """ This is the main driver program to look for changes and
    run tests, save the results and send mails for iteration.
    """
    client = MongoClient(conf.db_host)
    db = client.autotest
    col_submissions=db.submissions
    col_scores=db.scores
    for user,programname in listofParticipants():
        result = testserver.results.apply_async(args=(user, programname), queue='testing')
      if(result[2] == 1):  
        col_submissions.save({
                    "user_name":user,
                    "program":programname,
                    "program_result":'INVALID PROGRAM',
                    "test_case_result":[None,None,None],
                    "time":time.time(),
                })
        continue
      else:
               
        print "==> Saving submission record in the DB, after execution <=="
        col_submissions.save({
            "user_name":user,
            "program":programname,
            "program_result":result[2],
            "test_case_result":[result[3],result[4],result[5]],
            "time":time.time()
        })
        
        # If the user gets some score, update the score collection with latest
        # information
        if your_score:
            current_score = col_scores.find_one({'user_name':user})
            if not current_score:
                current_score = {
                    'user_name': user,
                    'programs': {}
                }
            current_score['programs'][programname] = {
                    'status': progstatus,
                    'score': result[6]
            }
            col_scores.save(current_score)
            progs = current_score['programs']
            total_score = sum(progs[x]['score'] for x in progs)
            result[user].insert(0, "=======================================")
            result[user].insert(0, "YOUR NEW SCORE IS %s" % str(total_score))
  


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

