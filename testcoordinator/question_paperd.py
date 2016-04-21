import os
from pymongo import MongoClient
import conf
from conf import db_host, root_dir, contest_name
import subprocess
import time


def copy_selected_questions():
    questions_for_contest=db.contest.find({'contestname': contest_name},{'_id':0,'questions':1})
    for i in questions_for_contest:
        x=i['questions']
    sq=list()
    for i in x.keys():
        sq.append(i)   
    cmd_to_run = "cp -r {root_dir}/starter-files/README.txt {root_dir}/selected_questions"
    subprocess.call(cmd_to_run.format(root_dir=root_dir), shell=True)
    
    cmd_to_run = "cp -r {root_dir}/starter-files/*.zip {root_dir}/selected_questions"
    subprocess.call(cmd_to_run.format(root_dir=root_dir), shell=True)
    
    for question in sq:
        print question
        cmd_to_run = "cp -r {root_dir}/starter-files/{question} {root_dir}/selected_questions"
        subprocess.call(cmd_to_run.format(root_dir=root_dir, question=question), shell=True)


def mainloop(db):
    try:
        files = '{}/selected_questions/*'.format(root_dir)
        direct=conf.participant_dir
        user_coll=db.contestant.find({'contestname': contest_name}, {'username': 1, '_id': 0, 'password': 1, 'email': 1})

        questions_for_contest=db.contest.find({'contestname': contest_name},{'_id':0,'questions':1})
        for i in questions_for_contest:
            x=i['questions']
        
        for user in user_coll:
            un=user['username']
            pswd=user['password']
            email=user['email']
            if os.path.isdir(os.path.join(direct,un)):
                print "omitted {} directory".format(un)
                continue
            questions_for_contest=db.contest.find({'contestname': contest_name},{'_id':0,'questions':1})
	    user=db.contestant.find_one({"username":un})
            user['questions'] = x.keys()
            db.contestant.save(user)
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
            print "pushing to origin"
            subprocess.call("git push origin master", shell=True, executable='/bin/bash',cwd=os.path.join(direct,un),stdout=subprocess.PIPE,stderr=subprocess.PIPE)    
            print "pushed {} directory to origin".format(un)
        
    except:
        subprocess.call("cd $GITSERVER_ROOT/testcoordinator")
        subprocess.call("python question_paperd.py >> /var/log/question-paper.log 2>&1")
        pass

# Python main routine to run the mainloop in a loop :-) 
# We have a minimum delay of 10 seconds between checks
# printing results for debugging purpose
if __name__ == '__main__':
    db_host = os.environ.get('DB_HOST', 'mongodb://192.168.1.101:27017/')
    client=MongoClient(db_host)
    db=client.autotest
    print os.getcwd()
    question_directory=os.path.isdir(os.path.join(root_dir, 'selected_questions'))
    if not question_directory:
        print "creating directory for contest questions"
        subprocess.call(["mkdir {}/selected_questions".format(root_dir)],shell=True)
        print "directory is created for contest questions.......copying questions"
        copy_selected_questions()

    while True:
        start_time=time.time()
        mainloop(db)
        exec_time = time.time()-start_time
        print exec_time
        
        if exec_time > 10:
            pass
        else:
            time.sleep(10-exec_time)
