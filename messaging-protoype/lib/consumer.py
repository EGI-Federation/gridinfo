#!/usr/bin/env python

# P.J. Harvey
# jhebus@gmail.com

import stomp
import sys
import time
import thread
import os
import socket
import threading
from threading import Thread

from mylib import get_dns, group_dns, read_ldif
import tempfile

#Features for logging, specified in main
import logging
LEVELS = {'debug'	: logging.DEBUG,
          'info'	: logging.INFO,
          'warning'	: logging.WARNING,
          'error'	: logging.ERROR,
          'critical'	: logging.CRITICAL}
LOG_FILENAME 		= 'bdii-consumer.log'
DEBUG_LEVEL		= "debug"


HOST='gridmsg001.cern.ch'
#HOST='vtb-generic-26.cern.ch'
PORT=6163
HEADERS={}
N=0
config = {'BDII_LOG_LEVEL'	:	None,
	  'BDII_ARCHIVE_SIZE'	:	0}


#LDAP database parameters (Hardcoded for the moment)
DB_HOSTNAME            = "lxbra2104"
DB_PORT                = "2170"
DB_PASSWORD            = "f0ZZmy2bx"
DB_ROOT_NAME           = "o=grid"
ERROR_FILE             = "/root/messaging/test/error.txt" #"/home/jhebus/Desktop/error.txt"#
DIRECTORY_LOCATION     = "."

#General Parameters
MY_SYNC_LIST           = "/topic/" + socket.gethostname()
SYNC_MODE              = True

#List of Provider objects, representing those providers who we know about
providers = []

#List of the names of the providers we are syncing from
#Required to prevent duplicated sync requests in the initial state
sync_providers = []


lock=thread.allocate_lock()

#Locks for the different processes
add_lock = thread.allocate_lock()
del_lock = thread.allocate_lock()
mod_lock = thread.allocate_lock()

#condition variables
add_cond = threading.Condition(add_lock)
del_cond = threading.Condition(del_lock)
mod_cond = threading.Condition(mod_lock)


# buffer
op_queue = []

q_event = threading.Event()
q_lock = thread.allocate_lock()
q_cond = threading.Condition(q_lock)

################################################################################
def q_processor(string,sleeptime,*args):

    num_to_be_removed = 0

    while True:


        logging.debug( "PROCESSOR: Get lock")
        #get the q lock
        q_cond.acquire()
        logging.debug( "PROCESSOR: Got lock")

        logging.debug( "PROCESSOR: Wait for the q to fill")
        #While the q is empty, wait
        while not op_queue:
            q_cond.wait()

        num_to_be_removed = 0
        
        logging.debug( "PROCESSOR: Something in the q")
        #Process the q
        for op in op_queue:

                logging.debug(("PROCESSOR: current seq_num %i " % op.seq_num()))

                #Normal modification
                if(op.get_type() == "/topic/modification/"):
                        logging.debug( "PROCESSOR: MODIFICATION : %i"%num_to_be_removed)
                        #logging.debug((num_to_be_removed))
                        handle_modification(op.get_action())
                        num_to_be_removed += 1

                #Normal addition
                elif(op.get_type() == "/topic/addition/"):
                        logging.debug( "PROCESSOR: ADDITION : %i"%num_to_be_removed)
                        #logging.debug((num_to_be_removed))
                        handle_addition(op.get_action())
                        num_to_be_removed += 1

                #Normal deletion
                elif(op.get_type() == "/topic/deletion/"):
                        logging.debug( "PROCESSOR: DELETION :%i"%num_to_be_removed)
                        handle_deletion(op.get_action(), 0)
                        num_to_be_removed += 1
                        #logging.debug((num_to_be_removed))

                #Provider restarted, delete currecnt entries in the tree
                elif(op.get_type() == "/topic/re-deletion/"):
                        logging.debug( "PROCESSOR: Recursive Delete : %i"%num_to_be_removed)
                        handle_deletion(op.get_action(), 1)
                        num_to_be_removed += 1
                        #logging.debug((num_to_be_removed))

                #?.....
                else:
                        logging.debug( "PROCESSOR: There was an undefined message to be processed ")
                        logging.debug((op))
                        logging.debug((num_to_be_removed))
                        num_to_be_removed += 1


        for i in range(num_to_be_removed):
                op_queue.pop(0)


        logging.debug( "PROCESSOR: Release Lock")
        #Now release the lock and go round
        q_cond.release()

