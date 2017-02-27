import smtplib
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import never_cache
import json
import os
import subprocess
import hashlib
import time
from vrautotest.settings import db1, on_aws, BASE_DIR, DB_HOST, DB_NAME, AWS_KEY, AWS_SECRET
import boto
import boto.cloudformation
import boto.ec2
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def login_required(func):
    def inner(request):
        if request.session.has_key("contestname"):
            return func(request)

        else:
            return render(request, 'errorpage.html', {'emessage': "Sorry Session Expired :("})

    return inner


# --------------SuperUser------------#

def superuser(request):
    contests = db1.contest.find()
    return render(request, 'superuser.html', {'contests': contests})


def execute_remote_command(instance, command):
    cmd = [
        "/usr/bin/ssh",
        "-o",
        "StrictHostKeyChecking=no",
        "-o",
        "UserKnownHostsFile=/dev/null",
        "-o",
        "LogLevel=quiet",
        "-i",
        '/home/ubuntu/hiringkeys.pem',
        "ubuntu@" + str(instance.private_ip_address),
        command]
    print instance.private_ip_address
    output = subprocess.check_output(cmd)
    return output


def deleteContest(request):
    cname = request.POST.get('cname')
    contests = db1.contest.find_one({"contestname": cname}, {'testadmin': 1, '_id': 0})
    print contests
    cmd1 = "tar -czvf data.tar.gz /opt/git/"
    cmd2 = "aws s3 cp data.tar.gz s3://contestsdata/{}-submissions.tar.gz".format(cname)
    instance_name = "GitServer - "+cname
    ec2_conn = boto.ec2.connect_to_region("ap-southeast-1",aws_access_key_id=AWS_KEY,aws_secret_access_key=AWS_SECRET)
    instance_obj = ec2_conn.get_all_instances(filters={"tag:Name": instance_name})
    y = instance_obj[0]
    instance_obj = y.instances[0]
    result = execute_remote_command(instance_obj, cmd1)
    print result
    result = execute_remote_command(instance_obj, cmd2)
    print result
    if contests:
        try:
            admin_email_list=[]
            admin_info = contests["testadmin"]
            for x,admin_details in admin_info.items():
                admin_email_list.append(admin_details.get('emaill'))
            to=admin_email_list
            print to
            # to = "padmasree.potta@aviso.com"
            gmail_user = 'techcontest2015@gmail.com'
            gmail_pwd = 'Aviso2017'
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.login(gmail_user, gmail_pwd)
            header = 'To:' + ",".join(to) + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Contest ended \n'
            msg = header + '\n\n Machines are going to terminate in 1 hour, Please ensure that participant submissions are uploaded to s3.\n\nThank you'
            smtpserver.sendmail(gmail_user, to, msg)
            smtpserver.close()
        except Exception as e:
            print "Error while sending mail"
    cf = boto.cloudformation.connect_to_region("ap-southeast-1")
    cf.delete_stack(cname)
    db1.contest.remove({"contestname": cname})
    return HttpResponseRedirect('/superuser')

@csrf_exempt
def addquestion(request):
    temp = 1
    qname = request.POST.get('qname')
    qtype = request.POST.get('qtype')
    qlevel = request.POST.get('qlevel')
    qmarks = request.POST.get('qmarks')
    if qname:
        db1.problemsrepository.insert(
            {
                "description": qname,
                "qtype": qtype,
                "difficultylevel": qlevel,
                "score": qmarks
            }
    )
    return render(request, 'testcreatorhome.html', {'temp':temp})

