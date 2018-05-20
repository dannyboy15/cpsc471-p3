import utils
# import commands
import subprocess as sp

def print_cmd(cmd, desc):
    print "{command} {description}".format(\
        command = cmd.ljust(16),\
        description = desc)

def do_help():
    print "The following commands are available:"
    print_cmd('get <file name>', '(downloads <file name> from the server)')
    print_cmd('put <file name>', '(uploads <file name> to the server)')
    print_cmd('ls', '(lists files on the server)')
    print_cmd('lls', '(lists files on the client)')
    print_cmd('quit', '(disconnects from the server and exits)')

def do_get(sock, num_bytes):
    return utils.get_all(sock, num_bytes)

def do_put(sock, file_name):
    file = open(file_name, "r")
    data = file.read()

    print 'sending this data', data
    utils.send_all(sock, data)

    return True


def do_ls():
    # sp.call(["ls", "-l"])
    output = sp.check_output('ls')
    print output

def do_lls():
    sp.call(["ls", "-l"])