################################################################################
#Simple function that performs the ldapadd - NO CHECKS PERFORMED
def handle_addition(body):
	#print body

        try:
            logging.debug("ldapadd -d 256 -x -c -h %s -p %s -D %s -w %s >/dev/null 2>>%s" %(DB_HOSTNAME, DB_PORT, DB_ROOT_NAME, DB_PASSWORD, ERROR_FILE))

            input_fh=os.popen("ldapadd -d 256 -x -c -h %s -p %s -D %s -w %s >/dev/null 2>>%s" %(DB_HOSTNAME, DB_PORT, DB_ROOT_NAME, DB_PASSWORD, ERROR_FILE), 'w')
            input_fh.write("%s\n" % (body))
            input_fh.close()
            pass
        except IOError:
            logging.debug("Could not add new entries to the database.")
        
	
####################################################
#Simple function that performs the ldapmodify - NO CHECKS PERFORMED
def handle_modification(body):
	#print body

        try:
            logging.debug("ldapmodify -d 256 -x -c -h %s -p %s -D %s -w %s >/dev/null 2>>%s" %(DB_HOSTNAME, DB_PORT, DB_ROOT_NAME, DB_PASSWORD, ERROR_FILE))

            input_fh=os.popen("ldapmodify -d 256 -x -c -h %s -p %s -D %s -w %s >/dev/null 2>>%s" %(DB_HOSTNAME, DB_PORT, DB_ROOT_NAME, DB_PASSWORD, ERROR_FILE), 'w')
            input_fh.write("%s\n" % (body))
            input_fh.close()
            pass
        except IOError:
            logging.debug("Could not modify entries in the database.")

####################################################
#Simple function that performs the ldapdelete - NO CHECKS PERFORMED
def handle_deletion(body, recursive):
	#print body

        try:

            #if we should recursively delete the element and its subtree
            if recursive == 1:
                command = ("ldapdelete -d 256 -x -c -h %s -p %s -D %s -w %s -r >/dev/null 2>>%s" %(DB_HOSTNAME, DB_PORT, DB_ROOT_NAME, DB_PASSWORD, ERROR_FILE))
            else:
                command = ("ldapdelete -d 256 -x -c -h %s -p %s -D %s -w %s >/dev/null 2>>%s" %(DB_HOSTNAME, DB_PORT, DB_ROOT_NAME, DB_PASSWORD, ERROR_FILE))

            logging.debug(command)

            input_fh=os.popen(command, 'w')
            input_fh.write("%s\n" % (body))
            input_fh.close()
        except IOError:
            logging.debug("Could not delete old entries in the database.")
