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
    db1.contest.remove({ "contestname" : cname })
    return HttpResponseRedirect('superuser.html')

def addContest(request):
    cn=Connection()
    db1=cn.autotest
    cname=request.POST.get('contestname')
    organisation=request.POST.get('organisation')
    date=request.POST.get('date')
    status=request.POST.get('status')
    tnc=request.POST.get('tnc')
    approverrule=request.POST.get('approverrule')
    ta1un=request.POST.get('ta1un')
    ta1pswd=request.POST.get('ta1pswd')
    ta1email=request.POST.get('ta1email')
    ta2un=request.POST.get('ta2un')
    ta2pswd=request.POST.get('ta2pswd')
    ta2email=request.POST.get('ta2email')
    tc1un=request.POST.get('tc1un')
    tc1pswd=request.POST.get('tc1pswd')
    tc1email=request.POST.get('tc1email')
    pa1un=request.POST.get('pa1un')
    pa1pswd=request.POST.get('pa1pswd')
    pa1email=request.POST.get('pa1email')
    pa2un=request.POST.get('pa2un')
    pa2pswd=request.POST.get('pa2pswd')
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
    return render(request, 'registration.html', {})  

def loginform(request):
    cn=Connection()
    db1=cn.autotest
    cname=db1.contest.find({},{'contestname' : 1 , '_id' : 0})
    return render(request, 'loginform.html', {'cname':cname})  

def loginvalidate(request):
    usertype = request.GET.get('usertype')
    username = request.GET.get('username')
    password = request.GET.get('password')
    a=hashlib.sha1(password)
    hpassword=a.hexdigest()
    cn = Connection()
    db1 = cn.autotest
    flag=0
    contestname = request.GET.get('contestname')
    if(usertype == "contestant"):
	coll=db1.contestant.find_one({'contestname':contestname,'username':username,'password':hpassword})
	if(coll != 'None'):
  	    return render(request, 'contestanthome.html', {'ut':"Contestanthome", 'username':username, 'ps':hpassword})       
        else:
	    return HttpResponse("error")
    else: 
        coll = db1.contest.find()
        for c in coll:
            if(c["contestname"] == contestname):
                if username in c[usertype].keys():
                    if c[usertype][username]["password"] == hpassword :
		         homepage=usertype+"home.html"
                         return render(request, homepage , {'ut':homepage, 'un':username, 'ps':hpassword})       
                else:
                    return HttpResponse("error")

def regisuccess(request):
    cn = request.GET.get('contestname')
    un = request.GET.get('username')
    name = request.GET.get('name')
    email = request.GET.get('email')
    pswd = request.GET.get('pass')
    a=hashlib.sha1(pswd)
    hpswd=a.hexdigest()
    c = Connection()
    db1 = c.autotest
    #cid=db1.contest.find_one({'contestname':cn},{'_id':1})
    user={"contestname":cn,"name":name,"username":un,"email":email,"password":hpswd}
    db1.contestant.insert(user)
    return render(request,'regisuccess.html',{})

def pup(request):
    os.system("cd ..")
    os.system("ls")
    os.system("vagrant up")
    #print "vagrant startedddddd"
    return HttpResponse("Heloooo pup started")
