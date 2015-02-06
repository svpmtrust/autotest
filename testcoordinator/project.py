import subprocess
import os
import conf
from conf import participant_dir
import xml.etree.ElementTree as ET
import time
from pymongo import MongoClient
import shlex
import timed_execution
import json
from celery import Celery
import tasks

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
                previous[y] = subprocess.check_output(['/usr/bin/git','log','-1','--oneline',y],cwd=direct)
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
    print conf.db_host
    client = MongoClient(conf.db_host)
    db = client.autotest
    col_submissions=db.submissions
    col_scores=db.scores
    result={}#creating empty dict for results
    for user,programname in listofParticipants():
        if user not in result:
            result.update({"user":user})#creating a new tupple in res with no values
            result.update({"programname":programname}) 
        program_dir=conf.participant_dir+user+'/'+programname #getting program code into program
        program_name=conf.program_dir+programname+'.xml'#getting program code  xml into program
        # Check if this programis something we support
        if not os.path.isfile(program_name): 
            col_submissions.save({
                    "user_name":user,
                    "program":programname,
                    "program_result":'INVALID PROGRAM',
                    "test_case_result":[None,None,None],
                    "time":time.time(),
                })
            continue
        submission = tasks.progtest.apply_async(args=(user, programname), queue='testing')
        submission = submission.get()
        print "==> Saving submission record in the DB, after execution <=="
        col_submissions.save({
            "user_name":submission["user"],
            "program":submission["programname"],
            "program_result":submission["progstatus"],
            "score":submission["score"],
            "test_case_result":submission["description"],
                  "time":time.time()
        })

    sccoll=db.scores.find_one({"username":submission["user"],"program":submission["program"]})
    if sccoll == None and submission["score"] == 0:
       pass        
    elif sccoll == None and submission["score"] > 0:      
        db.scores.insert({"user_name":submission["user"],"program":submission["programname"],"score":submission["score"]})
    elif sccoll!=None and submission["score"] == 0:
        db.scores.remove({"user_name":submission["user"],"program":submission["programname"]})     
    elif submission["score"] > sccoll["score"] or submission["score"] < sccoll["score"]:
       sccoll["score"]=submission["score"] 
       db.scores.save(sccoll)







        
'''        # If the user gets some score, update the score collection with latest
        # information
        if your_score:
            current_score = col_scores.find_one({'user_name':user})
            if not current_score:
                current_score = {
                    'user_name': user,
                    'programs': {}
                }
            current_score['programs'][programname] = {
                    'status': submission["progstatus"],
                    'score': submission["score"]
                    'status': progstatus,
                    'score': your_score

            }
            col_scores.save(current_score)
            progs = current_score['programs']
            total_score = sum(progs[x]['score'] for x in progs)
            result[user].insert(0, "YOUR NEW SCORE IS %s" % str(total_score))
'''

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