####################################################
def do_sync(hostname):

	new_ldif = ""
	logging.debug("request sync for hostname : %s"%hostname)
	
	#ldapsearch -LLL -x -h lxbra2104.cern.ch -p 2170 -b o=grid

	command = ("ldapsearch -LLL -x -h %s -p %s -b o=grid  " %(hostname, DB_PORT))
	
	input_fh	= os.popen(command, 'r')
	new_ldif 	= input_fh.read()
	input_fh.close()
	
	#logging.debug("Here, the result was : %s" % new_ldif)
	
        logging.info("Starting Update")
        stats={}
        stats['update_start'] = time.time()

        new_ldif=""
	
	if( config.has_key('FIX_GLUE')) and ( config['FIX_GLUE'] == 'yes'):
	    logging.debug("Doing Fix")
	    new_ldif = fix(new_dns, new_ldif)

	

		    
	logging.info("Reading old LDIF file ...")
	stats['read_old_start'] = time.time()
	old_ldif_file = "%s/old.ldif" % (DIRECTORY_LOCATION)
	if ( os.path.exists(old_ldif_file) ):
	    old_ldif = read_ldif("file://%s" % (old_ldif_file))
	else:
	    old_ldif = ""
	stats['read_old_stop'] = time.time()



	logging.debug("Starting Diff")
	print("start the diff")
	ldif_add=[]
	ldif_modify = ""
	ldif_delete=[]

	new_dns = get_dns(new_ldif)
	old_dns = get_dns(old_ldif)

	for dn in new_dns.keys():
	    if old_dns.has_key(dn):
	        old = old_ldif[old_dns[dn][0]:old_dns[dn][1]].strip()
	        new = new_ldif[new_dns[dn][0]:new_dns[dn][1]].strip()

	        # If the entries are different we need to compare them

	        #logging.debug("old string  :" + str(old))
	        #logging.debug("new string  :" + str(new))
	        if ( not new == old):
	            entry = ldif_diff(dn,old,new)
	            ldif_modify += entry

	        #logging.debug("the diff    :" + str(ldif_diff(dn,old,new)))
	    else:
	        ldif_add.append(dn)

	# Checking for removed entries
	for dn in old_dns.keys():
	    if not new_dns.has_key(dn):
	        ldif_delete.append(dn)
	
	logging.debug("Finished Diff")
	
	logging.debug("Sorting Add Keys")
	ldif_add.sort(lambda x, y: cmp(len(x), len(y)))

	"""
	The plan:

	*  Figure out how exactly scirpt is invoked and from where
	*  modify to include the use of messaging
	        jsut send the files inside message at first
	* Consult the papers to begin to consider what data can be split
	* Figure out the push/pull semantics
	
	"""
	logging.debug("now print the add enrtires")

	
	logging.debug("Writing ldif_add to disk")
	"""
	if ( config['BDII_LOG_LEVEL'] == 'DEBUG' ):
	    dump_fh=open("%s/add.ldif" % (DIRECTORY_LOCATION),'w')
	    for dn in ldif_add:
	        dump_fh.write(new_ldif[new_dns[dn][0]:new_dns[dn][1]])
	       
	        dump_fh.write("\n")
	    dump_fh.close()
	"""
	logging.debug("Adding New Entries")
	print("Adding New Entries")
	stats['db_update_start'] = time.time()

	#if ( config['BDII_LOG_LEVEL'] == 'DEBUG' ):
	#    error_file="%s/add.err" %(DIRECTORY_LOCATION)
	#else:
        error_file=tempfile.mktemp()

	roots = group_dns(ldif_add)
	
	add_error_counter = 0
	for root in roots.keys():
	    try:
	        input_fh=os.popen("ldapadd -d 256 -x -c -h %s -p %s -D %s -w %s >/dev/null 2>>%s" %(DB_HOSTNAME, DB_PORT, DB_ROOT_NAME, DB_PASSWORD, ERROR_FILE), 'w')
	        for dn in roots[root]:
	            input_fh.write(new_ldif[new_dns[dn][0]:new_dns[dn][1]])
	            #print(new_ldif[new_dns[dn][0]:new_dns[dn][1]])
	            input_fh.write("\n")
	        input_fh.close()
	    except IOError:
	        logging.error("Could not add new entries to the database.")
	        
  
	    add_error_counter += log_errors(error_file,ldif_add)

	    if ( not config['BDII_LOG_LEVEL'] == 'DEBUG' ):
	    	os.remove(error_file)
	                
	logging.debug("Writing ldif_modify to disk")
	if ( config['BDII_LOG_LEVEL'] == 'DEBUG' ):
	    dump_fh=open("%s/modify.ldif" % (DIRECTORY_LOCATION),'w')
	    dump_fh.write(ldif_modify)
	    dump_fh.close()

	logging.debug("Modify New Entries")
	print("Modify New Entries")
	if ( config['BDII_LOG_LEVEL'] == 'DEBUG' ):
	    error_file="%s/modify.err" % (DIRECTORY_LOCATION)
	else:
	    error_file=tempfile.mktemp()

	ldif_modify_dns = get_dns(ldif_modify)
	roots = group_dns(ldif_modify_dns)
	modify_error_counter = 0
	for root in roots.keys():
	    try:
	        input_fh=os.popen("ldapmodify -d 256 -x -c -h %s -p %s -D %s -w %s >/dev/null 2>>%s" %(DB_HOSTNAME, DB_PORT, DB_ROOT_NAME, DB_PASSWORD, ERROR_FILE), 'w')
	        for dn in roots[root]:
	            input_fh.write(ldif_modify[ldif_modify_dns[dn][0]:ldif_modify_dns[dn][1]])
	            #print(ldif_modify[ldif_modify_dns[dn][0]:ldif_modify_dns[dn][1]])
	            input_fh.write("\n")
	        input_fh.close()
	    except IOError:
	        logging.error("Could not modify entries in the database.")

	    modify_error_counter += log_errors(error_file, ldif_modify_dns.keys())

	    if ( not config['BDII_LOG_LEVEL'] == 'DEBUG' ):
	        os.remove(error_file)

	logging.debug("Sorting Delete Keys")
	ldif_delete.sort(lambda x, y: cmp(len(y), len(x)))

	logging.debug("Writing ldif_delete to disk")
	if ( config['BDII_LOG_LEVEL'] == 'DEBUG' ):
	    dump_fh=open("%s/delete.ldif" % (DIRECTORY_LOCATION),'w')
	    for dn in ldif_delete:
	        dump_fh.write("%s\n" % (dn))
	    dump_fh.close()

	logging.debug("Deleting Old Entries")
	print("Deleting Old Entries")
	if ( config['BDII_LOG_LEVEL'] == 'DEBUG' ):
	    error_file="%s/delete.err" % (DIRECTORY_LOCATION)
	else:
	    error_file=tempfile.mktemp()

	roots = group_dns(ldif_delete)
	delete_error_counter = 0
	for root in roots.keys():
	    try:
	        input_fh=os.popen("ldapdelete -d 256 -x -c -h %s -p %s -D %s -w %s >/dev/null 2>>%s" %(DB_HOSTNAME, DB_PORT, DB_ROOT_NAME, DB_PASSWORD, ERROR_FILE), 'w')
	        
	        for dn in roots[root]:
	            input_fh.write("%s\n" % (dn))
	            #print("%s\n" % (dn))
	        input_fh.close()
	    except IOError:
	        logging.error("Could not delete old entries in the database.")

	    delete_error_counter += log_errors(error_file, ldif_delete)

	    if ( not config['BDII_LOG_LEVEL'] == 'DEBUG' ):
	        os.remove(error_file)

	roots = group_dns(new_dns)
	stats['query_start'] = time.time()
	if ( os.path.exists("%s/old.ldif" % DIRECTORY_LOCATION) ):
	    os.remove("%s/old.ldif" % DIRECTORY_LOCATION)
	if ( os.path.exists("%s/old.err" % DIRECTORY_LOCATION) ):
	    os.remove("%s/old.err" % DIRECTORY_LOCATION)
	for root in roots.keys():
	    command = "ldapsearch -LLL -x -h %s -p %s -b %s >> %s/old.ldif 2>> %s/old.err" % (DB_HOSTNAME, DB_PORT, DB_ROOT_NAME, DIRECTORY_LOCATION, DIRECTORY_LOCATION )
	    #logging.debug("ldapsearch -LLL -x -h %s -p %s -b %s >> %s/old.ldif 2>> %s/old.err" % (config['BDII_HOSTNAME'], config['BDII_PORT'], root, DIRECTORY_LOCATION, DIRECTORY_LOCATION))

	    result = os.system(command)
	    if ( result > 0):
	        logging.error("Query to self failed.")
	stats['query_stop'] = time.time()
	out_file="%s/archive/%s-snapshot.gz" % (DIRECTORY_LOCATION, time.strftime('%y-%m-%d-%H-%M-%S'))
	logging.debug("Creating GZIP file")
	os.system("gzip -c %s/old.ldif > %s" %(DIRECTORY_LOCATION, out_file) )

	infosys_output=""
	if (len(old_ldif) == 0 ):
	    logging.debug("ldapadd o=infosys compression")
	    command="ldapadd"
	    
	    infosys_output+="dn: o=infosys\n"
	    infosys_output+="objectClass: organization\n"
	    infosys_output+="o: infosys\n\n"
	    infosys_output+="dn: CompressionType=zip,o=infosys\n"
	    infosys_output+="objectClass: CompressedContent\n"
	    infosys_output+="Hostname: %s\n" %(DB_HOSTNAME)
	    infosys_output+="CompressionType: zip\n"
	    infosys_output+="Data: file://%s\n\n" %(out_file)
	else:
	    logging.debug("ldapmodify o=infosys compression")
	    command="ldapmodify"

	    infosys_output+="dn: CompressionType=zip,o=infosys\n"
	    infosys_output+="changetype: Modify\n"
	    infosys_output+="replace: Data\n"
	    infosys_output+="Data: file://%s\n\n" %(out_file)
	    
	try:
	    output_fh = os.popen("%s -x -c -h %s -p %s -D o=infosys -w %s >/dev/null" %(command, DB_HOSTNAME, DB_PORT, DB_PASSWORD), 'w')
	    output_fh.write(infosys_output)
	    output_fh.close()
	except IOError:
	    logging.error("Could not add compressed data to the database.")

	old_files=os.popen("ls -t %s/archive" % (DIRECTORY_LOCATION) ).readlines()
	logging.debug("Deleting old GZIP files")
	for file in old_files[config['BDII_ARCHIVE_SIZE']:]:
	    os.remove("%s/archive/%s" % (DIRECTORY_LOCATION,file.strip()))

	stats['db_update_stop'] = time.time()
	stats['update_stop'] = time.time()

	stats['UpdateTime'] = int(stats['update_stop']
	                          - stats['update_start'])
	stats['ReadTime'] = int(stats['read_old_stop']
	                          - stats['read_old_start'])
	stats['ProvidersTime'] = 0 #int(stats['providers_stop']- stats['providers_start'])
	stats['PluginsTime'] = 	 0 #int(stats['plugins_stop']     - stats['plugins_start'])
	stats['QueryTime'] = int(stats['query_stop']
	                           - stats['query_start'])
	stats['DBUpdateTime'] = int(stats['db_update_stop']
	                           - stats['db_update_start'])
	stats['TotalEntries'] = len(old_dns) 
	stats['NewEntries'] =  len(ldif_add)
	stats['ModifiedEntries'] = len(ldif_modify_dns.keys())
	stats['DeletedEntries'] =  len(ldif_delete)
	stats['FailedAdds'] =  add_error_counter
	stats['FailedModifies'] = modify_error_counter
	stats['FailedDeletes'] = delete_error_counter

	for key in stats.keys():
	    if ( key.find("_") == -1 ):
	        logging.info("%s: %i" % (key, stats[key]) )

	infosys_output=""
	if (len(old_ldif) == 0 ):
	    logging.debug("ldapadd o=infosys updatestats")
	    command="ldapadd"

	    infosys_output+="dn: Hostname=%s,o=infosys\n" %(DB_HOSTNAME)
	    infosys_output+="objectClass: UpdateStats\n"
	    infosys_output+="Hostname: %s\n" %(DB_HOSTNAME)
	    for key in stats.keys():
	        if ( key.find("_") == -1):
	            infosys_output+="%s: %i\n" %(key, stats[key])
	    infosys_output+="\n"
	else:
	    logging.debug("ldapmodify o=infosys updatestats")
	    command="ldapmodify"

	    infosys_output+="dn: Hostname=%s,o=infosys\n" %(DB_HOSTNAME)
	    infosys_output+="changetype: Modify\n"
	    for key in stats.keys():
	        if ( key.find("_") == -1):
	            infosys_output+="replace: %s\n" %(key)
	            infosys_output+="%s: %i\n" %(key, stats[key])
	            infosys_output+="-\n"
	    infosys_output+="\n"
	try:
	    output_fh = os.popen("%s -x -c -h %s -p %s -D o=infosys -w %s >/dev/null" %(command, DB_HOSTNAME, DB_PORT, DB_PASSWORD), 'w')
	    output_fh.write(infosys_output)
	    output_fh.close()
	except IOError:
	    logging.error("Could not add stats entries to the database.")

	old_ldif = None
	new_ldif = None
	new_dns = None
	ldif_delete = None
	ldif_add = None
	ldif_modify = None
	
