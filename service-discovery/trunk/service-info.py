import ldap
import sys

def main():
	for arg in sys.argv:
		print arg
	#l = ldap.initialize('ldap://lcg-bdii.cern.ch:2170')
	#res = l.result(l.search('o='+dn,ldap.SCOPE_SUBTREE,'(objectClass='+objectclass+')'))

if __name__ == '__main__':
	main()