def addContest(request):
    cname = request.POST.get('contestname')
    organisation = request.POST.get('organisation')
    date = request.POST.get('date')
    status = request.POST.get('status')
    tnc = request.POST.get('tnc')
    approverrule = request.POST.get('approverrule')
    ta1un = request.POST.get('ta1un')
    ta1pswd = request.POST.get('ta1pswd')
    ta1pswd = hashlib.sha1(ta1pswd)
    ta1pswd = ta1pswd.hexdigest()
    ta1email = request.POST.get('ta1email')
    ta2un = request.POST.get('ta2un')
    ta2pswd = request.POST.get('ta2pswd')
    ta2pswd = hashlib.sha1(ta2pswd)
    ta2pswd = ta2pswd.hexdigest()
    ta2email = request.POST.get('ta2email')
    tc1un = request.POST.get('tc1un')
    tc1pswd = request.POST.get('tc1pswd')
    tc1pswd = hashlib.sha1(tc1pswd)
    tc1pswd = tc1pswd.hexdigest()
    tc1email = request.POST.get('tc1email')
    pa1un = request.POST.get('pa1un')
    pa1pswd = request.POST.get('pa1pswd')
    pa1pswd = hashlib.sha1(pa1pswd)
    pa1pswd = pa1pswd.hexdigest()
    pa1email = request.POST.get('pa1email')
    pa2un = request.POST.get('pa2un')
    pa2pswd = request.POST.get('pa2pswd')
    pa2pswd = hashlib.sha1(pa2pswd)
    pa2pswd = pa2pswd.hexdigest()
    pa2email = request.POST.get('pa2email')
    db1.contest.insert({
        "contestname": cname,
        "organisation": organisation,
        "date": date,
        "status": status,
        "tnc": tnc,
        "approverrule": approverrule,
        "testadmin": {
            ta1un: {
                "password": ta1pswd,
                "emaill": ta1email
            },
            ta2un: {
                "password": ta2pswd,
                "emaill": ta2email
            }
        },
        "testcreator": {
            tc1un: {
                "password": tc1pswd,
                "emaill": tc1email
            }
        },
        "participantapprover": {
            pa1un: {
                "password": pa1pswd,
                "emaill": pa1email
            },
            pa2un: {
                "password": pa2pswd,
                "emaill": pa2email
            }
        },
        "questions": {},
        "questions_criteria": {}
    })
    return HttpResponseRedirect('superuser')


def checkContestName(request):
    contestname = request.GET.get("contestname")
    con = db1.contest.find_one({'contestname': contestname})
    if not con:
        return HttpResponse("Valid")
    else:
        return HttpResponse("InValid")


# ------------Home---------------#

def home(request):
    try:
        del request.session['contestname']
        del request.session['username']
    except KeyError:
        pass
    return render(request, 'home.html', {})


def registration(request):
    cname = db1.contest.find({}, {'contestname': 1, '_id': 0})
    return render(request, 'registration.html', {'cname': cname})


def checkUserName(request):
    contestname = request.GET.get("contestname")
    username = request.GET.get("username")
    # con = db1.contestant.find_one({'username':username })
    con1 = db1.contestant.find_one({'contestname': contestname, 'username': username}, {'username': 1, '_id': 0})
    # print db1
    # print con1
    # print contestname
    # print username
    if not con1:
        return HttpResponse("Valid")
    else:
        return HttpResponse("InValid")


@csrf_exempt
def regisuccess(request):
    cn = request.POST.get('contestname')
    un = request.POST.get('username')
    name = request.POST.get('name')
    email = request.POST.get('email')
    pswd = request.POST.get('pass')
    if not pswd:
        '''return HttpResponse("ERROR: You need a password to register")'''
        return render(request, 'errorpage.html',
                      {'emessage': "You need a password to register.. Please Register Again"})
    a = hashlib.sha1(pswd)
    hpswd = a.hexdigest()
    d = db1.contest.find_one({"contestname": cn})
    if d["approverrule"] == "0":
        apstatus = "1"
    else:
        apstatus = "0"
    user = {"contestname": cn, "name": name, "username": un, "email": email, "password": hpswd,
            "approved_status": apstatus,
            "approved_by": [],
            "status": "active",
            "questions": [],
            "git_repo_created": False
            }
    dbr = db1.contestant.insert(user)
    if dbr:
        try:
            to = email
            gmail_user = 'techcontest2015@gmail.com'
            gmail_pwd = 'Aviso2017'
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(gmail_user, gmail_pwd)
            header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Registration Successfull \n'
            msg = header + '\n Thank you for Your Registration to ' + cn + '\n ' + ' UserName : ' + un + '\n Password : ' + pswd + '\n \n'
            smtpserver.sendmail(gmail_user, to, msg)
            smtpserver.close()
        except Exception as e:
            print "Error while sending mail"
        return HttpResponseRedirect('loginform')
    else:
        '''return HttpResponse("ERROR: Sorry Please Register Again")'''
        return render(request, 'errorpage.html', {'emessage': "Sorry Something went wrong.. Please Register Again"})


# ---------Login----------#

