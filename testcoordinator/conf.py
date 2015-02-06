import os

root_dir = os.environ.get('GITSERVER_ROOT', '/vagrant')
contest_name = os.environ.get('CONTEST_NAME', 'VR_Auto_Test')
participant_dir = os.path.join(root_dir, 'participants/')
program_dir = os.path.join(root_dir, 'programs/')
git_host = os.environ.get('GIT_HOST', '192.168.1.101:12003')
db_host = os.environ.get('DB_HOST', 'mongodb://192.168.1.101:27017/')