import conf
from conf import db_host
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from pymongo import Connection
import base64
import json
import os
import hashlib
from bson.son import SON

# Create your views here.
def superuser(request):
    cn=Connection()
    db1=cn.autotest
    contests=db1.contest.find()
    return render(request, 'superuser.html', {'contests':contests})

def deleteContest(request):
    cn=Connection()
    db1=cn.autotest
    cname=request.POST.get('cname')
    print(cname)
    db1.contest.remove({ "contestname" : cname })
    return HttpResponseRedirect('superuser.html')

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
    # con = db1.contest.findOne({'contestname': cname })
    # if (con != cname):
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
                    }
            })
    return HttpResponseRedirect('superuser.html')

def home(request):
    return render(request, 'home.html', {})  

def registration(request):
    cn=Connection()
    db1=cn.autotest
    cname=db1.contest.find({},{'contestname' : 1 , '_id' : 0})
    return render(request, 'registration.html', {'cname':cname})

def loginform(request):
    cn=Connection()
    db1=cn.autotest
    cname=db1.contest.find({},{'contestname' : 1 , '_id' : 0})
    return render(request, 'loginform.html', {'cname':cname})  

def loginvalidate(request):
    contestname = request.POST.get('contestname')
    usertype = request.POST.get('usertype')
    username = request.POST.get('username')
    password = request.POST.get('password')
    a=hashlib.sha1(password)
    password=a.hexdigest()
    cn = Connection()
    db1 = cn.autotest
    if(usertype == "contestant"):
	coll=db1.contestant.find_one({'contestname':contestname,'username':username,'password':password})
	if(coll != 'None'):
  	    return render(request, 'contestanthome.html', {'cname':contestname ,'username':username})       
        else:
	    return HttpResponse("error")
    if(usertype == "testadmin"):
	coll=db1.contest.find_one({'contestname':contestname,'username':username,'password':password})
	if(coll != 'None'):
  	    return render(request, 'testadminhome.html', {'cname':contestname ,'username':username})       
        else:
	    return HttpResponse("error")
    if(usertype == "testcreator"):
	coll=db1.contest.find_one({'contestname':contestname,'username':username,'password':password})
	if(coll != 'None'):
	    problems=db1.problemsrepository.find()
	    dt=db1.contest.find_one({'contestname':contestname})
	    #date=dt.date
  	    return render(request, 'testcreatorhome.html', 
			{'date':"date" ,'problems':problems ,'cname':contestname ,'username':username})       
        else:
	    return HttpResponse("error")
    if(usertype == "participantapprover"):
	coll=db1.contest.find_one({'contestname':contestname,'username':username,'password':password})
	if(coll != 'None'):
	    contestants=db1.contestant.find({'contestname':contestname})
  	    return render(request, 'participantapproverhome.html', {'contestants':contestants ,'cname':contestname ,'username':username})       
        else:
	    return HttpResponse("error")

def regisuccess(request):
    cn = request.POST.get('contestname')
    un = request.POST.get('username')
    name = request.POST.get('name')
    email = request.POST.get('email')
    pswd = request.POST.get('pass')
    a=hashlib.sha1(pswd)
    hpswd=a.hexdigest()
    c = Connection()
    db1 = c.autotest
    #cid=db1.contest.find_one({'contestname':cn},{'_id':1})
    user={"contestname":cn,"name":name,"username":un,"email":email,"password":hpswd}
    db1.contestant.insert(user)
    return render(request,'regisuccess.html',{})

def puppet(request):
    cn=request.GET.get('state')
    c = Connection()
    db1 = c.autotest
    print("hiiiiiiiiiiiiiii")
    cll=db1.contest.find_one({'contestname':cn},{'status':1,'_id':0})
    st=cll["status"]
    if(st == "Not Started"):
       db1.contest.update({'contestname':cn},{"$set":{'status':"Started"}})
       os.system("cd ..")
       os.system("ls")
       os.system("vagrant up")
       print "vagrant startedddddd"
       return HttpResponse("Heloooo pup started")
    else:
       db1.contest.update({'contestname':cn},{"$set":{'status':"Finished"}})
       return HttpResponse("Heloooo pup stoped")
