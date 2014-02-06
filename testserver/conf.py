<<<<<<< HEAD
participant_dir = '/home/svpmtrust/participants/'
program_dir='/home/svpmtrust/Programs/'
mail_dir='/home/svpmtrust/mails/'
git_host= '192.168.1.102:8080'
=======
import os
>>>>>>> branch 'master' of https://github.com/svpmtrust/autotest.git

participant_dir = os.environ.get('PARTICIPANT_DIR', '/home/svpmtrust/participants/')
program_dir = os.environ.get('PROGRAM_DIR', '/home/svpmtrust/Programs/')
mail_dir = os.environ.get('MAIL_DIR', '/home/svpmtrust/mails/')
git_host = os.environ.get('GIT_HOST', '192.168.1.105:8080')
