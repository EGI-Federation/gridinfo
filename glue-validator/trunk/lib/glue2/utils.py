#!/usr/bin/env python

import os
import sys
import getopt
import signal
import string
import re
import datetime

def parse_options():
    config = {}
    config['debug'] = 0
    config['output'] = None
   
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:b:f:d:o:",
          ["host", "port", "bind", "file", "debug"])
    except getopt.GetoptError:
        sys.stderr.write("Error: Invalid option specified.\n")
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-H", "--host"):
            config['host'] = a
        if o in ("-p", "--port"):
            config['port'] = a
        if o in ("-b", "--bind"):
            config['bind'] = a
        if o in ("-d", "--debug"):
            config['debug'] = a
        if o in ("-f", "--file"):
            config['file'] = a
   
    config['debug'] = int(config['debug'])
   
    if (config['debug'] > 3):
        sys.stderr.write("Error: Invalid logging level.\n")
        usage()
        sys.exit(1)
   
    config['debug'] = (4 - int(config['debug'])) * 10

    if ((config.has_key('port') or config.has_key('bind')) and config.has_key('file')):
        sys.stderr.write("Error: Can not specify both file and (port/bind) output options.\n")
        usage()
        sys.exit(1)
   
    if (not (config.has_key('host') or  config.has_key('file'))):
        sys.stderr.write("Error: Must specify file or host\n")
        usage()
        sys.exit(1)

    return config

# Funtion to print out the usage
def usage():
    sys.stderr.write('Usage: %s [OPTIONS] \n' % (sys.argv[0]))
    sys.stderr.write('''

Server Mode: Obtains LDIF from an OpenLDAP server.
 -g --host      Hostname of the LDAP server.
 -p --port      Port for the LDAP server.
 -b --bind      The bind point for the LDAP server. 

File Mode: Obtains LDIF directly from a file.
 -f --file      An LDIF file

Output Options:
 -d --debug     Debug level 0-3, default 0
''')
   
def get_config(file_name):
    config = {}
    if (os.path.exists(file_name)):
        for line in open(file_name).readlines():
            index = line.find("=") 
            if (index > -1):
                key = line[:index].strip()
                value = line[index + 1:].strip()
                config[key] = value
    return config

def handler(signum, frame):
    if (signum == 14):
        sys.stderr.write("Timed out while reading LDIF source\n")
        # Commit suicide
        process_group = os.getpgrp()
        os.killpg(process_group, signal.SIGTERM)
        sys.exit(1)

def fast_read_ldif(source):
    # Get pipe file descriptors
    read_fd, write_fd = os.pipe()

    # Fork
    pid = os.fork()

    if pid:
        
        # Close write file descriptor as we don't need it.
        os.close(write_fd)
     
        read_fh = os.fdopen(read_fd)
        raw_ldif = read_fh.read()
        result = os.waitpid(pid, 0)
        if (result[1] > 0):
            return ""
        raw_ldif = raw_ldif.replace("\n ", "")

        return raw_ldif

    else:
        
        # Close read file d
        os.close(read_fd)
        
        # Set process group
        os.setpgrp()
                
        # Setup signal handler
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(90)

        # Open pipe to LDIF
        if (source[:7] == 'ldap://'):
            url = source.split('/')
            host = url[2].split(':')[0]
            port = url[2].split(':')[1]
            filter = url[3].replace("?filter=", " ")
            command = "ldapsearch -LLL -x -h %s -p %s -b %s 2>/dev/null" % (host, port, filter)
            pipe = os.popen(command)

        elif(source[:7] == 'file://'):
            pipe = open(source[7:])
        else:
            pipe = os.popen(source)    

        raw_ldif = pipe.read()

        # Close LDIF pipe
        pipe.close()

        write_fh = os.fdopen(write_fd, 'w')
        write_fh.write(raw_ldif)
        write_fh.close()

        signal.alarm(0) # Disable the alarm
        sys.exit(0)

def get_dns(ldif):
    dns = {}
    last_dn_index = len(ldif)
    while (1):
        dn_index = ldif.rfind("dn:", 0, last_dn_index)
        if (dn_index == -1):
            break
        end_dn_index = ldif.find("\n", dn_index, last_dn_index) 
        dn = ldif[dn_index + 4 :end_dn_index].lower() 
        end_entry_index = ldif.find("\n\n", dn_index, last_dn_index) 
        dns[dn] = (dn_index, last_dn_index)
        last_dn_index = dn_index
    return dns

def convert_entry(entry_string):
    entry = {}
    for line in entry_string.split("\n"):
        index = line.find(":")
        if (index > -1):
            attribute = line[:index]
            value = line[index + 2:]
            if (entry.has_key(attribute)):
                entry[attribute].append(value)
            else:
                entry[attribute] = [value]
                
    return entry

