import subprocess
import conf

files = '../starter-files/*'
direct=conf.participant_dir
fi=open(conf.mail_dir + 'user_list.csv')

for user in fi:
    fp=open("/home/svpmtrust/username.txt","w")
    fp.writelines([user,user])
    fp.close()
    fp=open("/home/svpmtrust/username.txt","r")
    user = user.strip()
    user,email = user.split(',')
    #fp.seek(0,0)
    subprocess.call('/bin/rm -rf %s' % user, cwd=direct, shell=True)
    subprocess.call(['/usr/bin/git','clone',
                     "http://{u}:{u}@{h}/git/{u}.git".format(u=user, h=conf.git_host)],
                    cwd=direct)
    subprocess.call('/bin/cp -r %s %s' % (files, direct+user), shell=True)
    
    subprocess.call(['/usr/bin/git','add','.'],cwd=direct+user)
    subprocess.call(['/usr/bin/git','commit','-m',"Commiting the initial files"],cwd=direct+user)
    fp.seek(0)
    subprocess.call(['/usr/bin/git','push','origin','master'],cwd=direct+user)
    fp.close