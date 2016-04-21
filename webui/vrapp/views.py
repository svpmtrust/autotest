import smtplib
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
import os
import hashlib
import time
from vrautotest.settings import db1, on_aws, BASE_DIR, DB_HOST, DB_NAME
import boto
import boto.cloudformation


# Create your views here.

#--------------SuperUser------------#

def superuser(request):
    contests=db1.contest.find()
    return render(request, 'superuser.html', {'contests':contests})

def deleteContest(request):
    cname=request.POST.get('cname')
    print(cname)
    db1.contest.remove({ "contestname" : cname })
    return HttpResponseRedirect('/superuser')

def addContest(request):
    cname=request.POST.get('contestname')
    organisation=request.POST.get('organisation')
    date=request.POST.get('date')
    status=request.POST.get('status')
    tnc=request.POST.get('tnc')
    approverrule=request.POST.get('approverrule')
    ta1un=request.POST.get('ta1un')
    ta1pswd=request.POST.get('ta1pswd')
    ta1pswd=hashlib.sha1(ta1pswd)
    ta1pswd=ta1pswd.hexdigest()
    ta1email=request.POST.get('ta1email')
    ta2un=request.POST.get('ta2un')
    ta2pswd=request.POST.get('ta2pswd')
    ta2pswd=hashlib.sha1(ta2pswd)
    ta2pswd=ta2pswd.hexdigest()
    ta2email=request.POST.get('ta2email')
    tc1un=request.POST.get('tc1un')
    tc1pswd=request.POST.get('tc1pswd')
    tc1pswd=hashlib.sha1(tc1pswd)
    tc1pswd=tc1pswd.hexdigest()
    tc1email=request.POST.get('tc1email')
    pa1un=request.POST.get('pa1un')
    pa1pswd=request.POST.get('pa1pswd')
    pa1pswd=hashlib.sha1(pa1pswd)
    pa1pswd=pa1pswd.hexdigest()
    pa1email=request.POST.get('pa1email')
    pa2un=request.POST.get('pa2un')
    pa2pswd=request.POST.get('pa2pswd')
    pa2pswd=hashlib.sha1(pa2pswd)
    pa2pswd=pa2pswd.hexdigest()
    pa2email=request.POST.get('pa2email')
    db1.contest.insert({
            "contestname" : cname ,
            "organisation" : organisation ,
            "date" : date ,
            "status" : status ,
            "tnc" : tnc ,
            "approverrule" : approverrule ,
            "testadmin" : {
                            ta1un : {
                                    "password" : ta1pswd,
                                    "emaill" : ta1email
                            },
                            ta2un : {
                                    "password" : ta2pswd,
                                    "emaill" : ta2email
                            }
                    },
             "testcreator" : {
                            tc1un : {
                                    "password" : tc1pswd,
                                    "emaill" : tc1email
                            }
                    },
              "participantapprover" : {
                            pa1un : {
                                    "password" : pa1pswd,
                                    "emaill" : pa1email
                            },
                            pa2un : {
                                    "password" : pa2pswd,
                                    "emaill" : pa2email
                            }
                    },
                "questions":{},
                "questions_criteria":{}
            })
    return HttpResponseRedirect('superuser')

def checkContestName(request):
    contestname=request.GET.get("contestname")
    con = db1.contest.find_one({'contestname': contestname })
    if not con:
        return HttpResponse("Valid")
    else:
        return HttpResponse("InValid")

#------------Home---------------#

def home(request):
    try:
        del request.session['contestname']
        del request.session['username']
    except KeyError:
        pass
    return render(request, 'home.html', {})  

def registration(request):
    cname=db1.contest.find({},{'contestname' : 1 , '_id' : 0})
    return render(request, 'registration.html', {'cname':cname})

def checkUserName(request):
    #contestname=request.GET.get("contestname")
    username=request.GET.get("username")
    con = db1.contestant.find_one({'username':username })
    if not con:
        return HttpResponse("Valid")
    else:
        return HttpResponse("InValid")

