#!/usr/bin/env python
##############################################################################
# Copyright (c) Members of the EGEE Collaboration. 2004.
# See http://www.eu-egee.org/partners/ for details on the copyright
# holders.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at #
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################
#
# NAME :      gsutils
#
# DESCRIPTION : A library of useful functions for use with GStat
#
# AUTHORS :    Laurence.Field@cern.ch
#
# NOTES :
#
##############################################################################

import os
import sys
import getopt
import signal
import string
import re
import datetime

class error_logger:
   
    def __init__(self, source, error_messages):     
        self.source = str(source)
        self.error_messages = error_messages
        self.errors = []
      
    def log(self, entity_id, error_id, details, site_id):
        if (not self.error_messages.has_key(error_id)):
            sys.stderr.write("Error: Error ID '%s' is not defined." % (error_id))
            sys.exit(1)

        # Name, Type, EntityUniqueID, SiteID, Value, Source, Level          
        tuple = [ error_id, self.error_messages[error_id][0], entity_id, site_id, details, self.source, self.error_messages[error_id][1] ]
        self.errors.append(tuple)   

    def count(self):
        info_count = 0
        warning_count = 0
        error_count = 0
        for error in self.errors:
            if (error[6] == 'ERROR'):
                error_count += 1
            if (error[6] == 'WARNING'):
                warning_count += 1
            if (error[6] == 'INFO'):
                info_count += 1
        return [ error_count, warning_count, info_count ]

    def summary(self):
        my_count = self.count()
        errors = int(my_count[0])
        warnings = int(my_count[1])
        info = int(my_count[2])
        if (errors > 0):
            state = 'ERROR'
        elif (warnings > 0):
            state = 'WARNING'
        else:
            state = 'OK'
        for error in self.errors:
            print "%s: %s, %s, %s" % (error[6], error[2], error[1], error[4])

        print "%s - errors %i, warnings %i, info %i" % (state, errors, warnings, info) 
        
    def nagios(self):
        my_count = self.count()
        errors = int(my_count[0])
        warnings = int(my_count[1])
        info = int(my_count[2])
        if (errors > 0):
            state = 'CRITICAL'
        elif (warnings > 0):
            state = 'WARNING'
        else:
            state = 'OK'
       
        print "%s - errors %i, warnings %i, info %i | errors=%i;warnings=%i;info=%i" % (state, errors, warnings, info, errors, warnings, info) 
        i = 0

        for level in ["ERROR", "WARNING", "INFO"]:
            for error in self.errors:
                #Only return 100 lines if using Nagios
                if (i > 99 ):
                    missing = len(self.errors) - 100
                    print "Supressing %s more lines of output to be kind to Nagios." %(missing)
                    return
                if ( level == error[6] ):
                    print "%s: %s, %s, %s" % (error[6], error[2], error[1], error[4])
                    i+=1
                    
def parse_options():
   
    config = {}   

    config['debug'] = 0
    config['summary'] = False
    config['nagios'] = False
    config['output'] = None
   
    try:
        opts, args = getopt.getopt(sys.argv[1:], "H:p:b:f:d:o:t:sn", ["host", "port", "bind", "file", "debug", "output", "summary", "timeout", "nagios"])
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
        if o in ("-o", "--output"):
            config['output'] = a 
        if o in ("-t", "--timeout"):
            config['timeout'] = a 
        if o in ("-n", "--nagios"):
            config['nagios'] = True 
   
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

 -H --host     Hostname of the LDAP server.
 -p --port     Port for the LDAP server.
 -b --bind     The bind point for the LDAP server. 

File Mode: Obatins LDIF directly from a file.
 -f --file     An LDIF file

Output Options:
 -d --debug  Debug level 0-3, default 0
 -s --summary Displays a summary after runnning
 -n --nagios  Displays a nagios style output
 -t --timeout Placeholder for specifying a nagios timeout
