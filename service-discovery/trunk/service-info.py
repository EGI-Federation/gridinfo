import ldap
import sys
import getopt

_version = '0.1'
_debug = '2'
_output = 0

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "b:t:v:l:cjhd:V", ["bdii=", "type=","vo=","list=","csv","json","help","debug=","version"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()                     
			sys.exit()
		elif opt in ("-V", "--version"):
			print 'Service-info v'+_version
		elif opt in ("-d", "--debug"):                
			_debug = arg
			output = 'Debug level '+_debug
			if _debug == '0':
				output+=' (errors)'
                        if _debug == '1':
                                output+=' (warnings)'
                        if _debug == '2':
                                output+=' (info (default))'
                        if _debug == '3':
                                output+=' (debug)'
			print output
		elif opt in ("-c","--csv"):
			_output = 1
			print 'Output in csv formating'
                elif opt in ("-j","--json"):
			_output = 2
			print 'Output in json formating'
                elif opt in ("-l","--list"):
			print 'list=',arg
                elif opt in ("-v","--vo"):
			print 'vo=',arg
                elif opt in ("-t","--type"):
			print 'type=',arg
                elif opt in ("-b","--bdii"):
			print 'bdii=',arg
	#l = ldap.initialize('ldap://lcg-bdii.cern.ch:2170')
	#res = l.result(l.search('o='+dn,ldap.SCOPE_SUBTREE,'(objectClass='+objectclass+')'))

def usage():
	print '''Usage: service-info [options] 

    -b, -bdii     host:port	Specify a BDII endpoint (<hostname>:<port>). By default the environmental variable LCG_GFAL_INFOSYS will be used.
    -t, --type    type		Lists all services of a specific type. By default all services are returned.
    -v, --vo      VO   		List all services for a specific VO
    -l, --list	  attrib 	List all the published values for an attribute (ServiceType, VO)
    -c, --csv			Provides the output in CSV formating
    -j, --json			Provides the output in JSON formating
    -h, --help 	   		Prints this helpful message
    -d, --debug    		Debug level: 0(errors), 1(warnings), 2(info), 3(debug), default 2
    -V, --version		Prints this helpful message'''

if __name__ == "__main__":
    main(sys.argv[1:])