####################################################
class Backlog(object):
    sync_number = 0
    action = ""
    type   = ""


    def __init__(self, sync_number, action, type):
        self.sync_number = sync_number
        self.action = action
        self.type = type

    def seq_num(self):
        return self.sync_number

    def get_action(self):
        return self.action

    def get_type(self):
        return self.type
    
####################################################
class Provider(object):
	sync_number = 0
	backlog = []            #  list of Backlog objects
        name = ""
        sync_state = 0       # is the provider currently syncing, so sotre other messages

        #when registering a new provider, we just need the initial sync number
	def __init__(self, starting_sync, name):
                #print "consturctor1"
	 	self.sync_number = starting_sync
                self.name = name
                #print str(self.sync_number)
                self.sync_state = 0

        def __init__(self, starting_sync, name, sync_mode):
                #print "consturctor2"
	 	self.sync_number = starting_sync
                self.name = name
                #print str(self.sync_number)
                self.sync_state = sync_mode
                #print(self.sync_mode)


        def name(self):
            return self.name


        def next_seq(self):
            return self.sync_number + 1

        def get_seq_num(self):
            return self.sync_number

        def increment_seq(self):
            self.sync_number = self.sync_number + 1
            
        def store_action(self, action, seq, type):
            #need to store the desired action in sorted order
            logging.debug("STORE ACTION|  seq: %i, type: %s"%(seq, type))
            #print "STORE ACTION:  seq, type, action"
            #print(seq),
            #print(type),
            #print(action)
            
            #want to add this in sorted order
            self.backlog.append(Backlog(seq, action, type))
            sorted(self.backlog, key=lambda Backlog: Backlog.sync_number)

        def has_backlog(self):
            #print(self.backlog)
            return len(self.backlog)

        def sync_mode(self):
            return self.sync_state

        def set_sync_mode(self, mode):
            self.sync_state = mode

        def process_backlog(self):

            if len(self.backlog) == 0:
                return None


            logging.info( "Processing Backlog, list size : %i"%(len(self.backlog)))
            #print(len(self.backlog))

            num_to_be_removed = 0


            #go thorugh the queue and process any sequence numbers that are good
            for op in self.backlog:

                #Process legal backlog                   , or handel backlog which happened while syncing
                if(op.seq_num() == self.sync_number + 1):# or (op.seq_num() == self.sync_number) ):
                
                    """
                    Need to incrememnt this counter as python is stupid!
                    we can't remove the "op" element from the list, as the 
                    itterator will skip past the second element to the third
                    
                    Instead we must keep a count and remove the elements manually
                    below
                    """
                    num_to_be_removed = num_to_be_removed + 1

                    #increment the sequence number as we found one, only if not the same
                    #if op.seq_num() != self.sync_number:
                    self.sync_number = self.sync_number + 1

                    #now perform the operation
                    logging.debug( "Backlog actions: for SN : %i" %op.seq_num())
                    
                    logging.debug("Type " + op.get_type())
                    #print(op.get_action())

                    #now get the lock
                    q_cond.acquire()

                    #Create a new object and add to the table
                    op_queue.append(Backlog(op.seq_num(), op.get_action(), op.get_type()))

                    #notify and release
                    q_cond.notify()
                    q_cond.release()

                    
                    #print("FOUND seqnum %i"%(op.seq_num())),
                   
                    
           
                    #print("NEW seq num is %i"%(self.sync_number)),


                    #print(": Index " + str(self.backlog.index(op)))

                else:
                    logging.debug("Found Element is not in order")
                    logging.debug("Current : %i, stored %i"% (self.sync_number, op.seq_num()))
                    break

                sys.stdout.flush()


            #Now remove any processed backlog, always from the head - sorted list
            for i in range(num_to_be_removed):
                self.backlog.pop(0)
                #for o in temp:
                #        print(o.seq_num()),
                #        print(" " ),
                #print(" ")

            logging.info( "Finished processing Backlog")
            

                


