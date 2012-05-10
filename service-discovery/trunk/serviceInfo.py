import ldap
import sys
import getopt
import os

VERSION = 'Service-info V0.1'

def main(argv):
	bdii = ''
	type = ''
	output = 0
	debug = '2'
	try:
		opts, args = getopt.getopt(argv, "b:t:v:l:cjhd:V", ["bdii=", "type=","vo=","list=","csv","json","help","debug=","version"])
	except getopt.GetoptError:
		usage()
		sys.exit()
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()                     
			sys.exit()
	for opt, arg in opts:
		if opt in ("-V", "--version"):
			print VERSION
		elif opt in ("-d", "--debug"):                
			debug = arg
			debug_lvl = 'Debug level '+debug
			if debug == '0':
				debug_lvl+=' (errors)'
                        elif debug == '1':
                                debug_lvl+=' (warnings)'
                        elif debug == '2':
                                debug_lvl+=' (info (default))'
                        elif debug == '3':
                                debug_lvl+=' (debug)'
			else:
				print 'Wrong debug level'
				usage()
                        	sys.exit()
			print debug_lvl
		elif opt in ("-c","--csv"):
			if output == 2:
				print 'Error: choose between csv and json.'
				sys.exit()
			output = 1
			print 'Output in csv formating'
                elif opt in ("-j","--json"):
			if output == 1:
                                print 'Error: choose between csv and json formatting.'
                                sys.exit()
			output = 2
			print 'Output in json formating'
                elif opt in ("-b","--bdii"):
                        bdii = arg
                        print 'The following bdii will be used:',arg
	if not bdii:
                if 'LCG_GFAL_INFOSYS' in os.environ:
                        bdii = os.environ['LCG_GFAL_INFOSYS']
                else:
                        print 'Please specify a bddi endpoint (-b option).'
                        sys.exit()
	for opt, arg in opts:
                if opt in ("-l","--list"):
			attr = arg
			print 'The values for the following attribute will be displayed:',arg
			print
			list_attr(bdii,attr)
			sys.exit()
                elif opt in ("-v","--vo"):
			print 'Lists all services for the following VO:',arg
                elif opt in ("-t","--type"):
			type = arg
			print 'Lists all services for the following type:',arg
	print
	discover(bdii,type,output,debug)
	sys.exit()

def usage():
	print '''Usage: service-info [options]

    -b, --bdii	host:port	Specify a BDII endpoint (<hostname>:<port>). By default the environmental variable LCG_GFAL_INFOSYS will be used.
    -t, --type	type		Lists all services of a specific type. By default all services are returned.
    -v, --vo	VO		List all services for a specific VO
    -l, --list	attrib		List all the published values for an attribute (ServiceType, VO)
    -c, --csv			Provides the output in CSV formating
    -j, --json			Provides the output in JSON formating
    -h, --help			Prints this helpful message
    -d, --debug			Debug level: 0(errors), 1(warnings), 2(info), 3(debug), default 2
    -V, --version		Prints this helpful message'''

def discover(bdii,type='',output=0,debug='2'):
	l = ldap.initialize('ldap://'+bdii)
	res = l.result(l.search('o=glue',ldap.SCOPE_SUBTREE,'(objectClass=GLUE2Service)'))
	list=[]
	for r in res[1]:
		if type:
			if r[1]['GLUE2ServiceType'][0] != type:
				continue
		list.append(r[0][r[0].find('=')+1:r[0].find(',')])
	list.sort()
	if output == 0:
		print '\n'.join(list)
	elif output == 1:
		print ','.join(list)
	elif output == 2:
		list = '\':[],\''.join(list)
		print '{\''+list+'\':[]}'

def list_attr(bdii,attr=''):
	if attr == 'ServiceType':
		l = ldap.initialize('ldap://'+bdii)
        	res = l.result(l.search('o=glue',ldap.SCOPE_SUBTREE,'(objectClass=GLUE2Service)'))
        	list=[]
		for r in res[1]:
			if r[1]['GLUE2'+attr][0] not in list:
				list.append(r[1]['GLUE2ServiceType'][0])
		list.sort()
        	for i in list:
        	        print i
	else:
		print 'Error: wrong attribute.'

if __name__ == "__main__":
    main(sys.argv[1:])
