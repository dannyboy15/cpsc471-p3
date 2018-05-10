import utils
# import commands
import subprocess

def do_help():
    print "The following commands are available"
    print "get <file name> (downloads <file name> from the server)"
    print "put <file name> (uploads <file name> to the server)"
    print "ls (lists files on the server)"
    print "lls (lists files on the client)"
    print "quit (disconnects from the server and exits)"

def do_get(sock, num_bytes):
    return get_all(sock, num_bytes)

def do_put(sock, file_name):
    file = open(file_name, "r")
    data = file.read()

    return True


def do_ls():
    datta
    for line in commands.getstatusoutput('ls -l'):
    	print line

def do_lls():
    for line in commands.getstatusoutput('ls -l'):
    	print line
