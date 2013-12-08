import subprocess
import os
import conf
from conf import participant_dir
import xml.etree.ElementTree as ET
import testmail


def listofParticipants():
    dirs1 = os.listdir(conf.participant_dir)
    for user in dirs1:
        direct=participant_dir + user + '/'
        previous={}
        for y in os.listdir(direct):
            if os.path.isdir(direct+'/'+y) and y[0] !='.':
                previous[y] = subprocess.check_output(['/usr/bin/git',
                                                 'log','-1',
                                                 '--oneline',y],
                                                cwd=direct)
        subprocess.call(['/usr/bin/git', 'pull'], cwd=direct)

        for y in os.listdir(direct):
            if os.path.isdir(direct+'/'+y) and y[0] !='.':
                after = subprocess.check_output(['/usr/bin/git',
                                                 'log','-1',
                                                 '--oneline',y],
                                                cwd=direct)
                if True or y not in previous or previous[y] != after:
                    yield user,y
        
  
    
def inputoutput(progname):
    tree = ET.parse(conf.program_dir+progname+".xml")
    root=tree.getroot()
    for test in root:
        input_str=test.find('input').text
        output_str=test.find('output').text
        description=test.find('description').text
        yield input_str,output_str,description 

#for input_str, output_str, description in inputoutput('Echo'):
#   print input_str, output_str, description

if __name__ == '__main__':
    for user,programname in listofParticipants():
        program_dir=conf.participant_dir+user+'/'+programname
        print 'checking if program is valid '+ programname
        program_name=conf.program_dir+programname+'.xml'
        if not os.path.isfile(program_name):
            testmail.feedbackmail()
            print 'program name is invalid'
            continue            
                   
        print 'compiling ' + program_dir
        ret=subprocess.call(['/bin/bash','compile.sh'],cwd=program_dir)
        if ret!=0:
            testmail.feedbackmail()
            print 'Failed compilation error'
            continue        
        for input_i,output_o,description_d in inputoutput(programname):
            run_cmd = ['/bin/bash','run.sh']
            run_cmd.extend(input_i.split(' '))
            try:
                cmd_op = subprocess.check_output(run_cmd,cwd=program_dir)
                cmd_op=cmd_op.strip()
                if cmd_op == output_o:
                    testmail.feedbackmail()
                    print 'SUCCESSFUL ' + description_d
                else:
                    testmail.feedbackmail()
                    print 'FAILED ' + description_d
            except:
                testmail.feedbackmail()
                print 'ERROR ' + description_d
