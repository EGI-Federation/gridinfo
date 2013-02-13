import re
import unittest
import datetime

class EGIProfileTest(unittest.TestCase):

    def __init__(self, test_name, entry, value, test_class):

        unittest.TestCase.__init__(self, test_name)
        self.entry = entry
        if 'dn' in entry:
            self.dn = entry['dn'][0]
        else:
            self.dn = None

        self.types = __import__('%s.types' %(test_class,)).types

        self.value = value


    def test_GLUE2EntityCreationTime_OK (self):
        creationtime = datetime.datetime.strptime( self.value[0], "%Y-%m-%dT%H:%M:%SZ" )
        now = datetime.datetime.utcnow()
        year = datetime.timedelta(days=365)
        if creationtime > now:
            message = "ERROR: %s has a creation time in the future!" % (self.dn)
            status = False
        elif creationtime < (now - year):
            message = "WARNING: %s has a creation time of more than one year ago" % (self.dn) 
            status = False
        else: 
            message = ""
            status = True
        self.assertTrue(status, message)


    def test_GLUE2EntityValidity_OK (self):
        if 'GLUE2EntityCreationTime' not in self.entry:
            status = False
            message = "ERROR: %s should not publish GLUE2EntityValidity since GLUE2EntityCreationTime is not published" %\
                       (self.dn)
        else:
            creationtime = datetime.datetime.strptime( self.entry['GLUE2EntityCreationTime'][0], "%Y-%m-%dT%H:%M:%SZ" ) 
            now = datetime.datetime.utcnow()
            validity = datetime.timedelta(seconds=int(self.value[0]))
            if ( creationtime + validity ) < now:
                message = "ERROR: %s validity has expired !" % (self.dn)
                status = False
            else:
                message = ""
                status = True
        self.assertTrue(status, message)


    def test_GLUE2EntityOtherInfo_OK (self):
        message = ""
        status = True
        for pair in self.value:
            index = pair.find("=")
            if (index > -1):
                att = pair[:index]
                val = pair[index + 1:]
                if att == 'ProfileName':
                    if val != 'EGI':
                        message = "WARNING: %s contains an unknown value for the Profile Name" % (self.dn)
                        Status = False
                        break
                elif att == 'BLOG':
                    if not self.types.is_URL(val):
                        message = "INFO: %s should specify a correct URL for BLOG" % (self.dn)
                        Status = False
                        break
                elif att == 'WLCG_TIER':
                    if not self.types.is_Tier_t(val):
                        message = "INFO: %s defines a wrong value for WLCG Tier" % (self.dn)
                        Status = False
                        break
                elif att == 'GRID':
                    if not self.types.is_Grid_t(val):
                        message = "INFO: %s defines a wrong Grid Infrastructure" % (self.dn)
                        Status = False
                        break
                elif att == 'CONFIG':
                    if not self.types.is_Config_t(val):
                        message = "INFO: %s defines an unknown configuration tool" % (self.dn)
                        Status = False
                        break

        self.assertTrue(status, message)

    
    def test_GLUE2LocationLongitude_OK (self):
        message = "ERROR: %s has Longitude attribute %s out of range!" % (self.dn, self.value[0]) 
        self.assertTrue( float(self.value[0]) > -180 and float(self.value[0]) < 180, message)     


    def test_GLUE2LocationLatitude_OK (self):
        message = "ERROR: %s has Latitude attribute %s out of range!" % (self.dn, self.value[0])
        self.assertTrue( float(self.value[0]) > -90 and float(self.value[0]) < 90, message)


    def test_GLUE2ServiceQualityLevel_OK (self):
        message = "INFO: %s should publish a 'production' quality level instead of %s" % (self.dn, self.value[0])
        self.assertTrue( self.value[0] == 'production', message )


    def test_GLUE2ComputingServiceTotalJobs_OK (self):
        total = 0
        for job in ['GLUE2ComputingServiceRunningJobs',
                    'GLUE2ComputingServiceWaitingJobs',
                    'GLUE2ComputingServiceStagingJobs',
                    'GLUE2ComputingServiceSuspendedJobs',
                    'GLUE2ComputingServicePreLRMSWaitingJobs']:
            if job in self.entry:
                total = total + int(self.entry[job][0])
        message = "WARNING: %s is publishing a wrong number of total jobs that does not sum up RunningJobs, \
                   WaitingJobs, StagingJobs, SuspendedJobs and PreLRMSWaitingJobs" % (self.dn)           
        self.assertTrue( total == int(self.value[0]), message ) 

    def test_GLUE2ComputingServiceRunningJobs_OK (self):
        message = "INFO: %s publishes %s Running Jobs, higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingServiceWaitingJobs_OK (self):
        message = "INFO: %s publishes %s WaitingJobs, higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )


    def test_GLUE2ComputingServiceStagingJobs_OK (self):
        message = "INFO: %s publishes %s StagingJob, higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )


    def test_GLUE2ComputingServiceSuspendedJobs_OK (self):
        message = "INFO: %s publishes %s SuspendedJobs, higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )


    def test_GLUE2ComputingServicePreLRMSWaitingJobs_OK (self):
        message = "INFO: %s publishes %s PreLRMSWaitingJobs, higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )




