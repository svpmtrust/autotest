import subprocess
import time

def check_output_with_timeout(*args, **kwargs):
    timeout = kwargs.pop('timeout', 5)    
    p = subprocess.Popen(*args, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, **kwargs)
    while timeout > 0:
        result = p.poll()
        if result is not None:
            outputs, errors = p.communicate()
            if result == 0:
                return outputs
            else:
                raise Exception('Program did not finish successfully. \n\n'+"".join([outputs,errors]))
        
        time.sleep(0.250)
        timeout -= 0.250

    p.kill()
    raise TimedoutException('Program did not finish in given time')

class TimedoutException(Exception):
    pass