def loginform(request):
    try:
        # print request.session.keys() ,"before deleting in loginform"
        del request.session['contestname']
        del request.session['username']
        # print request.session ,"after deleting in loginform"
        return render(request, 'errorpage.html', {'emessage': "Sorry Session Expired :("})
    except KeyError as k:
        print k
        pass
    cname = db1.contest.find({}, {'contestname': 1, '_id': 0})
    print "cname in log in form is ", cname
    return render(request, 'loginform.html', {'cname': cname})


def logout(request):
    # print "i am called outside try"
    try:
        # print "i am called in try"
        # print request.session,"in logout before deleting"
        del request.session['contestname']
        del request.session['username']
        # print request.session.keys(), "in logout after deleting"
    except KeyError as k:
        print k
        pass
    cname = db1.contest.find({}, {'contestname': 1, '_id': 0})
    print "cname in logout is ", cname
    return render(request, 'loginform.html', {'cname': cname})


@csrf_exempt
def loginvalidate(request):
    usertype = request.POST.get('usertype')
    contestname = request.POST.get('contestname1')
    username = request.POST.get('username1')
    password = request.POST.get('password1')
    a = hashlib.sha1(password)
    password = a.hexdigest()
    request.session['contestname'] = contestname
    request.session['username'] = username
    cname = db1.contest.find({}, {'contestname': 1, '_id': 0})
    failurereason = " "

    if (usertype == "contestant"):
        coll = db1.contestant.find_one({'contestname': contestname, 'username': username})
        if coll:
            if password == coll["password"]:
                return HttpResponseRedirect('/contestanthome')
            else:
                failurereason = "Incorrect password"
        else:
            failurereason = "Incorrect username"
    elif (usertype == "testadmin"):
        coll = db1.contest.find_one({"contestname": contestname})
        if username in coll["testadmin"].keys():
            if password == coll["testadmin"][username]["password"]:
                return HttpResponseRedirect('/testadminhome')
            else:
                failurereason = "Incorrect password"
        else:
            failurereason = "Incorrect username"
    elif (usertype == "testcreator"):
        coll = db1.contest.find_one({"contestname": contestname})
        if username in coll["testcreator"].keys():
            if password == coll["testcreator"][username]["password"]:
                return HttpResponseRedirect('/testcreatorhome')
            else:
                failurereason = "Incorrect password"
        else:
            failurereason = "Incorrect username"
    elif (usertype == "participantapprover"):
        coll = db1.contest.find_one({"contestname": contestname})
        if username in coll["participantapprover"].keys():
            if password == coll["participantapprover"][username]["password"]:
                return HttpResponseRedirect('/participantapproverhome')
            else:
                failurereason = "Incorrect password"
        else:
            # '''return HttpResponse("error")'''
            failurereason = "Incorrect username"

    del request.session['contestname']
    del request.session['username']
    return render(request, 'loginform.html', {'cname': cname, 'error': failurereason})


# ------------Contestant Home------------#
@never_cache
@login_required
def contestanthome(request):
    print request.session.keys()
    contestname = request.session['contestname']
    username = request.session['username']

    coll = db1.contestant.find_one({"username": username})
    password = coll["password"]
    programs = db1.submissions.find({'user_name': username})
    git_repo_created = coll.get("git_repo_created")
    scores = db1.scores.aggregate([
        {"$match":
             {"$and": [{"contestname": contestname}]}},
        {"$group": {"_id": "$user_name", "total": {"$sum": "$score"}}},
        {"$sort": {"total": -1}}
    ])
    # for i in scores:
    #    scores = i['result']
    scores = scores["result"]
    rank = 0
    userscores = []
    totalscore = 0
    for i, u in enumerate(scores):
        user_name = u["_id"]
        total = u["total"]
        userscores.append({'username': user_name, 'total': total})
    for i, u in enumerate(scores):
        if u["_id"] == username:
            rank = (i + 1)
            totalscore = u["total"]
    contest_data = db1.contest.find_one({"contestname": contestname}, {"_id": 0, "status": 1, "git_ip": 1})
    # nor_submissions=db1.submissions.find([{"$match"{"username":username},"$group":{"_id":"$programname","no_of_sub":{"$sum":1}}).count()
    conteststatus = contest_data['status']
    git_address = contest_data.get('git_ip', None)
    submissions = db1.submissions.aggregate([{
        "$match": {
        }},
        {"$group": {"_id": "$program",
                    'no-of-submissions': {'$sum': 1},

                    'successfull-submissions': {"$sum":
                        {
                            "$cond":
                                [{"$eq": ["$program_result", "SUCCESSFUL"]}
                                    , 1, 0
                                 ]
                        }

                    },
                    'scores': {"$max": "$score"}

                    }}]
    )
    print submissions
    pro = list()
    for submission in submissions['result']:
        result = dict()
        program = submission["_id"]
        result['program'] = submission['_id']
        result['Total_sub'] = submission['no-of-submissions']
        result['Successful_sub'] = submission['successfull-submissions']
        #
        result['Program_score'] = submission['scores']
        firstsubmitted = db1.scores.find_one({'program': program, 'contestname': contestname},
                                             {'user_name': 1, '_id': 0})
        if firstsubmitted is None:
            result['First_submitted'] = "N/A"
        else:
            result['First_submitted'] = firstsubmitted['user_name']
        # result['Program_score'] = programscore['score']
        # print programscore
        print "first submitted is ", firstsubmitted

        pro.append(result)

    return un_cache_response(render(
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
            'rank': rank,
            'git_repo_created': git_repo_created,
            'prog': pro,
        }
    ))