''')
   
def get_config(file_name=None):
    if (not file_name):
        file_name = "/opt/gstat/etc/gstat.conf"
    config = {}
    if (os.path.exists(file_name)):
        for line in open(file_name).readlines():
            index = line.find("=") 
            if (index > -1):
                key = line[:index].strip()
                value = line[index + 1:].strip()
                config[key] = value
    return config

def read_ldif(name, port=None, bind=None, filter=None):

    # Open pipe to LDIF
    if (bind):
        command = "ldapsearch -LLL -x -h %s -p %s -b %s %s" % (name, port, bind, filter)
        pipe = os.popen(command)
    else:
        pipe = open(name)

    ldif = {}
    entry = {}
    attribute = "#"

    # Process LDIF
    for line in pipe:
         
        # Store entry if new dn is found.
        if (line[:3] == "dn:"):
            if (entry.has_key('dn')):
                dn = string.join(entry['dn'])
                entry.pop('dn')
                ldif[dn] = entry
            entry = {}
            attribute = "#"

        # Deal with wrapped lines
        if (line[0] == " "):
            if (entry.has_key(attribute)):
                # Remove the newline character
                line = line.replace("\n", "")
                index = len(entry[attribute]) - 1
                entry[attribute][index] = "%s%s" % (entry[attribute][index], line[1:])
            continue

        # Ignore comments
        if (line[0] == "#"):
            attribute = "#"
            continue

        index = line.find(":")
         
        # Ignore blank lines
        if (index == -1):
            continue

        # Remove the newline character
        line = line.replace("\n", "")

        # Split the attribute and value
        attribute = line[0:index]
        value = line[index + 2:]
         
        # Add to entry
        if (entry.has_key(attribute)):
            entry[attribute].append(value)
        else:
            entry[attribute] = []
            entry[attribute].append(value)

    if (entry.has_key('dn')):
        dn = string.join(entry['dn'])
        entry.pop('dn')
        ldif[dn] = entry

    # Close LDIF pipe
    pipe.close()

    return ldif

def get_site(dn):
    site = "Unknown"
    for value in dn.split(","):
        index = value.find("=")
        attribute = value[:index]
        if (attribute.lower() == "mds-vo-name"):
            site = value[index + 1:]
            break
    return site

def get_unique_id(dn):
    unique_id = "Unknown"
    for value in dn.split(","):
        index = value.find("=")
        attribute = value[:index]
        if (attribute.lower().find("uniqueid") > -1):
            unique_id = value[index + 1:]
            break
    return unique_id

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

def do_output(my_errors, config):

    if (config['nagios']):
        my_errors.nagios()
    else:
        my_errors.summary()

def do_exit(my_errors):
    # Exit with the correct return code
    my_count = my_errors.count()
    errors = my_count[0]
    warnings = my_count[1]
    info = my_count[2]
    if (errors > 0):
        sys.exit(2)
    elif (warnings > 0):
        sys.exit(1)
    else:
        sys.exit(0)

def get_nagios_status():
    """ This takes the nagios realtime status data and outputs as a dictionary object. """
    
    # config local access control permission to enable the file to be readbale by this script
    # Please note that it's HARD CODE for now!!!
    status_file="/var/nagios/status.dat"

    # store nagios status data in a dictionary object. 
    status = {}

    # fixme - the following token change dependiong on the version of Nagios 
    hosttoken='hoststatus'
    servicetoken='servicestatus'
    programtoken='programstatus'

    # The below dictionary are used for mapping all sorts of exit status codes.
    nagios_status_mapping = {
        '0': "OK",
        '1': "WARNING",
        '2': "CRITICAL",
        '3': "UNKNOWN"}
    
    # parse the nagios realtime status data and generate a dictionary
    
    # each host
    hosts = __GetDefinitions(status_file, hosttoken)
    services = __GetDefinitions(status_file, servicetoken)
    for hostdef in hosts:
        host_name          = __GetDirective(hostdef, "host_name")
        current_state      = __GetDirective(hostdef, "current_state")
        plugin_output      = __GetDirective(hostdef, "plugin_output")
        last_check         = __GetDirective(hostdef, "last_check")
        
        status[host_name]                  = {}
        status[host_name]['current_state'] = current_state
        status[host_name]['plugin_output'] = plugin_output
        status[host_name]['last_check']    = last_check

        for servicedef in services:
            if (__GetDirective(servicedef, "host_name") == host_name):
                service_description = __GetDirective(servicedef, "service_description")
                current_state       = __GetDirective(servicedef, "current_state")
                plugin_output       = __GetDirective(servicedef, "plugin_output")
                long_plugin_output  = __GetDirective(servicedef, "long_plugin_output")
                last_check          = __GetDirective(servicedef, "last_check")
                
                current_state_string = nagios_status_mapping[str(current_state)]
                
                status[host_name][service_description]                       = {}
                status[host_name][service_description]['current_state']      = current_state_string
                status[host_name][service_description]['plugin_output']      = plugin_output
                status[host_name][service_description]['long_plugin_output'] = long_plugin_output
                status[host_name][service_description]['last_check']         = last_check
                
    return status

def __GetDefinitions(filename, obj):
    """ Parse the status.dat file and extract matching object definitions """
    try:
        file = open(filename)
    except(IOError):
        print "Nagios realtime status file doesn't exist: %s" % filename
        sys.exit()
        
    content = file.read().replace("\t"," ")
    file.close
    pat = re.compile(obj +' \{([\S\s]*?)\}',re.DOTALL)
    finds = pat.findall(content)
    return finds

def __GetDirective(item, directive):
    """ parse an object definition, return the directives """
    pat = re.compile(' '+directive + '[\s= ]*([\S, ]*)\n')
    m = pat.search(item)
    if m:
        return m.group(1).strip()
    
