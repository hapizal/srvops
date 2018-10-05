#!/usr/bin/python

import os, pexpect,sys
import subprocess

def print_(khar):
    sys.stdout.write(khar); sys.stdout.flush()

def grs(n,kar):
    for i in xrange(0,n): sys.stdout.write(kar);sys.stdout.flush()
    print '\r'

ip="192.168.19.129"
host=subprocess.check_output('hostname',shell=True)
home=subprocess.check_output('echo $HOME',shell=True)

grs(80,'-')
print_('This Server is : %s'%host)
print_(os.popen("date").read())
grs(80,'-')
print_(">> Generate ssh keygen from this Server %s"%host)
grs(80,'-')

os.system("ssh-keygen")
grs(80,'-')
print_(">> Copying id_rsa_pub to Target %s"%ip)

conn=pexpect.spawn('ssh-copy-id -i /home/hottofu/.ssh/id_rsa.pub test@%s'%ip)
#conn=pexpect.spawn('cat ~/.ssh/id_rsa_pub | ssh test@%s "cat >> ~/.ssh/authorized_keys"'%ip)
conn.expect("assword:")
conn.sendline("test")
conn.close
print '\r'

conn_=pexpect.spawn("scp -P 22 /home/hottofu/.ssh/id_rsa.pub -o Pubkeyauthentication=no test@192.168.19.129:/home/test/.ssh/authorized_keys")
#conn_=pexpect.spawn("cat /home/hottofu/.ssh/id_rsa.pub | ssh test@192.168.19.129 'cat >> /home/test/.ssh/authorized_keys'")
conn_.expect("assword:");conn_.sendline("test")
grs(80,'-')
print_("Done")
print '\r'
