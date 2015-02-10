import subprocess
import time

def check_output_with_timeout(*args, **kwargs):
    timeout = kwargs.pop('timeout', 5)    
    outputs = ""
    p = subprocess.Popen(*args, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, **kwargs)
    while timeout > 0:
        result = p.poll()
        if result is not None:
            outputs, errors = p.communicate()
            if result == 0:
                print "------"
                print errors
                print outputs
                print "------"
                return outputs
            else:
                return "This program did not return zero error code: "+str(result)+"\n"+outputs+"\n"+errors
                #raise Exception('Program did not finish successfully. \n\n'+"".join([outputs,errors]))
        
        time.sleep(0.250)
        timeout -= 0.250

    p.kill()
    return "This program took longer than allowed time (%s)" % timeout + outputs
    #raise TimedoutException('Program did not finish in given time')

class TimedoutException(Exception):
    pass

