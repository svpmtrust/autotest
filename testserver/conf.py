import os

participant_dir = os.environ.get('PARTICIPANT_DIR', '/home/svpmtrust/participants/')
program_dir = os.environ.get('PROGRAM_DIR', '/home/svpmtrust/Programs/')
mail_dir = os.environ.get('MAIL_DIR', '/home/svpmtrust/mails/')
git_host = os.environ.get('GIT_HOST', '192.168.1.105:8080')
db_host = os.environ.get('DB_HOST', 'mongodb://127.0.0.1:27017/')

