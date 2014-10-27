import psutil
import time
from configobj import ConfigObj

config = ConfigObj('affinityd.ini')

nameList = config['exes']
sleepTime = float(config['sleep'])

if nameList == '':
    raise 'No exes specified.'
if type(nameList) == str:
    nameList = [nameList]

while True:
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['name', 'cmdline'])
        except psutil.NoSuchProcess:
            pass
        else:
            path = None
            if pinfo['cmdline']:
                path = pinfo['cmdline'][0]
            if pinfo['name'] in nameList or path in nameList:
                if len(proc.cpu_affinity()) > 1:
                    print pinfo['name'] + ' locked to a single core.'
                    proc.cpu_affinity([0])
    time.sleep(sleepTime)