'''
def submissions(request):
    c = Connection()
    db1 = c.autotest
    contestname = request.session['contestname']
    username = request.session['username']
    submissions = db1.submissions.find({'username':username})
    return render(request, 'contestanthome.html', {'cname': contestname ,'username':username , 'submissions':submissions})
'''


# ------------TestAdmin Home------------#
@never_cache
@login_required
def testadminhome(request):
    # testadminhome = login_required(testadminhome)
    contestname = request.session['contestname']
    username = request.session['username']
    contest_data = db1.contest.find_one({"contestname": contestname}, {"_id": 0, "status": 1, "git_ip": 1})
    conteststatus = contest_data['status']
    git_address = contest_data.get('git_ip', None)
    users = db1.contestant.find({'contestname': contestname})
    scores = db1.scores.aggregate([
        {"$match":
             {"$and": [{"contestname": contestname}]}},
        {"$group": {"_id": "$user_name", "total": {"$sum": "$score"}}},
        {"$sort": {"total": -1}}
    ])
    # for i in scores:
    #    scores = i['result']

    scores = scores["result"]
    userscores = []
    for i, u in enumerate(scores):
        user_name = u["_id"]
        total = u["total"]
        sub = db1.submissions.find({'user_name': user_name}).count()
        programs = db1.scores.find({'user_name': user_name}).count()
        userscores.append({'username': user_name, 'total': total, 'submissions': sub, 'programs': programs})

    submission = db1.submissions.aggregate([{
        "$match": {
        }},
        {"$group": {"_id": "$program",
                    'no-of-submissions': {'$sum': 1},

                    'successfull-submissions': {"$sum":
                        {
                            "$cond":
                                [{"$eq": ["$program_result", "SUCCESSFUL"]}
                                    , 1, 0
                                 ]
                        }

                    },
                    'scores': {"$max": "$score"}

                    }}]
    )
    print submission
    pra = list()
    for submission in submission['result']:
        program = submission["_id"]
        result = dict()

        result['program'] = submission['_id']
        result['Total_sub'] = submission['no-of-submissions']
        result['Successful_sub'] = submission['successfull-submissions']
        # programscore = db1.submissions.find_one({'program': program}, {'score': 1, '_id': 0})
        firstsubmitted = db1.scores.find_one({'program': program, 'contestname': contestname},
                                             {'user_name': 1, '_id': 0})
        if firstsubmitted is None:
            result['First_submitted'] = "N/A"
        else:
            result['First_submitted'] = firstsubmitted['user_name']
        result['Program_score'] = submission['scores']
        # print programscore['score']
        print type(firstsubmitted)
        print "first submitted is ", firstsubmitted
        # result['score'] = submission['score']
        pra.append(result)

    return un_cache_response(render(request, 'testadminhome.html',
                                    {'cname': contestname,
                                     'username': username,
                                     'scores': list(userscores),
                                     'cstatus': conteststatus,
                                     'git_address': git_address,
                                     'programsubbmissions': pra,
                                     })
                             )


