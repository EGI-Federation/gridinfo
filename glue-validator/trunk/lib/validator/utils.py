import os
import sys
import getopt
import signal
import string
import re
import datetime
from collections import defaultdict

def parse_options():
    config = {}
    config['debug'] = 0
    config['output'] = None
    config['testsuite'] = 'general'
   
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:b:f:d:o:t:s:n",
          ["host", "port", "bind", "file", "debug", "test", "testsuite", "nagios"])
    except getopt.GetoptError:
        sys.stderr.write("Error: Invalid option specified.\n")
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--host"):
            config['host'] = a
        if o in ("-p", "--port"):
            config['port'] = a
        if o in ("-b", "--bind"):
            config['bind'] = a
        if o in ("-d", "--debug"):
            config['debug'] = a
        if o in ("-f", "--file"):
            config['file'] = a
        if o in ("-t", "--test"):
            config['test'] = a
        if o in ("-s", "--testsuite"):
            config['testsuite'] = a
        if o in ("-n", "--nagios"):
            config['nagios'] = True
   
    config['debug'] = int(config['debug'])
   
    if (config['debug'] > 3):
        sys.stderr.write("Error: Invalid logging level.\n")
        usage()
        sys.exit(1)
   
    if ((config.has_key('port') or config.has_key('bind')) and config.has_key('file')):
        sys.stderr.write("Error: Can not specify both file and (port/bind) output options.\n")
        usage()
        sys.exit(1)
   
    if (not (config.has_key('host') or  config.has_key('file'))):
        sys.stderr.write("Error: Must specify file or host\n")
        usage()
        sys.exit(1)

    if config.has_key('test'):
        if not config['test'] in ['glue2', 'glue1', 'egi-glue2']:
            sys.stderr.write("Error: Invalid test class %s.\n" %(config['test'],))
            usage()
            sys.exit(1)
    else:
        sys.stderr.write("Error: Must specify a test class.\n")
        usage()
        sys.exit(1)

    if config.has_key('testsuite'):
        if not config['testsuite'] in ['general', 'wlcg', 'egi-profile']:
            sys.stderr.write("Error: Invalid testsuite class %s.\n" %(config['testsuite'],))
            usage()
            sys.exit(1)
    else:
        config['testsuite']='general'

    # Sanity Checks
    if config['test'] == 'glue1' and ( config['bind'].find('o=glue') != -1 ): 
            sys.stderr.write("Error: Use a glue 1 binding containing o=grid.\n")
            usage()
            sys.exit(1)
    if config['test'] == 'glue2' and ( config['bind'].find('o=grid') != -1 ):
            sys.stderr.write("Error: Use a glue 2 binding containing o=glue.\n")
            usage()
            sys.exit(1)
    if config['test'] in ['glue1', 'glue2'] and (config['testsuite'] == 'egi-profile'):
            sys.stderr.write("Error: egi-profile testsuite must be executed against the egi-glue2 schema.\n")
            usage()
            sys.exit(1)

    return config

# Funtion to print out the usage
def usage():
    sys.stderr.write('Usage: %s -t <test class> [OPTIONS] \n' % (sys.argv[0]))
    sys.stderr.write('''
 -t --test        The glue schema version to be tested [glue1|glue2|egi-glue2].

OPTIONS:

Server Mode: Obtains LDIF from an OpenLDAP server.
 -h --host      Hostname of the LDAP server.
 -p --port      Port for the LDAP server.
 -b --bind      The bind point for the LDAP server. 

File Mode: Obtains LDIF directly from a file.
 -f --file      An LDIF file

Tesuite type: Selects the set of tests to be executed against the LDIF.
 -s --testsuite   The testsuite  [general (default)|wlcg|egi-profile].

Nagios output: Indicates whether the command should produce Nagios output.
               This is only available for the egi-profile testsuite.
 -n --nagios

Other Options:
 -d --debug     Debug level 0-3, default 0

Examples:

  glue-validator -t glue1 -h localhost -p 2170 -b o=grid -s wlcg
  glue-validator -t glue2 -h localhost -p 2170 -b o=glue
  glue-validator -t egi-glue2 -h localhost -p 2170 -b o=glue -s egi-profile -n

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
            bind = url[3]
            command = "ldapsearch -LLL -x -h %s -p %s -b %s 2>/dev/null" % (host, port, bind)
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
        dn = ldif[ dn_index + 4 : end_dn_index ].lower() 
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

def nagios_output(debug_level):

   if os.path.exists('/var/lib/grid-monitoring/glue-validator/glue-validator'):
      results=open("/var/lib/grid-monitoring/glue-validator/glue-validator","r")
   else:
      sys.stderr.write("Error: File /var/lib/grid-monitoring/glue-validator/glue-validator does not exist\n")
      sys.exit(1)

   count = defaultdict(int)
   messages = defaultdict(list)
   for line in results:
      matched=re.search(r'(INFO|WARNING|ERROR)',line)
      if matched is not None:
         match_string=matched.group()
         count[match_string] += 1
         messages[match_string].append(line.strip("AssertionError:"))

   results.close()

   errors = count['ERROR']
   warnings = count['WARNING']
   info = count['INFO']
   if (errors > 0):
     state = 'CRITICAL'
   elif (warnings > 0):
     state = 'WARNING'
   else:
     state = 'OK'

   print "%s - errors %i, warnings %i, info %i | errors=%i;warnings=%i;info=%i" % \
         (state, errors, warnings, info, errors, warnings, info)

   if debug_level == 3:
      maxlines=100
      for i in ['ERROR','WARNING','INFO']:   
         for line in messages[i]:
            print line
            maxlines =- 1
            if maxlines == 0:
               break
         maxlines =-1
         if maxlines == 0:
           break

   if (errors > 0):
     sys.exit(2)
   elif (warnings > 0):
     sys.exit(1)
   else:
     sys.exit(0)

