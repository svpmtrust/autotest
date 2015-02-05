import subprocess
import os
import conf
from conf import participant_dir
import xml.etree.ElementTree as ET
import time
import shlex
import timed_execution
import json
from celery import Celery

app = Celery('tasks', backend='amqp', broker='amqp://guest@192.168.1.100//')


def inputoutput(programname):
    """ Yields the combinations of input_string, output_string
    and description expected to pass for the given program.
    """
    print "xmlfilename: ",conf.program_dir+programname+".xml"
    tree = ET.parse(conf.program_dir+programname+".xml")
    root=tree.getroot()
    for test in root:
        if test.tag != 'test':
            continue
        input_str=test.find('input').text
        output_str=test.find('output').text
        description=test.find('description').text
        yield input_str,output_str,description 

@app.task
def progtest(user, programname):
    i=1
    result={}
    result.update({"user":user})
    result.update({"programname":programname}) 
    program_name=conf.program_dir+programname+'.xml'#getting program code  xml into program
    program_dir=conf.participant_dir+user+'/'+programname #getting program code into program
    
    # Get more info about the program
    tree = ET.parse(program_name)
    root=tree.getroot()
    program_score=int(root.find("score").text)
    program_timeout = root.find('time-limit')
    input_type = root.find('input-type')
    case_sensitive = root.find('case-sensitive')
    validation_program = root.find('validation-program')
    validation_program_info = root.find('validation-program-info')
    multi_line = root.find('multi-line')
    program_timeout = int(program_timeout.text) if program_timeout is not None else 5
    input_type = input_type.text if input_type is not None else 'text'
    case_sensitive = True if case_sensitive is not None and case_sensitive.text == 'true' else False
    validation_program = validation_program.text if validation_program is not None else None 
    validation_program_info = validation_program_info.text if validation_program_info is not None else ''
    multi_line = True if multi_line is not None and multi_line.text == 'true' else False
    # Compile the program
    with file('compilation error.txt','w') as fp:
         ret=subprocess.call(['/bin/bash','compile.sh'],cwd=program_dir,stderr=fp,stdout=fp)
    if ret!=0:
        with file('compilation error.txt','r') as fp:
            error=fp.read()
            your_score=0
            result.update({"user":user})
            result.update({"programname":programname}) 
            result.update({"progstatus":'COMPILATION FAILED'})
            result.update({"description":error})
            result.update({"score":your_score})
        return result        
    # Execute the test cases
    p_pass=[]
    p_fail=[]
    p_error=[]
    # Hard_code_warning
    inputs_found = 0
    total_inputs = 0
    for input_i,output_o,description_d in inputoutput(programname):
    # Create the command to run.  In case of file inputs, make
    # sure filenames are formatted for {pdir}
        run_cmd = ['/bin/bash','run.sh']
        additional_args = shlex.split(input_i)
        for each_arg in additional_args:
            null_file = file('/dev/null','w')
            is_found = subprocess.call('grep %s *' % each_arg, shell=True, cwd=program_dir, stdout=null_file, stderr=null_file)
            if is_found == 0:
                inputs_found += 1
            total_inputs += 1
        if input_type == 'filename':
            additional_args = [x.format(pdir=conf.program_dir[0:-1]) for x in additional_args]
        run_cmd.extend(additional_args)
        try:
            cmd_op = timed_execution.check_output_with_timeout(run_cmd, cwd=program_dir, timeout=program_timeout)
            cmd_op=cmd_op.strip()
            if not case_sensitive:
                cmd_op = cmd_op.lower()
            program_passed = False
            if validation_program is None:
                if not multi_line:
                    program_passed = (cmd_op == output_o)
                else:
                    expected_lines = sorted(x.strip() for x in output_o.split('\n'))
                    actual_lines = sorted(x.strip() for x in cmd_op.split('\n'))
                    expected_lines = filter(lambda x:x, expected_lines)
                    actual_lines = filter(lambda x:x, actual_lines)
                    if len(expected_lines) != len(actual_lines):
                        print "line count mismatch"
                        program_passed = False
                    else:
                        for el, al in zip(expected_lines, actual_lines):
                            if el!=al:
                                program_passed = False
                                print "line mismatch %s and %s" % (el, al)
                                break
                            else:
                                program_passed = True
            else:
                i_file = 'validation_program_inputs.json'
                with file(i_file, 'w') as fp:
                    json.dump({'inputs': additional_args,
                           'output':cmd_op,
                           'info': validation_program_info}, fp)
                with file('validation_program_output.txt', 'w') as fp:
                    prog_path = '{pdir}{pcode}'.format(pdir=conf.program_dir, pcode=validation_program)
                    validation_result = subprocess.check_call(['python', prog_path, i_file])
                    if validation_result == 0:
                        program_passed = True
                    else:
                        program_passed = False
            if program_passed:
                p_pass.append('%s %s [successful]' %(description_d, programname)) 
            else:
                p_fail.append('%s %s [failed]' %(description_d, programname))  
                if case_sensitive:
                    p_fail.append(' Actual output ')
                else:
                    p_fail.append(' Actual output (in lower case) ')
                p_fail.append(cmd_op)
                p_fail.append(' Expected output ')
                p_fail.append(output_o)
                if input_type == 'filename':
                    p_fail.append(' Input Provided (file content) ')
                else:
                    p_fail.append(' Input Provided (args) ')
                p_fail.append(input_i)            
        except Exception as ex:
            p_error.append('%s %s [error]' %(description_d, programname))
            p_error.append(str(ex))  
    if len(p_pass) == 0:
        result.update({"progstatus":"FAIL"})
        your_score = 0
        result.update({"description":p_fail})
        result.update({"score":your_score})    
    # insert record the db as execution failed
    elif len(p_fail)+len(p_error)==0:   
        result.update({"progstatus":"SUCCESSFUL"})
        result.update({"description":p_pass})
        result.update({"score":program_score})
    # insert record the db as execution sucess
    else:
        result.update({"progstatus":"PARTIALLY SUCCESSFUL"})
        result.update({"description":p_error})
        partial = root.find('partial')
        if partial and partial.text == 'true':
            your_score = (program_score * len(p_pass)) / (len(p_pass) + len(p_fail) + len(p_error))
            result.update({"score":your_score})
            # insert record the db as patial is allowed
        else:
            your_score = 0
            result.update({"score":your_score})
            # insert record the db as patial is not allowed
        '''if (inputs_found*100)/total_inputs > 25:
            your_score = 0
        result1[user].append('WARNING for program %s' % program_name)
            result1[user].append("Too may inputs found in the directory")
        result1[user].append("If this is not intentional clean up your directory and remove hard coded inputs")'''

    return (result)