import os
import sys
import getopt
import signal
import string
import re
import datetime
import validator.messages

def parse_options():
    config = {}
    config['debug'] = 0
    config['output'] = None
    config['testsuite'] = 'egi-profile'
    config['separator'] = "\n"
    config['nagios'] = True
    config['glue-version'] = 'egi-glue2'
   
    try:
        opts, args = getopt.getopt(sys.argv[1:], "H:p:b:f:v:g:s:t:r:knVh",
          ["hostname=", "port=", "bind=", "file=", "verbosity=", "glue-version=", 
           "testsuite=", "timeout=", "separator=", "exclude-known-issues", "nagios", "version", "help"])
    except getopt.GetoptError:
        sys.stderr.write("Error: Invalid option specified.\n")
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-H", "--hostname"):
            config['hostname'] = a
        if o in ("-p", "--port"):
            config['port'] = a
        if o in ("-b", "--bind"):
            config['bind'] = a
        if o in ("-v", "--verbosity"):
            config['verbosity'] = a
        if o in ("-f", "--file"):
            config['file'] = a
        if o in ("-g", "--glue-version"):
            config['glue-version'] = a
        if o in ("-s", "--testsuite"):
            config['testsuite'] = a
        if o in ("-n", "--nagios"):
            config['nagios'] = True
        if o in ("-t", "--timeout"):
            config['timeout'] = a
        if o in ("-r", "--separator"):
            config['separator'] = a
        if o in ("-V", "--version"):
            sys.stdout.write("glue-validator version 2.0.23\n")
            sys.exit()
        if o in ("-k", "--exclude-known-issues"):
            config['exclude-known-issues'] = True
        if o in ("-h", "--help"):
            usage()
            sys.exit()

    if ( not (config.has_key('hostname') or config.has_key('file'))):
        sys.stderr.write("Error: Must specify a hostname or file\n")
        usage()
        sys.exit(1)

    if ( (config.has_key('hostname') and config.has_key('file'))):
        sys.stderr.write("Error: Must specify either hostname or file\n")
        usage()
        sys.exit(1)

    if ( (config.has_key('hostname') and not config.has_key('port'))):     
        sys.stderr.write("Error: Must specify a port\n")
        usage()
        sys.exit(1)
    
    if ( config.has_key('hostname') and not (config.has_key('bind'))):     
        sys.stderr.write("Error: Must specify a bind\n")
        usage()
        sys.exit(1)

    if config.has_key('verbosity'):
        config['verbosity'] = int(config['verbosity'])
        if (config['verbosity'] > 3):
            sys.stderr.write("Error: Invalid logging level\n")
            usage()
            sys.exit(1)
   
    if ((config.has_key('port') or config.has_key('bind')) and config.has_key('file')):
        sys.stderr.write("Error: (port/bind) options are needed by hostname only\n")
        usage()
        sys.exit(1)
   
    if config.has_key('glue-version'):
        if not config['glue-version'] in ['glue2', 'glue1', 'egi-glue2']:
            sys.stderr.write("Error: Invalid schema version %s.\n" %(config['glue-version'],))
            usage()
            sys.exit(1)
    else:
        config['glue-version']='egi-glue2' 

    if config.has_key('testsuite'):
        if not config['testsuite'] in ['general', 'wlcg', 'egi-profile', 'lhcb']:
            sys.stderr.write("Error: Invalid testsuite type %s.\n" %(config['testsuite'],))
            usage()
            sys.exit(1)
    else:
        config['testsuite']='egi-profile'

    if not config.has_key('timeout'):
        config['timeout']=10
    else:
        if (config['timeout'].isdigit()):
            config['timeout']=int(config['timeout'])
        else:
            sys.stderr.write("Error: Timeout should be a number.\n")
            usage()
            sys.exit(1)

    # Sanity Checks
    if config['glue-version'] in ['glue1', 'glue2'] and (config['testsuite'] == 'egi-profile'):
            sys.stderr.write("Error: egi-profile testsuite must be executed against the egi-glue2 schema version.\n")
            usage()
            sys.exit(1)
    if (config['separator'] != "\n" and not config.has_key('verbosity')) or \
       (config['separator'] != "\n" and config.has_key('verbosity') and config['verbosity'] != 3):
            sys.stderr.write("Error: Separator option is only available for verbosity level 3.\n")
            usage()
            sys.exit(1)
  
    return config