def puppetrun(request):
    cn = request.session['contestname']
    print cn
    cll = db1.contest.find_one({'contestname': cn}, {'status': 1, '_id': 0})
    st = cll["status"]
    if (st == "Not Started"):
        print "ON_AWS is ::::::::::::", on_aws
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
                        ("ContestName", cn),
                        ("AWSkey", AWS_KEY),
                        ("AWSsecret", AWS_SECRET)
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

            db1.contest.update({'contestname': cn},
                               {"$set": {
                                   'status': "Started",
                                   'git_ip': git_ip}
                               })
        else:
            os.system("cd ..")
            os.system("ls")
            vagrantstarted(request)
            os.system("vagrant up")
            vagrantstarted1(request)
            db1.contest.update({'contestname': cn},
                               {"$set": {
                                   'status': "Started",
                                   'git_ip': "192.168.50.1"}
                               })
            git_ip = "192.168.50.1"
        return HttpResponse(str(git_ip))
    else:
        return HttpResponse(str("Contest Already Started"))


def vagrantstarted(request):
    return render(request, 'testadminhome.html', {'msg': "vagrant is starting"})


def vagrantstarted1(request):
    return render(request, 'testadminhome.html', {'msg1': "vagrant started"})


def puppetstop(request):
    cn = request.session['contestname']
    cll = db1.contest.find_one({'contestname': cn}, {'status': 1, '_id': 0})
    st = cll["status"]
    if (st == "Started"):
        # db1.contest.update({'contestname': cn}, {"$set": {'status': "Finished"}})

        os.system("vagrant stop")

        return HttpResponse(str("Contest Stopped"))


def deactivateuser(request):
    un = request.POST.get("names")
    db1.contestant.update({'username': un}, {"$set": {'status': "Deactivate"}})
    return HttpResponseRedirect('/testadminhome')


# ------------TestCreator Home------------#
@never_cache
@login_required
def testcreatorhome(request):
    if request.session.has_key("contestname"):
        contestname = request.session['contestname']
        username = request.session['username']
        problems = db1.problemsrepository.find()
        dt = db1.contest.find_one({'contestname': contestname})
        date = dt["date"]
        return un_cache_response(render(request, 'testcreatorhome.html',
                                        {'cname': contestname, 'username': username, 'date': date,
                                         'problems': problems})
                                 )
    else:
        return loginform(request)


@never_cache
@login_required
def createquestionpaper(request):
    contestname = request.session['contestname']
    ques = json.loads(request.GET.get("names"))
    flags = json.loads(request.GET.get("flags"))
    coll = db1.contest.find_one({"contestname": contestname})
    easy = request.GET.get("easy")
    medium = request.GET.get("medium")
    hard = request.GET.get("hard")
    coll["questions_criteria"] = {"easy": easy,
                                  "medium": medium,
                                  "hard": hard}
    for i in ques:
        if i in flags:
            coll["questions"].update({i: 1})
        else:
            coll["questions"].update({i: 0})
    db1.contest.save(coll)
    return HttpResponse("created")


# ------------ParticipantApprover Home------------#
@never_cache
@login_required
def participantapproverhome(request):
    contestname = request.session['contestname']
    username = request.session['username']
    sname = request.GET.get("patype")
    contestants = db1.contestant.find({'contestname': contestname})
    pa = db1.contest.find({'contestname': contestname}, {'participantapprover': 1})
    for i in pa:
        tc = i["participantapprover"]
    pa = list()
    for i in tc.keys():
        pa.append(i)
    if (sname == "eligible"):
        contestants = db1.contestant.find({'contestname': contestname, "approved_status": "1"})
    elif (sname == "approve"):
        contestants = db1.contestant.find(
            {'contestname': contestname, "approved_status": "0", "approved_by": {"$ne": sname}})
    else:
        contestants = db1.contestant.find({'contestname': contestname, "approved_by": {"$in": [sname]}})
    return un_cache_response(render(request, 'participantapproverhome.html',
                                    {'contestants': contestants, 'cname': contestname, 'username': username,
                                     'pa1': pa[0], 'pa2': pa[1]})
                             )


@never_cache
@login_required
def approve(request):
    users = json.loads(request.GET.get("names"))
    contestname = request.session['contestname']
    username = request.session['username']
    contest = db1.contest.find_one({'contestname': contestname}, {"approverrule": 1, "_id": 0})
    crule = int(contest["approverrule"])
    print(crule)
    print(contest)
    for u in users:
        print(u)
        cont = db1.contestant.find_one({"contestname": contestname, "username": u})
        cont["approved_by"].append(username)
        if (crule >= len(cont["approved_by"])):
            cont["approved_status"] = "1"
        db1.contestant.save(cont)
    return HttpResponse("Valid")


def un_cache_response(response):
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response
