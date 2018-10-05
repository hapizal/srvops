#!/usr/bin/python
###################################################################################
# Exhange ssh key to nodes in order to make them having passwordless ssh connection 
# from master to nodes
####################################################################################
import os, pexpect,sys
import subprocess

def print_(khar):
    sys.stdout.write(khar); sys.stdout.flush()

def grs(n,kar):
    for i in xrange(0,n): sys.stdout.write(kar);sys.stdout.flush()
    print '\r'


file_=sys.argv[1]
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

with open(file_) as f:
    line=f.readline()
    cnt=1
    while line:
        line_=line.strip().split()
        ip=line_[0]
        usr=line_[1]
        passw=line_[3]
        port=line_[4]

        print_(">> Copying id_rsa_pub to Target %s"%ip)
        conn=pexpect.spawn('ssh-copy-id -i %s/.ssh/id_rsa.pub test@%s'%(host,ip))
        conn.expect("assword:")
        conn.sendline("%s"%passw)
        conn.close
        print '\r'

        conn_=pexpect.spawn("scp -P %s %s/.ssh/id_rsa.pub -o Pubkeyauthentication=no %s@%s:/home/%s/.ssh/authorized_keys"%(port,host,usr,ip,usr))
        conn_.expect("assword:");conn_.sendline("%s"%passw)
        grs(80,'-')
        print_("Key Exchange Done")
        print '\r'
grs(80,'-')
print_("Done")
grs(80,':')
