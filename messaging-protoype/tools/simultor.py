#! /usr/bin/python

import getopt                       #command line parsing
import sys
import stop                         #Stomp Library
import time                         #For the time measurements


"""
Predefined parameter values, these are the knobs for the simulation
"""
TOTAL_OBJECTS                       =   0           #Total number of objects in the system
NUM_OBJECT_TYPES                    =   15          #Number of different types of objects

ADDS_PER_DAY                        =   0           #Number of objecsts added per day
DELS_PER_DAY                        =   0           #Number of objects deleted per day
MODS_PER_DAY                        =   0           #Number of modifications per day


"""
These indices refer to the object arrays below
"""
OBJECT_TOTALS                       =   0           #Index of the number of total objects
OBJECT_ADDS                         =   1           #Index of the number of additions
OBJECT_DELETS                       =   2           #Index of the number of deletions
OBJECT_MODIFICATIONS                =   3           #Index of the number of modifications


#Total number of object types in the following order
"TOTAL_CE_OBJECTS"
"TOTAL_CESEBIND_OBJECTS"
"TOTAL_CESEBINDGROUP_OBJECTS"
"TOTAL_CLUSTER_OBJECTS"
"TOTAL_LOCATION_OBJECTS"
"TOTAL_SA_OBJECTS"
"TOTAL_SE_OBJECTS"
"TOTAL_SEACCESSPROTOCOL_OBJECTS"
"TOTAL_SECONTROLPROTOCOL_OBJECTS"
"TOTAL_SERVICE_OBJECTS"
"TOTAL_SERVICEDATA_OBJECTS"
"TOTAL_SITE_OBJECTS"
"TOTAL_SUBCLUSTER_OBJECTS"
"TOTAL_VOINFO_OBJECTS"
"TOTAL_VOVIEW_OBJECTS"
#OBJECT_TYPE_TOTALS                  =  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


#Those marked with a # are the modification per 6 minutes
#Array of the different objects: TOTAL | ADDED | DELETED | MODIFIED
ce_object                   = [4271,        11,     7,      2470]   #
cesebind_object             = [8254,        22,     13,     8]
cesebindgroup_object        = [4318,        14,     7,      2]
cluster_object              = [599,         1,      1,      1]
location_object             = [45699,       320,    174,    302]
sa_object                   = [5470,        25,     26,     829]    #
se_object                   = [456,         1,      1,      65]     #
seaccessprotocol_object     = [2347,        13,     11,     6]
secontrolprotocol_object    = [703,         2,      2,      1]
service_object              = [3851,        16,     12,     568]    #
servicedata_object          = [9313,        49,     27,     2]
site_object                 = [351,         1,      1,      1]
subcluster_object           = [657,         2,      1,      130]
voinfo_object               = [5011,        39,     36,     2]
voview_object               = [9603,        24,     16,     4319]   #


STATS_ARRAY = [ce_object,
               cesebind_object,
               cesebindgroup_object,
               location_object,
               sa_object,
               se_object,
               seaccessprotocol_object,
               secontrolprotocol_object,
               service_object,
               servicedata_object,
               site_object,
               subcluster_object,
               voinfo_object,
               voview_object]


STATE_OF_THINGS_FILE    = "sot.txt" #File location of the state of things

"""
Array of integers to serve as the seeds for LDAP objects, the size of which is
equal to the total number of objects in the System
"""
seed_objects = None

#List to store the objects that have been added
added_objects = []

#list to store the objects that have been deleted
deleted_objects = []

#List to store the objects that have been modified
modified_objects = []


"""
Functions to generated an object based on a supplied seed value
"""

def create_ce(seed, prefix):
    temp = None
    temp += "dn: GlueCEUniqueID=%i, %s"%(seed, prefix)
    temp += "GlueCEUniqueID: %i"%(seed)
    temp += "objectclass: GlueCETop"
    temp += "objectClass: GlueCE"
    return temp

def create_cesebind(seed):
    temp = None
    temp += "dn: GlueCESEBindSEUniqueID==%i, %s"%(seed, prefix)
    temp += "GlueCEUniqueID: %i"%(seed)
    temp += "objectclass: GlueCETop"
    temp += "objectClass: GlueCE"
    return temp

def create_cesebindgroup(seed):
    pass

def create_cluster(seed):
    pass

def create_location(seed):
    pass

def create_sa(seed):
    pass

def create_se(seed):
    pass

def create_seaccessprotocol(seed):
    pass

def create_secontrolprotocol(seed):
    pass

def create_service(seed):
    pass

def create_servicedata(seed):
    pass