class MyListener(object):

    TOTAL_TIME  = 0
    stop 	= 0
    
    def on_connecting(self, host_and_port):
        print 'connecting...'
        #self.c.connect(wait=True)

    def on_disconnected(self):
        print "lost connection"

    def on_message(self, headers, body):
        global N
        self.__print_async("MESSAGE:", headers, body)
        N+=1

    def on_error(self, headers, body):
        self.__print_async("ERROR", headers, body)

    def on_receipt(self, headers, body):
        self.__print_async("RECEIPT", headers, body)

    def on_connected(self, headers, body):
        self.__print_async("CONNECTED", headers, body)
    
    def __print_async(self, frame_type, headers, body):
        logging.debug("\r  \r")
        logging.debug( frame_type)
        
        """
        HEADER KEYS
        headers[0]	:	expiration
        headers[1]	: 	ack
        headers[2]	: 	timestamp
        headers[3]	:	destination
        headers[4]	:	priority
        headers[5]	:	message-id
        """
        #lock.acquire()
        
	#logging.info(time.time())
	
	start = time.time()
	#print("diff %f"%(start-self.stop))
	
	#This is the timing threshold
	if(start-self.stop) > 30:
		self.TOTAL_TIME = 0
		
        #Is this a potential IS message?
        if('destination' in headers):
               # try:
                    header = body.split("\n\n")
                    provider = header[0].split("\n")
                    processed = 0
                    #print "are there any providers"

                    #print(providers)

                    #Are there any current providers?
                    if(len(providers) > 0):
                        for p in providers:
                               
                                temp_name = str(provider[0])
                                temp_num = int(provider[1])

                                if(str(p.name) == temp_name):

                                        logging.debug( "found existing provider : %s"%temp_name)
                                        
                                        #Use this as a flag to skip the new provider bit below
                                        processed = 1
                                         
                                        
                                        #is this next message in the sequence
                                        logging.debug("SEQNUM       : "  +  str(temp_num))
                                        logging.debug("SYNC MODE    :"   + str(p.sync_mode()))

                                        
                                        #print(p.next_seq())
                                        #print(str(p.sync_mode()))
                                        #if Valid sequence number, and provider not in sync mode
                                        if((int(p.next_seq()) ==  temp_num) and (int(p.sync_mode()) == 0)):
                                               

                                                logging.debug("*********NEXT seq num*******************")
                                                logging.debug("****************************************")
                                                logging.debug("****************************************")
                                                
                                                #we have the correct seq num, so prepare for the next one
                                                p.increment_seq()

                                                #now get the lock
                                                q_cond.acquire()

                                                #Create a new object and add to the table
                                                op_queue.append(Backlog(temp_num, header[1], headers['destination']))

                                                #notify and release
                                                q_cond.notify()
                                                q_cond.release()

                                                #this will add any backlog to the process q
                                                p.process_backlog()

                                        #If a sync message for an existing provider
                                        elif( headers['destination'] == MY_SYNC_LIST):
                                            
                                                        #special case, can't do anything else till we are done syncing
                                                        logging.debug( "special case sync")

                                                        #Sync messages are always additions (This should really be another threaded q)
                                                        handle_addition(header[1])

                                                        #if done syncing, set sync_mode to false
                                                        if int(provider[1]) == 1:
                                                            logging.debug( "LAST SYNC MESSAGE")
                                                            p.set_sync_mode(0)
                                                            p.process_backlog()



                                                        #how about remove from providers list
                                                        #this will ensure that no other updates are processed unitl in sync

                                        #If the provider was restarted, we will already have it on record
                                        #But the incoming  sync number will be lower than the current recorded
                                        elif temp_num < p.get_seq_num()  :

                                               #simply remove the entry from the providers, forcing a sync
                                               providers.remove(p)

                                               #Then do a recursive delete of the entry and its subtree (This shoudl really be another threaded q)
                                               #handle_deletion(header[1], 1)

                                               #now get the lock
                                               q_cond.acquire()

                                               #Create a new object and add to the table
                                               op_queue.append(Backlog(int(provider[1]), header[1], "/topic/re-deletion/"))

                                               #notify and release
                                               q_cond.notify()
                                               q_cond.release()

                                               """
                                               This above 'resync' method is heavy handed

                                               A better situation would be to do a comparison
                                               between the contextCSN number between the Provider
                                               and consumer (Master and Slave)

                                               ldapsearch -x -LLL -h MASTER -b o=grid contextCSN

                                               ldapsearch -x -LLL -h SLAVE  -b o=grid contextCSN


                                               This returns the contextCSN values for each. As there is only 1 provider,
                                               this value is good enough to ensure whether or not the items are in sync.

                                               If the elements are in sync, need to do a traversal of the subtree with a similar idea
                                               """


                                        else:

                                                logging.debug("Seq should be %i" %(int(p.next_seq())))

                                                
                                                if (int(p.sync_mode()) == 1):
                                                    logging.debug( "SYNC MODE: Store the action")
                                                else:
                                                    logging.debug("OUT OF ORDER")
                                                """
                                                need a q to store backed-up operations for a given provider with a seqnum that gets out

                                                also, there should be something that syncs after a number/duration timeout - dumps 							current q
                                                """
                                                #the queue will live inside the p obejct . p.backlog()
                                                p.store_action(header[1], temp_num, headers['destination'])

                                        #we have processed the request, leave the loop
                                        break
                       # print "now skip"
                      #  raise Skip


                    """
                    If we have an unrecognised provider either:

                    

                    *There is a sync message from an unrecognised provider,
                        collect the sync messages and finally add the provider

                    (This is used for the consumers inital sync request)
                    ------------------------------------------------------------

                    
                    
                    *There are non sync messages from an unrecognised provider
                        Create a Provider object in sync mode
                        Send the provider a sync request

                    (This is used for when a provider message if found at runtime)
                    """

                    #Provider not synced or seen
                    if(processed == 0):


                        logging.debug( "UNKNOWN MESSAGE : %s"%str(provider[0]))

                        logging.debug( "Sequence Number : %i" %int(provider[1]))

                        

                        #Sync messages from an unknown provider
                        if( headers['destination'] == MY_SYNC_LIST):
                            
                            logging.debug("SYNC")
                            #print(body)

                            #Sync messages are always additions
                            #now get the lock
                            q_cond.acquire()

                            #Create a new object and add to the table
                            #op_queue.append(Backlog(int(provider[1]), header[1], "/topic/addition/"))
                            
                           
                            do_sync(provider[0])

                            #notify and release
                            q_cond.notify()
                            q_cond.release()

                            #Record this providers, so we don't resend the sync
                            if provider[0] not in sync_providers:
                                sync_providers.append(provider[0])

                            #this is the last sync message, add the provider
                            if int(provider[1]) == 1:
                                logging.debug ("END OF REQUESTED SYNC")

                                
                                #create a new provider object with the current sequence number
                                #new = Provider(int(provider[1]), str(provider[0]))
                                #print "created provider"
                                #providers.append(new)

                            #print "Finished unknown sync"


                        #unrecognised provider normal messages
                        if( headers['destination'] != MY_SYNC_LIST):
                            logging.debug( "UNKNOWN PROVIDER MESSAGE : %s"%provider[0])

                            #create a new provider with the correct seq num
                            logging.debug( "create new provider")
                            new = Provider(int(provider[1]), str(provider[0]), 1)
                            providers.append(new)
                            
                            #If completely unseen entry
                            if provider[0] not in sync_providers:

                                logging.debug( "Send SYNC Request")
                                #send out the sync request
                                con.send(REPLY,destination=REQUEST, ack='auto')
                            else:

                                logging.debug( "SYNCED: Process the request")
                                #To get here me must be in Sync so update the mode
                                new.set_sync_mode(0)

                                #Handel the requested action, next time will be
                                #caught by the above loop

                                #now get the lock
                                q_cond.acquire()

                                #Create a new object and add to the table
                                op_queue.append(Backlog(int(provider[1]), header[1], headers['destination']))

                                #notify and release
                                q_cond.notify()
                                q_cond.release()
                                
                                #record whatever action was being requested
                                #new.store_action(header[1], int(provider[1]), headers['destination'])
                            
                        logging.debug( "Providers List: ")
                        logging.debug(providers)



        #for header_key in headers.keys():
         #   print '%s: %s' % (header_key, headers[header_key])
            #print(header_key)
            #print(headers)
            
        #print
        #print body
        logging.debug ('\n\n> ')
        sys.stdout.flush()
        self.stop = time.time()
        dl = body.splitlines()
        
        #The try is to ignore an exception in the case of a last sync message not having dl[3]
        try:
	       	if dl and ('destination' in headers):
	       	   
	       	   if str(dl[3]).endswith("o=grid"):
			logging.info("time, head, body, type | %f : %i : %i : %s"%((self.stop - start), len(headers), len(body), dl[3].split(",")[0]))
			#logging.info(time.time())
			self.TOTAL_TIME = self.TOTAL_TIME + (self.stop-start)
			logging.info("UPDATE TIME : %f"%(self.TOTAL_TIME))
	except:
		pass
        #lock.release()

