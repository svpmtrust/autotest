import smtplib
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from pymongo import Connection
import json
import os
import hashlib
#from celery.worker.job import Request
from vrautotest.settings import db1

# Create your views here.

#--------------SuperUser------------#

def superuser(request):
    contests=db1.contest.find()
    return render(request, 'superuser.html', {'contests':contests})

def deleteContest(request):
    cn=Connection()
    db1=cn.autotest
    cname=request.POST.get('cname')
    print(cname)
    db1.contest.remove({ "contestname" : cname })
    return HttpResponseRedirect('/superuser')

def addContest(request):
    cn=Connection()
    db1=cn.autotest
    cname=request.POST.get('contestname')
    cname=cname.replace(" ","_")
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
    cn=Connection()
    db1=cn.autotest
    contestname=request.GET.get("contestname")
    contestname=contestname.replace(" ","_")
    con = db1.contest.find_one({'contestname': contestname })
    if not con:
        return HttpResponse("Valid")
    else:
        return HttpResponse("InValid")


#------------Home---------------#

def home(request):
    return render(request, 'home.html', {})  

def registration(request):
    cn=Connection()
    db1=cn.autotest
    cname=db1.contest.find({},{'contestname' : 1 , '_id' : 0})
    return render(request, 'registration.html', {'cname':cname})

def checkUserName(request):
    cn=Connection()
    db1=cn.autotest
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
    a=hashlib.sha1(pswd)
    hpswd=a.hexdigest()
    c = Connection()
    db1 = c.autotest
    d=db1.contest.find_one({"contestname":cn})
    if d["approverrule"] == "0" :
        apstatus="1"
    else:
        apstatus="0"
    user={"contestname":cn,"name":name,"username":un,"email":email,"password":hpswd,
          "approved_status":apstatus,
          "approved_by":[],
          "status":"active",
          "questions":[]
          }
    db1.contestant.insert(user)
    return render(request,'regisuccess.html',{})

#---------Login----------#

def loginform(request):
    cn=Connection()
    db1=cn.autotest
    cname=db1.contest.find({},{'contestname' : 1 , '_id' : 0})
    return render(request, 'loginform.html', {'cname':cname})  

def logout(request):
    try:
        del request.session['contestname']
        del request.session['username']
    except KeyError:
        pass
    return HttpResponseRedirect('/loginform')

def loginvalidate(request):
    usertype = request.POST.get('usertype')
    contestname = request.POST.get('contestname')
    username = request.POST.get('username')
    password = request.POST.get('password')
    a=hashlib.sha1(password)
    password=a.hexdigest()
    cn = Connection()
    db1 = cn.autotest 
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
            return HttpResponse("error")

#------------Contestant Home------------#
def contestanthome(request):
    contestname = request.session['contestname']
    username = request.session['username']
    c=Connection()
    db1=c.autotest
    programs = db1.submissions.find({'user_name':username})
    scores=db1.scores.find()
    #lb=db1.submissions.aggregate([{"$group":{_id:"$"+username+,nos:{"$sum":1}}}])
    return render(request, 'contestanthome.html',
                   {'cname': contestname ,'username':username, 'programs':list(programs), 'scores':scores}) 

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
    c = Connection()
    db1 = c.autotest
    programs = db1.submissions.find({'user_name':username})
    return render(request, 'testadminhome.html', {'cname': contestname ,'username':username})
	
def puppetrun(request):
    cn = request.session['contestname']
    c = Connection()
    db1 = c.autotest
    cll=db1.contest.find_one({'contestname':cn},{'status':1,'_id':0})
    st=cll["status"]
    if(st == "Not Started"):
        os.system("cd ..")
        os.system("ls")
        os.system("vagrant up")
        db1.contest.update({'contestname':cn},{"$set":{'status':"Started"}})
        return HttpResponse(str("Contest Started"))
    else:
        return HttpResponse(str("Contest Already Done"))

def puppetstop(request):
    cn = request.session['contestname']
    c = Connection()
    db1 = c.autotest
    cll=db1.contest.find_one({'contestname':cn},{'status':1,'_id':0})
    st=cll["status"]
    if(st == "Started"):
        db1.contest.update({'contestname':cn},{"$set":{'status':"Finished"}})
        os.system("vagrant stop")
        return HttpResponse(str("Already finished"))

def deactivateuser(request):
    cn = Connection()
    db1 = cn.autotest
    un = request.POST.get("names")
    db1.contestant.update({'username':un},{"$set":{'status':"Deactivate"}})
    return HttpResponseRedirect('/testadminhome') 

#------------TestCreator Home------------#
def testcreatorhome(request):
	contestname = request.session['contestname']
	username = request.session['username']
	cn = Connection()
	db1 = cn.autotest
	problems=db1.problemsrepository.find()
	dt=db1.contest.find_one({'contestname':contestname})
	date=dt["date"] 
	return render(request, 'testcreatorhome.html',
	{'cname': contestname ,'username':username,'date':date ,'problems':problems})       

def createquestionpaper(request):
    cn=Connection()
    db1=cn.autotest
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
    cn = Connection()
    db1 = cn.autotest
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
    cn = Connection()
    db1 = cn.autotest
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
