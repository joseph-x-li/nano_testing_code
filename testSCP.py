from paramiko import SSHClient
from scp import SCPClient
import time




def timer(function):
    start = time.time()
    function()
    end = time.time()
    print("Elapsed Time: {}".format(end - start))

@timer
def setup():
    global ssh
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect('172.16.0.38', username = 'jet1', password = '1990')
    global scp 
    scp = SCPClient(ssh.get_transport())

@timer
def test():
    scp.get('/home/jet1/nano_testing_code/full_code/images/frame1.jpg')

setup
test
scp.close()