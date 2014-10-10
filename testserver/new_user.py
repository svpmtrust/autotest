import subprocess
import conf
import os

files = '../starter-files/*'
direct=conf.participant_dir
fi=open(conf.mail_dir + 'user_list.csv')

for user in fi:

    user = user.strip()
    if not user:
        continue

    fp=open("/tmp/username.txt","w")
    fp.writelines([user,user])
    fp.close()
    fp=open("/tmp/username.txt","r")
    
    user,pwd,email = user.split(',')
    
    if os.path.isdir(os.path.join(direct, user)):
        continue
    
    subprocess.call(['/usr/bin/git','clone',
                     "http://{u}:{p}@{h}/git/{u}.git".format(u=user, h=conf.git_host, p=pwd)],
                    cwd=direct)
    subprocess.call('/bin/cp -r %s %s' % (files, direct+user), shell=True)
    
    subprocess.call(['/usr/bin/git','add','.'], cwd=direct+user)
    subprocess.call(['/usr/bin/git','commit','-m',"Commiting the initial files"], cwd=direct+user)
    fp.seek(0)
    subprocess.call(['/usr/bin/git','push','origin','master'], cwd=direct+user)
    fp.close()