if __name__ == '__main__':
    """

    if len(sys.argv) != 2:
        print sys.argv[0],'<topic or queue>'
        sys.exit(-1)

    TOPIC=sys.argv[1]se
    """

    ADDITION = '/topic/addition/'
    MODIFICATION = '/topic/modification/'
    DELETION = '/topic/deletion/'
    REQUEST  = '/topic/sync/'
    REPLY    = '/topic/' + socket.gethostname()       #this should be consumer specific


    #Hardcoded for the moment
    level = LEVELS.get(DEBUG_LEVEL, logging.NOTSET)

    logging.basicConfig(filename=LOG_FILENAME,level=level)
    
    con = stomp.Connection([(HOST,PORT)], 'guest', 'password')
    #sync = stomp.Connection([(HOST,PORT)], 'guest', 'password')
    
    con.set_listener('MyConsumer', MyListener())
    #sync.set_listener('MyConsumer', MyListener())

    con.start()
    #sync.start()

    con.connect()
    #sync.connect()

    con.subscribe(destination=ADDITION,     ack='auto', headers=HEADERS)
    con.subscribe(destination=MODIFICATION, ack='auto', headers=HEADERS)
    con.subscribe(destination=DELETION,     ack='auto', headers=HEADERS)
    con.subscribe(destination=REPLY,        ack='auto', headers=HEADERS)
    #sync.subscribe(destination=DELETION, ack='auto', headers=HEADERS)


    #Request the initial sync request
    con.send(REPLY,destination=REQUEST, ack='auto')


    #Finally, start the thread that will process messages to the database
    thread.start_new_thread(q_processor, (None, None))



    while True:
        time.sleep(500)

   # conn.disconnect()

    
