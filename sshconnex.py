#!/usr/bin/python
#########################################################################
# For execute many servers using ssh connection
# file list of the server info :
# ip<space>username<space>password<space>port<space>rootpassword
########################################################################

import pexpect
import sys,re,os

### function for line
def grs(n,kar):
    for i in xrange(0,n): sys.stdout.write(kar);sys.stdout.flush()
    print '\r'


### Read input
comm=raw_input("Command to Execute :\n")
file_=sys.argv[1]

### Read line by line from file targeted to take access info
with open(file_) as f:
    line=f.readline()
    cnt=1
    while line:
        line_=line.strip().split()
        ip=line_[0]
        usr=line_[1]
        passw=line_[2]
        port=line_[3]
        passr=line_[4]
        
        grs(80,'-')
        print 'Trying to Connect to',ip
        grs(80,'-')
        ### connecting by ssh protocol
        conn=pexpect.spawn("ssh -p %s %s@%s"%(port,usr,ip))
        try:
            ### give the password
            conn.expect("assword:",timeout=3)
            conn.sendline(passw)

            print "Logged In to ",ip
            grs(80,'-')
            ### detect login status
            conn.expect(["~]","~>"],timeout=3)
            print 'Execute Command :',comm
            grs(80,'-')
            ### send command to targeted server
            conn.sendline(comm)
            conn.expect(["~]","~>"],timeout=3)
            ### create, write to temp file
            filename='/var/tmp/ptest-%s.txt'%ip
            files=open(filename,'w')
            files.write(conn.before)
            files.close()
            ### filtering command output
            for linet in open(filename):
                if not comm in linet:
                    if not usr in linet:
                        sys.stdout.write("> %s"%linet); sys.stdout.flush()
            conn.close()
            ### remove temp file
            os.remove(filename)

        except pexpect.TIMEOUT:
            print("Timeout,Failed To Connect!!!")
        print '\r'
        line=f.readline()
        cnt+=1