def create_site(seed):
    pass

def create_subcluster(seed):
    pass

def create_voinfo(seed):
    pass

def create_voview(seed):
    pass
################################################################################
"""
Utility fundtions
"""

#Parse the file conataining the state of things
def parse_state_of_things(file_handel):
    pass
#-------------------------------------------------------------------------------
def print_usage():
    print "USAGE: gen.py [-m [1|2] , -c <CONFIGURATION FILE>]"
    print "1    :   Initial Database Generation"
    print "2    :   LDAP simulator"
    sys.exit(2)
#-------------------------------------------------------------------------------
def parse_options():
    try:
        opts, rem = getopt.getopt(sys.argv[1:], 'c:m:')

        for opt, arg in opts:
            if opt == "-m":
                if arg == "1" or arg == "2":
                    return int(arg)
                else:
                     print_usage()

            if opt == "-c":
                print "Configuration file was supplied :",
                print(arg)
                sys.exit(2)
                
    except getopt.GetoptError:
        sys.stderr.write("Error: Invalid option specified.\n")
        print_usage()
        sys.exit(2)
    
#-------------------------------------------------------------------------------
#Create an integer array of the total number of seed values
def setup_seed_values():

    total = 0

    #Get the total number of objects
    for i in range(len(STATS_ARRAY)):
        total += STATS_ARRAY[i][OBJECT_TOTALS]

    #initalise the seed values
    for i in range(total):
        seed_objects[i] = i
#-------------------------------------------------------------------------------
#returns the next avaliable seed value which is unsued
def next_free_seed():
    
    try:
        temp = seed_objects.pop()
        return temp
    except:
        print "ERROR: We are out of seeds"
        return None


################################################################################

#Will generate as many objects per type as specified by the above "knobs"
def generate_initial_database():



    function    = None             #Function pointer

    LDIF        = None             #Will hold the new LDIF objects


    #as this is the first run, need to setup the array
    setup_seed_values()

    #for each object type
    for i in range(NUM_OBJECT_TYPES):

        #assign the appropriate constructor to the function pointer
        if i == 0:
            function = create_ce
        elif i == 1:
            function = create_cesebind
        elif i == 2:
            function = create_cesebindgroup
        elif i == 3:
            function = create_cluster
        elif i == 4:
            function = create_location
        elif i == 5:
            function = create_sa
        elif i == 6:
            function = create_se
        elif i == 7:
            function = create_seaccessprotocol
        elif i == 8:
            function = create_secontrolprotocol
        elif i == 9:
            function = create_service
        elif i == 10:
            function = create_servicedata
        elif i == 11:
            function = create_site
        elif i == 12:
            function = create_subcluster
        elif i == 13:
            function = create_voinfo
        else:
            function = create_voview

        #for the number of specified objects of each type
        for j in range(STATS_ARRAY[i][OBJECT_TOTALS]):

            #get the next seed
            seed = next_free_seed()

            #create such an object with the correct seed
            LDIF += function(seed)


            """
            Need to figure out the nesting structure of the objects.
            Some objects are sub objects of others
            """


    return LDIF

################################################################################
"""
So, this simulator will work on the principal that the "update" script will invoke
this python at some intervals. In return, this file will return a random collection
of ldap objects for addition, deletion and modification. This will require some
pre-knowledge, accordingly a file will have to exist conatining the current state
of things.

This main will work like the following:

* Read the file to determine the current state of things

* Based on the current state of things, generate objects for the current time

* Update the file with the new current state of things
"""

def main():


    #read the file, this location could be secified as a command line param
    fh = open(STATE_OF_THINGS_FILE, 'r')

    some_datastructure = parse_state_of_things(fh)

    fh.close()

    #if a day has passed
    if need_to_regenerate(some_datastructure):

        #recalculate the statistics for the coming day
        generate_statistics(some_datastructure)
    
    
    #grab the appropriate statsitcs for just now, and created the appropriate objects
    generate_objects(some_datastructure)

    #write the file
    fh = open(STATE_OF_THINGS_FILE, 'w')

    write_state_of_things(fh)


def stat_generator():

    while True:


        


        #Per 6 minutes
        time.sleep(360)

"""
There are two possibilities  for the main:

* Generating the database initially

* The simulator

"""
if __name__ == "__main__":


    config = parse_options()

    if config == 1:
        generate_initial_database()
    elif config == 2:
        main()
    else:
        print_usage()


    conn = stomp.Connection([(HOST,PORT)], 'guest', 'password')
    conn.set_listener('MyListener', MyListener())
    conn.start()
    conn.connect()