# Funtion to print out the usage
def usage():
    sys.stderr.write('Usage: %s [LDIF OPTIONS] [-g] [-s] [Other Options]\n' % (sys.argv[0]))
    sys.stderr.write('''

Mandatory Arguments:

Server Mode: Obtains LDIF from an OpenLDAP server
 -H --hostname      Hostname of the LDAP server
 -p --port          Port for the LDAP server
 -b --bind          The bind point for the LDAP server

File Mode: Obtains LDIF directly from a file
 -f --file          An LDIF file

Optional Arguments:

GLUE version: Selects the GLUE schema version to be tested
 -g --glue-version        The glue schema version to be tested [glue1|glue2|egi-glue2 (default)]

Tesuite type: Selects the set of tests to be executed against the LDIF
 -s --testsuite     The testsuite  [general|lhcb|egi-profile (default)]

Other Options:
 -k --exclude-known-issues  Do not run tests for wrongly published attributes due to known bugs
 -t --timeout               glue-validator runtime timeout, default 10s 
 -v --verbose               Verbosity level 0-3, default 0
 -r --separator             Defines the separator for the output messages, default \\n
                            This is only available for the verbosity level 3.
 -V --version               Prints glue-validator version
 -h --help                  Prints glue-validator usage

Examples:

  GLUE 1.3 validation: glue-validator -H localhost -p 2170 -b o=grid -g glue1
  GLUE 2.0 validation: glue-validator -H localhost -p 2170 -b o=glue -g glue2
  EGI profile against GLUE 2.0 validation: glue-validator -H localhost -p 2170 -b o=glue 

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
        sys.stdout.write("UNKNOWN - Timed out\n")
        # Commit suicide
        process_group = os.getpgrp()
        os.killpg(process_group, signal.SIGTERM)
        sys.exit(3)

def fast_read_ldif(source,timeout):
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
        signal.alarm(timeout)

        # Open pipe to LDIF
        if (source[:7] == 'ldap://'):
            url = source.split('/')
            host = url[2].split(':')[0]
            port = url[2].split(':')[1]
            bind = url[3]
            count=4
            while count < len(url):
                bind = bind + "/" + url[count]
                count = count + 1 
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

def nagios_output(debug_level,file):

   config = parse_options()
   try:
       results = open(file,'r')
       count = {'INFO':0,'WARNING':0,'ERROR':0}
       messages = {'INFO':[],'WARNING':[],'ERROR':[]}
       summary = {}
       for line in results:

          # Process new error, warning or info block
          if line.find("INFO START:") > -1 or line.find("WARNING START:") > -1 or line.find("ERROR START:") > -1:
             matched=re.search(r'(INFO|WARNING|ERROR)',line)
             if matched is not None:
                match_string=matched.group()
                count[match_string] += 1
                extra_line = line.replace("AssertionError: %s START:" % match_string," ")
                while extra_line.find("END") == -1: 

                    # If separator is a newline, print the DN in different lines as well 
                    if config['separator'] == "\n" and extra_line.find("Affected DN") > -1:
                        DN = extra_line.split(",")
                        for i, element in enumerate(DN): 
                            messages[match_string].append(element)
                            if i != len(DN) - 1:
                                messages[match_string].append("\n                  ")
                    else:
                        messages[match_string].append(extra_line)
                    old_line = extra_line
                    extra_line = results.next()

                # Summary per attribute and value
                code=re.search(r'(I...|W...|E...)',old_line)
                if code is not None:
                    code_string=code.group()
                    if code_string in summary:
                        summary[code_string] += 1
                    else:
                        summary[code_string] = 1
                messages[match_string].append("\n")

       results.close()
       os.remove(file)
   except IOError:
       os.remove(file)
       print "UNKNOWN - glue-validator failed to parse the error messages!"
       sys.exit(3)
   
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
  
   if debug_level == 2:
       sys.stdout.write("Summary per type of error, warning and info message:\n")
       for i in sorted(summary.keys()):
           sys.stdout.write("%s - %s (%s): " % (i, validator.messages.messages[i][0], validator.messages.messages[i][1]))
           sys.stdout.write("%i\n" % summary[i])

   if debug_level == 3:
      maxlines=100
      for i in ['ERROR','WARNING','INFO']:   
         for line in messages[i]:
            sys.stdout.write (line)
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


def message_generator ( type , code , dn , attribute , value , extra_info="" ):

    config = parse_options()
    separator = config['separator']
    #separator = "\n"
    message = ("%s START:%s"
               "%s Description: %s%s"
               "%s Affected DN: %s%s"
               "%s Affected attribute: %s%s"
               "%s Published value: %s ") %\
              ( type, separator,\
                code, validator.messages.messages[code][0], separator,\
                code, dn, separator,\
                code, attribute, separator,\
                code, value )
    if extra_info != "":
        message = message + ("%s%s Additional information: %s\n") % ( separator, code, extra_info )
    else:
        message = message + "\n"

    message = message + "%s END\n" % ( type )
              
    return message 