def regisuccess(request):
    cn = request.POST.get('contestname')
    un = request.POST.get('username')
    name = request.POST.get('name')
    email = request.POST.get('email')
    pswd = request.POST.get('pass')
    if not pswd:
        '''return HttpResponse("ERROR: You need a password to register")'''
        return render(request, 'errorpage.html', {'emessage':"You need a password to register.. Please Register Again"})
    a = hashlib.sha1(pswd)
    hpswd = a.hexdigest()
    d=db1.contest.find_one({"contestname":cn})
    if d["approverrule"] == "0" :
        apstatus="1"
    else:
        apstatus="0"
    user={"contestname":cn, "name":name, "username":un, "email":email, "password":hpswd,
          "approved_status":apstatus,
          "approved_by":[],
          "status":"active",
          "questions":[]
          }
    dbr = db1.contestant.insert(user)
    if dbr :
        to = email
        gmail_user = 'techcontest2015@gmail.com'
        gmail_pwd = 'aviso2015'
        smtpserver = smtplib.SMTP("smtp.gmail.com",587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(gmail_user, gmail_pwd)
        header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Registration Successfull \n'
        msg = header + '\n Thank you for Your Registration to ' + cn + '\n ' + ' UserName : ' +  un + '\n Password : ' + pswd + '\n \n'
        smtpserver.sendmail(gmail_user, to, msg)
        smtpserver.close()
        return HttpResponseRedirect('loginform')
    else :
        '''return HttpResponse("ERROR: Sorry Please Register Again")'''
        return render(request, 'errorpage.html', {'emessage':"Sorry Something went wrong.. Please Register Again"})

#---------Login----------#

def loginform(request):
    try:
        del request.session['contestname']
        del request.session['username']
        return render(request, 'errorpage.html', {'emessage':"Sorry Session Expired :("})
    except KeyError:
        pass
    cname=db1.contest.find({},{'contestname' : 1 , '_id' : 0})
    return render(request, 'loginform.html', {'cname':cname})

def logout(request):
    try:
        del request.session['contestname']
        del request.session['username']
    except KeyError:
        pass
    cname=db1.contest.find({},{'contestname' : 1 , '_id' : 0})
    return render(request, 'loginform.html', {'cname':cname})

def loginvalidate(request):
    usertype = request.POST.get('usertype')
    contestname = request.POST.get('contestname1')
    username = request.POST.get('username1')
    password = request.POST.get('password1')
    a=hashlib.sha1(password)
    password=a.hexdigest()
    request.session['contestname'] = contestname
    request.session['username'] = username
    if(usertype == "contestant"):
        coll=db1.contestant.find_one({'contestname':contestname,'username':username,'password':password})
        if not coll:
            return HttpResponse("error")      
        else:
            return HttpResponseRedirect('/contestanthome')
    if(usertype == "testadmin"):
        coll=db1.contest.find_one({"contestname":contestname})
        if username in coll["testadmin"].keys():
            if password==coll["testadmin"][username]["password"]:
                return HttpResponseRedirect('/testadminhome')
        else:
            return HttpResponse("error")
    if(usertype == "testcreator"):
        coll=db1.contest.find_one({"contestname":contestname})
        if username in coll["testcreator"].keys():  
            if password==coll["testcreator"][username]["password"]:
                return HttpResponseRedirect('/testcreatorhome')               
            else:
                return HttpResponse("error")
        else:
            return HttpResponse("error")
    if(usertype == "participantapprover"):
        coll=db1.contest.find_one({"contestname":contestname})
        if username in coll["participantapprover"].keys():
            if password==coll["participantapprover"][username]["password"]:
                return HttpResponseRedirect('/participantapproverhome')
        else:
            '''return HttpResponse("error")'''
            return render(request, 'errorpage.html', {'emessage':"Sorry Invalid Login Details :("})
            

#------------Contestant Home------------#
def contestanthome(request):
    contestname = request.session['contestname']
    username = request.session['username']
    coll = db1.contestant.find_one({"username":username})
    password=coll["password"]
    programs = db1.submissions.find({'user_name': username})
    scores=db1.scores.aggregate([
		     { "$match": 
			{"$and":[{"contestname": contestname } ]}},
                     { "$group": { "_id": "$user_name", "total": { "$sum": "$score" } } },
                     { "$sort": { "total": -1 } }
                   ])
    #for i in scores:
    #    scores = i['result']
    scores=scores["result"]
    rank=0
    userscores=[]
    totalscore=0
    for i,u in enumerate(scores) :
        user_name=u["_id"]
        total=u["total"]
        userscores.append({'username':user_name , 'total':total})
    for i,u in enumerate(scores) :
        if u["_id"] == username :
            rank = (i+1)
            totalscore=u["total"]
    contest_data = db1.contest.find_one({"contestname":contestname},{"_id":0, "status": 1, "git_ip": 1})
    #nor_submissions=db1.submissions.find([{"$match"{"username":username},"$group":{"_id":"$programname","no_of_sub":{"$sum":1}}).count()
    conteststatus = contest_data['status']
    git_address = contest_data.get('git_ip', None)
    return render(
        request, 'contestanthome.html',
        {
            'cname': contestname,
            'username': username,
            'password': password,
            'cstatus': conteststatus,
            'programs': list(programs),
            'scores': list(userscores),
            'git_address': git_address,
	        'totalscore': totalscore,
	        'rank':rank
        }
    )

'''
def submissions(request):
    c = Connection()
    db1 = c.autotest
    contestname = request.session['contestname']
    username = request.session['username']
    submissions = db1.submissions.find({'username':username})
    return render(request, 'contestanthome.html', {'cname': contestname ,'username':username , 'submissions':submissions})
'''
#------------TestAdmin Home------------#
def testadminhome(request):
    contestname = request.session['contestname']
    username = request.session['username']
    contest_data = db1.contest.find_one({"contestname":contestname},{"_id":0, "status": 1, "git_ip": 1})
    conteststatus = contest_data['status']
    git_address = contest_data.get('git_ip', None)
    users=db1.contestant.find({'contestname':contestname})
    scores=db1.scores.aggregate([
		     { "$match": 
			{"$and":[{"contestname": contestname } ]}},
                     { "$group": { "_id": "$user_name", "total": { "$sum": "$score" } } },
                     { "$sort": { "total": -1 } }
                   ])
    #for i in scores:
    #    scores = i['result']
    scores=scores["result"]
    userscores=[]
    for i,u in enumerate(scores) :
        user_name=u["_id"]
        total=u["total"]
	sub=db1.submissions.find({'user_name':user_name}).count()
	programs = db1.scores.find({'user_name':user_name}).count()
	userscores.append({'username':user_name , 'total':total , 'submissions':sub , 'programs':programs})
    return render(request, 'testadminhome.html', 
                  {'cname': contestname ,
                   'username':username ,
                   'scores': list(userscores),
                   'cstatus': conteststatus,
                   'git_address': git_address
                   })
    
def puppetrun(request):
    cn = request.session['contestname']
    cll=db1.contest.find_one({'contestname':cn},{'status':1,'_id':0})
    st=cll["status"]
    if(st == "Not Started"):
        print "ON_AWS is ::::::::::::",on_aws
        if on_aws:
            # TODO: Ideally we should ask celery to launch this in the background

            # Launch the AWS Cloud Formation Stack
            stack_name = cn.replace('_', '-')
            cf = boto.cloudformation.connect_to_region("ap-southeast-1")
            with file(os.path.join(BASE_DIR, "..", "contest_setup.cf")) as fp:
                stack_id = cf.create_stack(
                    stack_name=stack_name, template_body=fp.read(),
                    parameters=[
                        # TODO: Make the KeyName parameterized
                        ("KeyName", "hiring-keys"),
                        ("DBHost", DB_HOST),
                        ("DBName", DB_NAME),
                        ("ContestName", cn)
                    ]
                )
            # Get the IP Address from the outputs
            for x in range(60):
                stack_data = cf.describe_stacks(stack_name_or_id=stack_name)
                if len(stack_data) > 0:
                    our_stack = stack_data[0]
                    if our_stack.stack_status in ["CREATE_IN_PROGRESS",
                                                  "UPDATE_IN_PROGRESS"]:
                        pass
                    elif our_stack.stack_status in ("CREATE_COMPLETE",
                                                    "UPDATE_COMPLETE"):
                        outputs = dict((x.key, x.value) for x in our_stack.outputs)
                        git_ip = outputs["GitServerAddress"]
                        break
                    else:
                        raise Exception('Unable to create the stack. Check AWS')
                time.sleep(5)
            else:
                raise Exception("Timeout in creating the AWS stack")

            db1.contest.update({'contestname':cn},
                               {"$set":{
                                   'status':"Started",
                                   'git_ip': git_ip}
                               })
        else:
            os.system("cd ..")
            os.system("ls")
            os.system("vagrant up")
            db1.contest.update({'contestname':cn},
                               {"$set":{
                                   'status':"Started",
                                   'git_ip': "192.168.1.101"}
                               })
        return HttpResponse(str(git_ip))
    else:
        return HttpResponse(str("Contest Already Started"))

def puppetstop(request):
    cn = request.session['contestname']
    cll=db1.contest.find_one({'contestname':cn},{'status':1,'_id':0})
    st=cll["status"]
    if(st == "Started"):
        db1.contest.update({'contestname':cn},{"$set":{'status':"Finished"}})
        os.system("vagrant stop")
        return HttpResponse(str("Contest Stopped"))

def deactivateuser(request):
    un = request.POST.get("names")
    db1.contestant.update({'username':un},{"$set":{'status':"Deactivate"}})
    return HttpResponseRedirect('/testadminhome') 

#------------TestCreator Home------------#
def testcreatorhome(request):
	contestname = request.session['contestname']
	username = request.session['username']
	problems=db1.problemsrepository.find()
	dt=db1.contest.find_one({'contestname':contestname})
	date=dt["date"] 
	return render(request, 'testcreatorhome.html',
	{'cname': contestname ,'username':username,'date':date ,'problems':problems})       

def createquestionpaper(request):
    contestname = request.session['contestname']
    ques=json.loads(request.GET.get("names"))
    flags=json.loads(request.GET.get("flags"))
    coll=db1.contest.find_one({"contestname":contestname})
    easy=request.GET.get("easy")
    medium=request.GET.get("medium")
    hard=request.GET.get("hard")
    coll["questions_criteria"]={"easy":easy,
                                "medium":medium,
                                "hard":hard}
    for i in ques:
    	if i in flags:
    		coll["questions"].update({i:1})
    	else:
    		coll["questions"].update({i:0})
    db1.contest.save(coll)
    return HttpResponse("created")
     
#------------ParticipantApprover Home------------#    
def participantapproverhome(request):
    contestname = request.session['contestname']
    username = request.session['username']
    sname=request.GET.get("patype")
    contestants=db1.contestant.find({'contestname':contestname})
    pa=db1.contest.find({'contestname':contestname},{'participantapprover':1})
    for i in pa:
        tc=i["participantapprover"]
    pa=list()
    for i in tc.keys():
        pa.append(i)
    if(sname=="eligible"):
        contestants=db1.contestant.find({'contestname':contestname,"approved_status":"1"})
    elif(sname=="approve"):
        contestants=db1.contestant.find({'contestname':contestname,"approved_status":"0","approved_by":{"$ne":sname}})
    else:
        contestants=db1.contestant.find({'contestname':contestname ,"approved_by":{"$in":[sname]}})
    return render(request, 'participantapproverhome.html', 
	{'contestants':contestants ,'cname':contestname ,'username':username,'pa1':pa[0],'pa2':pa[1]})    
    
def approve(request):
    users=json.loads(request.GET.get("names"))
    contestname = request.session['contestname']
    username = request.session['username']
    contest=db1.contest.find_one({'contestname':contestname},{"approverrule":1,"_id":0}) 
    crule=int(contest["approverrule"])
    print(crule)
    print(contest) 
    for u in users:
        print(u)
        cont=db1.contestant.find_one({"contestname":contestname,"username":u})
        cont["approved_by"].append(username)
        if(crule >= len(cont["approved_by"])):
            cont["approved_status"]="1"
        db1.contestant.save(cont)
    return HttpResponse("Valid")
