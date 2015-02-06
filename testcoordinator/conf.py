import os

participant_dir = os.environ.get('PARTICIPANT_DIR', '/vagrant/participants/')
program_dir = os.environ.get('PROGRAM_DIR', '/vagrant/programs/')
mail_dir = os.environ.get('MAIL_DIR', '/vagrant/mails/')
git_host = os.environ.get('GIT_HOST', '192.168.1.101:12003')
db_host = os.environ.get('DB_HOST', 'mongodb://192.168.1.101:27017/')
