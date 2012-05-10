import unittest
import commands

class TestServiceInfo(unittest.TestCase):

	def test_help(self):
		result = commands.getstatusoutput("service-info -h")
		expected_message ='''Usage: service-info [options]

    -b, --bdii	host:port	Specify a BDII endpoint (<hostname>:<port>). By default the environmental variable LCG_GFAL_INFOSYS will be used.
    -t, --type	type		Lists all services of a specific type. By default all services are returned.
    -v, --vo	VO		List all services for a specific VO
    -l, --list	attrib		List all the published values for an attribute (ServiceType, VO)
    -c, --csv			Provides the output in CSV formating
    -j, --json			Provides the output in JSON formating
    -h, --help			Prints this helpful message
    -d, --debug			Debug level: 0(errors), 1(warnings), 2(info), 3(debug), default 2
    -V, --version		Prints this helpful message'''
		self.assertEqual(result[1],expected_message)

	def test_bdii_1(self):
		result = commands.getstatusoutput("unset LCG_GFAL_INFOSYS;service-info -b lcg-bdii.cern.ch:2170")
		expected_message ="The following bdii will be used: lcg-bdii.cern.ch:2170"
		self.assertRegexpMatches(result[1],expected_message)

	def test_bdii_2(self):
                result = commands.getstatusoutput("export LCG_GFAL_INFOSYS='lcg-bdii.cern.ch:2170';service-info")
                unexpected_message ="Please specify a bddi endpoint (-b option)."
                self.assertNotRegexpMatches(result[1],unexpected_message)

	def test_no_bdii(self):
		result = commands.getstatusoutput("unset LCG_GFAL_INFOSYS;service-info")
		expected_message = "Please specify a bddi endpoint (-b option)."
                self.assertEqual(result[1],expected_message)

if __name__ == "__main__":
	unittest.main()
