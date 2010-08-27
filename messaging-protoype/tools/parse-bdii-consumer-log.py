#!/usr/bin/env python

#from pyparsing import *
import os
import sys

"""
Open all the log files and output a comma  seperated list of entries
"""

#print "open the file"
#input = open("test.txt", 'r')
#data = input.read()

#------------------------------------------------------------------------
# Define Grammars
#------------------------------------------------------------------------
"""
chars1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-"
chars2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-.[]"
chars3 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890:"
lower = "-"

integer = Word(nums)
word    = Word(alphas)
hexnums = Word(alphanums)
pre_chars = hexnums + Literal("-")
non_chars = ("-")
space = " "
chars = Word(alphanums)
end = Literal("\n").suppress()
all = SkipTo(end)
colon = Literal(":")

size_preamble = Literal("-rw------- 1 edguser edguser")
size_actual = Word(nums)

data_size = size_preamble + size_actual.setResultsName("size") + all


timing = word + integer.setResultsName("minutes") + Literal("m") + integer.setResultsName("seconds") + Literal(".") + integer.setResultsName("micros")

percentage_figure = Literal("(") + integer + Literal("% ff)\n") 
"""




#logEntry = date.setResultsName("date")  + host.setResultsName("host")  +version.setResultsName("version") + colon + words + eq + conn.setResultsName("connection") + action.setResultsName("action") + eq + action_num.setResultsName("action_number") + db_op.setResultsName("db_op") + all.setResultsName("body")

#logEntry2 = date.setResultsName("date")  + host.setResultsName("host")  +version.setResultsName("version") + colon + words + eq + conn.setResultsName("connection") + action.setResultsName("action") + eq + action_num.setResultsName("action_number") + db_op.setResultsName("db_op")

"""
threadname = dblQuotedString
daemon = Literal("daemon")
objectwait = Literal("in Object.wait()")
waitmon = Literal("waiting for monitor entry")
waitcon = Literal("waiting on condition")
runnable = Literal("runnable")
runstate = objectwait | runnable | waitmon | waitcon
memloc = Word(alphanums + "\[\].")
waitlock = Combine (Group(Literal("- waiting to lock")+ all))
waiton = Combine (Group(Literal("- waiting on")+ all))
locked = Combine (Group(Literal("- locked")+ all))
verbline = Combine (Group("at " + all))
condition = waitlock | waiton | locked
cond = ZeroOrMore(condition + restOfLine).setResultsName("condition")
cond.ignore(verbline)

priority = "prio=" + integer.setResultsName("prio")
tidref = "tid=" + hexnums.setResultsName("tid")
nidref = "nid=" + hexnums.setResultsName("nid")

logEntry = threadname.setResultsName("threadname") + daemon + priority + tidref + nidref \
    + runstate.setResultsName("runstate") + memloc.setResultsName("memloc") \
    + cond
"""
#------------------------------------------------------------------------

mapping = {'gluelocationlocalid' 		: 'Location         ',
           'gluevoviewlocalid' 			: 'VOView           ',
           'glueservicedatakey' 		: 'ServiceData      ',
           'gluecesebindseuniqueid' 		: 'CESEBind         ',
           'gluesalocalid' 			: 'SA               ',
           'glueseuniqueid' 			: 'SE               ',
           'gluesiteuniqueid' 			: 'Site             ',
           'glueceuniqueid' 			: 'CE               ',
           'gluevoinfolocalid' 			: 'VOInfo           ', 
           'gluecesebindgroupceuniqueid' 	: 'CESEBindGroup    ', 
           'glueserviceuniqueid' 		: 'Service          ',
           'glueseaccessprotocollocalid' 	: 'SEAccessProtocol ',
           'gluesecontrolprotocollocalid' 	: 'SEControlProtocol',
           'gluesubclusteruniqueid' 		: 'SubCluster       ',
           'glueclusteruniqueid' 		: 'Cluster          ',
}

f=open("./bdii-consumer.log", 'r')
data=f.read()
f.close()
previous_time		= 0.0

proc_times   		= [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
object_sizes 		= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
num_objs     		= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
total_proc_times	= []

#sys.stdout.write(file),
#print out the relevant data with commas
for line in data.split("\n"):
	if line.startswith("INFO:root:time"):
		temp = line[35:]
		#print(temp)
		temp = temp.replace("dn: ", "") 
		#print(temp.split(": "))
		processing_time, header_size, body_size, object_type = temp.split(": ")
		#print(float(processing_time)	)
		#print(int(header_size) + int(body_size)	)
		#print(body_size)
		#print(object_type.split("=")[0])
		
		#print(mapping[object_type.split("=")[0]])
		
		n = 0
		for i, j in mapping.iteritems():
			if(i == object_type.split("=")[0]):
				proc_times[n] 	+= float(processing_time)
				object_sizes[n] += int(header_size) + int(body_size)
				num_objs[n]	+= 1
				
			n += 1

	
	
	if line.startswith("INFO:root:UPDATE TIME "):
		temp = line[24:]
		number = float(temp)
		
			
		if number < previous_time:
			total_proc_times.append(previous_time)

		previous_time = number
		
		#print(temp)
		
for i in range(len(num_objs)):
	if num_objs[i] == 0:
		num_objs[i] = 1
n = 0	
print("Object Type 		    Message Proc Time		            Object Size		  	Number of Messages")
print("----------- 		-------------------------		-------------------		-------------------")

print("******************AVERAGE VALUES*********************************")

for i, j in mapping.iteritems():
	print("%s		%f			%f			%i"%(j, proc_times[n]/num_objs[n],object_sizes[n]/num_objs[n],num_objs[n]))
	n += 1
	
print("******************TOTAL VALUES*********************************")
tot_data = 0
n = 0
for i, j in mapping.iteritems():
	print("%s		%f			%i"%(j, proc_times[n]/60, object_sizes[n]))
	tot_data += object_sizes[n]
	n +=1
print("----------------")
print("Total Data Transmitted: %fMB"%((tot_data/1024)/1024 ))
print("******************TIME VALUES*********************************")
tot = 0.0
for i in range(len(total_proc_times)):
	tot += total_proc_times[i]
	print("Update %i took %f seconds"%(i,total_proc_times[i]))
print("----------------")
print("Average : %f"%(tot / len(total_proc_times)))
print("Total   : %f Hours"%(tot/3600))
