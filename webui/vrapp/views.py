import conf
from conf import db_host
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from pymongo import Connection
import base64
import json
import os

# Create your views here.
def superuser(request):
    cn=Connection()
    db1=cn.autotest
    contests=db1.contest.find()
    return render(request, 'superuser.html', {'contests':contests})

def deleteContest(request):
    cn=Connection()
    db1=cn.autotest
    cname=request.GET.get('cname')
    db.contest.remove({ "contestname" : cname })
    return render(request, 'superuser.html', {})

def home(request):
    return render(request, 'home.html', {})  

def registration(request):
    name = "hiiiiiiiiiii registration"
    return render(request, 'registration.html', {'name':name})  

def loginform(request):
    cn=Connection()
    db1=cn.autotest
    cname=db1.contest.find()
    return render(request, 'loginform.html', {'cname',cname})  

def loginvalidate(request):
    usertype = request.GET.get('usertype')
    username = request.GET.get('username')
    password = request.GET.get('password')
    cn = Connection()
    db1 = cn.autotest
    flag=0
    contestname = request.GET.get('contestname')
    if(usertype == "contestant"):
	coll=db1.contestant.find_one({'contestname':contestname,'username':username,'password':password})
	if(coll != 'None'):
  	    return render(request, 'contestanthome.html', {'ut':"Contestanthome", 'username':username, 'ps':password})       
        else:
	    return HttpResponse("error")
    else: 
        coll = db1.contest.find()
        for c in coll:
            if(c["contestname"] == contestname):
                if username in c[usertype].keys():
                    if c[usertype][username]["password"] == password :
		         homepage=usertype+"home.html"
                         return render(request, homepage , {'ut':homepage, 'un':username, 'ps':password})       
                else:
                    return HttpResponse("error")

def regisuccess(request):
    cn = request.GET.get('contestname')
    un = request.GET.get('username')
    name = request.GET.get('name')
    email = request.GET.get('email')
    pswd = request.GET.get('pass')
    c = Connection()
    db1 = c.autotest
    #cid=db1.contest.find_one({'contestname':cn},{'_id':1})
    user={"contestname":cn,"name":name,"username":un,"email":email,"password":pswd}
    db1.contestant.insert(user)
    return render(request,'loginform.html',{})

def pup(request):
    os.system("cd ..")
    os.system("ls")
    os.system("vagrant up")
    #print "vagrant startedddddd"
    return HttpResponse("Heloooo pup started")
