import re
import unittest
import datetime
import time

#---------------------------------------------------------------------------------------------
def local_to_utc(t):
    secs = time.mktime(t)
    return time.gmtime(secs)
#----------------------------------------------------------------------------------------------

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

#------------------------------------- GLUE2Entity --------------------------------------------

    def test_GLUE2EntityCreationTime_OK (self):
        try:
            creationtime = datetime.datetime(*(time.strptime(self.value[0],"%Y-%m-%dT%H:%M:%SZ")[0:6]))
            now = datetime.datetime.utcnow()
            year = datetime.timedelta(days=365)
            if local_to_utc(creationtime.timetuple()) > now.timetuple():
                message = ("ERROR:\n"
                           "E001 Description: Creation time in the future !\n" 
                           "E001 Affected DN: %s\n"
                           "E001 Affected attribute: GLUE2EntityCreationTime\n"
                           "E001 Published value: %s") % (self.dn, self.value[0])
                status = False
            elif local_to_utc(creationtime.timetuple()) < (now - year).timetuple:
                message = ("WARNING:\n"
                           "W001 Description: Creation time more than one year old\n"
                           "W001 Affected DN: %s\n"
                           "W001 Affected attribute: GLUE2EntityCreationTime\n"
                           "W001 Published value: %s") % (self.dn, self.value[0])
                status = False
            else: 
                message = ""
                status = True
        except ValueError:
            message = ""
            status = True
        self.assertTrue(status, message)

    def test_GLUE2EntityValidity_OK (self):
        if 'GLUE2EntityCreationTime' not in self.entry:
            status = False
            message = ("WARNING:\n"
                       "W002 Description: GLUE2EntityValidity published when GLUE2EntityCreationTime is not published\n"
                       "W002 Affected DN: %s\n"
                       "W002 Affected attribute: GLUE2EntityValidity\n"
                       "W002 Published value: NA") % (self.dn)
        else:
            try:
                creationtime =  datetime.datetime(*(time.strptime(self.entry['GLUE2EntityCreationTime'][0],"%Y-%m-%dT%H:%M:%SZ")[0:6])) 
                now = datetime.datetime.utcnow()
                validity = datetime.timedelta(seconds=int(self.value[0]))
                due_time = local_to_utc((creationtime + validity).timetuple()) 
                creationtime_utc = local_to_utc(creationtime.timetuple())
                if due_time < now.timetuple():
                    message = ("ERROR:\n"
                               "E002 Description: Obsolete entry\n"
                               "E002 Affected DN: %s\n"
                               "E002 Affected attribute: GLUE2EntityCreationTime and GLUE2EntityValidity\n"
                               "E002 Published value: %s and %s\n") % \
                               (self.dn, self.entry['GLUE2EntityCreationTime'][0], self.value[0])
                    status = False
                else:
                    message = ""
                    status = True
            except ValueError:
                message = ""
                status = True
        self.assertTrue(status, message)

    def test_GLUE2EntityOtherInfo_OK (self):
        message = "%s contains the following issues in the GLUE2EntityOtherInfo attribute" % (self.dn)
        sharedict={}
        status = True
        for pair in self.value:
            index = pair.find("=")
            if (index > -1):
                att = pair[:index]
                val = pair[index + 1:]
                if att == 'ProfileName':
                    if val != 'EGI':
                        message = message + ("\n WARNING:\n"
                                             "W003 Description: Unknown profile name\n"
                                             "W003 Affected DN: %s\n"
                                             "W003 Affected attribute: GLUE2EntityOtherInfo: ProfileName\n"
                                             "W003 Published value: %s\n") % (self.dn, val)
                        status = False
                if att == 'ProfileVersion':
                    if not self.types.is_String(val):
                        message = message + ("\n WARNING:\n"
                                             "W004 Description: Incorrect profile version\n"
                                             "W004 Affected DN: %s\n"
                                             "W004 Affected attribute: GLUE2EntityOtherInfo: ProfileVersion\n"
                                             "W004 Published value: %s\n") % (self.dn, val)
                        status = False
                elif att == 'GRID':
                    if not self.types.is_Grid_t(val):
                        message = message + ("\n INFO:\n"
                                             "I001 Description: Unknown Grid Infrastructure name\n"
                                             "I001 Affected DN: %s\n"
                                             "I001 Affected attribute: GLUE2EntityOtherInfo: GRID\n"
                                             "I001 Published value: %s\n") % (self.dn, val)
                        status = False
                elif att == 'CONFIG':
                    if not self.types.is_Config_t(val):
                        message = message + ("\n INFO:\n"
                                             "I002 Description: Unknown configuration tool\n"
                                             "I002 Affected DN: %s\n"
                                             "I002 Affected attribute: GLUE2EntityOtherInfo: CONFIG\n"
                                             "I002 Published value: %s\n") % (self.dn, val)
                        status = False
                elif att == 'EGI_NGI':
                    if not self.types.is_EGIngi_t(val):
                        message = message + ("\n INFO:\n"
                                             "I003 Description: Unknown EGI NGI\n"
                                             "I003 Affected DN: %s\n"
                                             "I003 Affected attribute: GLUE2EntityOtherInfo: EGI_NGI\n"
                                             "I003 Published value: %s\n") % (self.dn, val)
                        status = False
                elif att == 'BLOG':
                    if not self.types.is_URL(val):
                        message = message + ("\n INFO:\n"
                                             "I004 Description: Incorrect blog URL\n"
                                             "I004 Affected DN: %s\n"
                                             "I004 Affected attribute: GLUE2EntityOtherInfo: BLOG\n"
                                             "I004 Published value: %s\n") % (self.dn, val)
                        status = False
                elif att == 'ICON':
                    if not self.types.is_URL(val):
                        message = message + ("\n INFO:\n"
                                             "I005 Description: Incorrect icon URL\n"
                                             "I005 Affected DN: %s\n"
                                             "I005 Affected attribute: GLUE2EntityOtherInfo: ICON\n"
                                             "I005 Published value: %s\n") % (self.dn, val)
                        status = False
                elif att == 'WLCG_TIER':
                    if not self.types.is_Tier_t(val):
                        message = message + ("\n INFO:\n"
                                             "I006 Description: Unknown WLCG Tier\n"
                                             "I006 Affected DN: %s\n"
                                             "I006 Affected attribute: GLUE2EntityOtherInfo: WLCG_TIER\n"
                                             "I006 Published value: %s\n") % (self.dn, val)
                        status = False
                elif att == 'WLCG_NAME' or att == 'WLCG_PARENT':
                    if not self.types.is_WLCGname_t(val):
                        message = message + ("\n INFO:\n"
                                             "I007 Description: Unknown WLCG name\n"
                                             "I007 Affected DN: %s\n"
                                             "I007 Affected attribute: GLUE2EntityOtherInfo: WLCG_NAME\n"
                                             "I007 Published value: %s\n") % (self.dn, val)
                        status = False
                elif att == 'WLCG_NAMEICON':
                    if not self.types.is_URL(val):
                        message = message + ("\n INFO:\n"
                                             "I008 Description: Incorrect WLCG name icon URL\n"
                                             "I008 Affected DN: %s\n"
                                             "I008 Affected attribute: GLUE2EntityOtherInfo: WLCG_NAMEICON\n"
                                             "I008 Published value: %s\n") % (self.dn, val)
                        status = False
                elif att == 'MiddlewareName':
                    if not self.types.is_Middleware_t(val):
                        message = message + ("\n INFO:\n"
                                             "I009 Description: Unknown middleware name\n"
                                             "I009 Affected DN: %s\n"
                                             "I009 Affected attribute: GLUE2EntityOtherInfo: MiddlewareName\n"
                                             "I009 Published value: %s\n") % (self.dn, val)
                        status = False
                elif att == 'MiddlewareVersion':
                    if not self.types.is_String(val):
                        message = message + ("\n INFO:\n"
                                             "I010 Description: Incorrect middleware version\n"
                                             "I010 Affected DN: %s\n"
                                             "I010 Affected attribute: GLUE2EntityOtherInfo: MiddlewareVersion\n"
                                             "I010 Published value: %s\n") % (self.dn, val)
                        status = False
                elif att == 'HostDN':
                    if not self.types.is_DN_t(val):
                        message = message + ("\n INFO:\n"
                                             "I011 Description: Incorrect DN syntax\n"
                                             "I011 Affected DN: %s\n"
                                             "I011 Affected attribute: GLUE2EntityOtherInfo: HostDN\n"
                                             "I011 Published value: %s\n") % (self.dn, val)
                        status = False
                elif att == 'Share':
                    index2 = val.find(":")
                    if (index2 > -1):
                        voname = val[:index2]
                        percentage = val[index2 +1:]
                        if not self.types.is_VO_t(voname):
                            message = message + ("\n INFO:\n"
                                                 "I012 Description: Unknown VO name in share\n"
                                                 "I012 Affected DN: %s\n"
                                                 "I012 Affected attribute: GLUE2EntityOtherInfo: Share\n"
                                                 "I012 Published value: %s\n") % (self.dn, voname)
                            status = False
                        elif voname not in sharedict:
                            if (int(percentage) < 0) or (int(percentage) > 100):
                                message = message + ("\n ERROR:\n"
                                                     "E003 Description: Wrong share percentage\n"
                                                     "E003 Affected DN: %s\n"
                                                     "E003 Affected attribute: GLUE2EntityOtherInfo: Share\n"
                                                     "E003 Published value: %s:%s\n") % (self.dn, voname, percentage) 
                                status = False
                            sharedict[voname] = int(percentage)
                        else:  
                            message = message + ("\n ERROR:\n"
                                                 "E004 Description: VO appears more than one in share\n"
                                                 "E004 Affected DN: %s\n"
                                                 "E004 Affected attribute: GLUE2EntityOtherInfo: Share\n"
                                                 "E004 Published value: %s\n") % (self.dn, voname)
                            status = False
                    else:
                        message = message + ("\n ERROR:\n"
                                             "E005 Description: Wrong share format\n"
                                             "E005 Affected DN: %s\n"
                                             "E005 Affected attribute: GLUE2EntityOtherInfo: Share\n"
                                             "E005 Published value: %s\n") % (self.dn, val)
                        status = False
                elif att.startswith('CPUScalingReference'):
                    if not self.types.is_Benchmarkabbr_t(att.split('CPUScalingReference')[1]):
                        message = message + ("\n INFO:\n"
                                             "I013 Description: Unknown benchmark name\n"
                                             "I013 Affected DN: %s\n"
                                             "I013 Affected attribute: GLUE2EntityOtherInfo: CPUScalingReference\n"
                                             "I013 Published value: %s\n") % (self.dn,att.split('CPUScalingReference')[1])
                        status = False
            else:
                message = message + ("\n ERROR:\n"
                                     "E006 Description: Wrong attribute format\n"
                                     "E006 Affected DN: %s\n"
                                     "E006 Affected attribute: GLUE2EntityOtherInfo\n"
                                     "E006 Published value: %s\n") % (self.dn, pair)
                status = False
        totalshare=0 
        for i in sharedict:
            totalshare = totalshare + sharedict[i]
        if ( totalshare > 100 ):
            message = message + ("\n ERROR:\n"
                                 "E007 Description: Total published shares > 100% !\n"
                                 "E007 Affected DN: %s\n"
                                 "E007 Affected attribute: GLUE2EntityOtherInfo\n"
                                 "E007 Published value: %s\n") % (self.dn, totalshare)
            status = False 
        self.assertTrue(status, message)
    
#------------------------------------- GLUE2Location --------------------------------------------

    def test_GLUE2LocationLongitude_OK (self):
        message = ("ERROR:\n"
                   "E008 Description: Longitude out of range !\n"
                   "E008 Affected DN: %s\n"
                   "E008 Affected attribute: GLUE2LocationLongitude\n"
                   "E008 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( float(self.value[0]) > -180 and float(self.value[0]) < 180, message)     

    def test_GLUE2LocationLatitude_OK (self):
        message = ("ERROR:\n"
                   "E009 Description: Latitude out of range !\n"
                   "E009 Affected DN: %s\n"
                   "E009 Affected attribute: GLUE2LocationLatitude\n"
                   "E009 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( float(self.value[0]) > -90 and float(self.value[0]) < 90, message)

#------------------------------------- GLUE2ComputingService ---------------------------------------

    def test_GLUE2ComputingServiceTotalJobs_OK (self):
        total = 0
        job_stats = "" 
        for job in ['GLUE2ComputingServiceRunningJobs',
                    'GLUE2ComputingServiceWaitingJobs',
                    'GLUE2ComputingServiceStagingJobs',
                    'GLUE2ComputingServiceSuspendedJobs',
                    'GLUE2ComputingServicePreLRMSWaitingJobs']:
            if job in self.entry:
                total = total + int(self.entry[job][0])
                job_stats = job_stats + " %s=%s" % (job,self.entry[job][0])
        message = ("WARNING:\n"
                   "W005 Description: Incoherent number of total jobs\n"
                   "W005 Affected DN: %s\n"
                   "W005 Affected attribute: GLUE2ComputingServiceTotalJobs\n"
                   "W005 Published value: %s vs %s\n") % (self.dn, self.value[0], job_stats)
        self.assertTrue( total == int(self.value[0]), message ) 

    def test_GLUE2ComputingServiceRunningJobs_OK (self):
        message = ("INFO:\n"
                   "I014 Description: Number of jobs higher than 1 million !\n"
                   "I014 Affected DN: %s\n"
                   "I014 Affected attribute: GLUE2ComputingServiceRunningJobs\n"
                   "I014 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingServiceWaitingJobs_OK (self):
        message = ("INFO:\n"
                   "I015 Description: Number of jobs higher than 1 million !\n"
                   "I015 Affected DN: %s\n"
                   "I015 Affected attribute: GLUE2ComputingServiceWaitingJobs\n"
                   "I015 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingServiceStagingJobs_OK (self):
        message = ("INFO:\n"
                   "I016 Description: Number of jobs higher than 1 million !\n"
                   "I016 Affected DN: %s\n"
                   "I016 Affected attribute: GLUE2ComputingServiceStagingJobs\n"
                   "I016 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingServiceSuspendedJobs_OK (self):
        message = ("INFO:\n"
                   "I017 Description: Number of jobs higher than 1 million !\n"
                   "I017 Affected DN: %s\n"
                   "I017 Affected attribute: GLUE2ComputingServiceSuspendedJobs\n"
                   "I017 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingServicePreLRMSWaitingJobs_OK (self):
        message = ("INFO:\n"
                   "I018 Description: Number of jobs higher than 1 million !\n"
                   "I018 Affected DN: %s\n"
                   "I018 Affected attribute: GLUE2ComputingServicePreLRMSWaitingJobs\n"
                   "I018 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

#------------------------------------- GLUE2ComputingEndpoint ---------------------------------------

    def test_GLUE2EndpointStartTime_OK (self):
        try:
            creationtime = datetime.datetime(*(time.strptime(self.value[0],"%Y-%m-%dT%H:%M:%SZ")[0:6]))
            now = datetime.datetime.utcnow()
            twoyears = datetime.timedelta(days=730)
            if local_to_utc(creationtime.timetuple()) > now.timetuple():
                message = ("ERROR:\n"
                           "E010 Description: Start time in the future !\n"
                           "E010 Affected DN: %s\n"
                           "E010 Affected attribute: GLUE2EndpointStartTime\n"
                           "E010 Published value: %s\n") % (self.dn, self.value[0])
                status = False
            elif local_to_utc(creationtime.timetuple()) < (now - twoyears).timetuple():
                message = ("WARNING:\n"
                           "W006 Description: Start time more than two years old\n" 
                           "W006 Affected DN: %s\n"
                           "W006 Affected attribute: GLUE2EndpointStartTime\n"
                           "W006 Published value: %s\n") % (self.dn, self.value[0])
                status = False
            else:
                message = ""
                status = True
        except ValueError:
            message = "" 
            status = True
        self.assertTrue(status, message)

    def test_GLUE2EndpointIssuerCA_OK (self):
        message = ("INFO:\n"
                   "I019 Description: Issuer CA published as 'unknown'\n"
                   "I019 Affected DN: %s\n"
                   "I019 Affected attribute: GLUE2EndpointIssuerCA\n"
                   "I019 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( self.value[0] != 'unknown', message )

    def test_GLUE2EndpointTrustedCA_OK (self):
        message = ("INFO:\n"
                   "I020 Description: Trusted CA published as 'unknown'\n"
                   "I020 Affected DN: %s\n"
                   "I020 Affected attribute: GLUE2EndpointTrustedCA\n"
                   "I020 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( self.value[0] != 'unknown', message )

    def test_GLUE2EndpointDowntimeAnnounce_OK (self):
        try:
            creationtime = datetime.datetime(*(time.strptime(self.value[0],"%Y-%m-%dT%H:%M:%SZ")[0:6]))
            now = datetime.datetime.utcnow()
            year = datetime.timedelta(days=365)
            if local_to_utc(creationtime.timetuple()) > now.timetuple():
                message = ("ERROR:\n"
                           "E011 Description: Downtime announcement in the future !\n"
                           "E011 Affected DN: %s\n"
                           "E011 Affected attribute: GLUE2EndpointDowntimeAnnounce\n"
                           "E011 Published value: %s\n") % (self.dn, self.value[0])
                status = False
            elif local_to_utc(creationtime.timetuple()) < (now - year).timetuple():
                message = ("WARNING:\n"
                           "W007 Description: Downtime announcement more than one year old\n"
                           "W007 Affected DN: %s\n"
                           "W007 Affected attribute: GLUE2EndpointDowntimeAnnounce\n"
                           "W007 Published value: %s") % (self.dn, self.value[0])
                status = False
            else:
                message = ""
                status = True
        except ValueError:
            message = ""
            status = True
        self.assertTrue(status, message)

    def test_GLUE2EndpointDowntimeAnnounce_checkStart (self):
       message = ("WARNING:\n"
                  "W008 Description: Downtime announcement with no Downtime start published\n"
                  "W008 Affected DN: %s\n"
                  "W008 Affected attribute: GLUE2EndpointDowntimeAnnounce\n"
                  "W008 Published value: NA") % (self.dn)
       self.assertTrue('GLUE2EndpointDowntimeStart' in self.entry, message)

    def test_GLUE2EndpointDowntimeStart_OK (self):
        try:
            status = True
            message = ""
            starttime = datetime.datetime(*(time.strptime(self.value[0],"%Y-%m-%dT%H:%M:%SZ")[0:6]))
            now = datetime.datetime.utcnow()
            year = datetime.timedelta(days=365)
            if 'GLUE2EndpointDowntimeEnd' in self.entry:
                endtime = datetime.datetime(*(time.strptime(self.entry['GLUE2EndpointDowntimeEnd'][0],"%Y-%m-%dT%H:%M:%SZ")[0:6]))
                if starttime > endtime:
                    message = ("ERROR:\n" 
                               "E012 Description: Downtime start time is older than end time !\n"
                               "E012 Affected DN: %s\n"
                               "E012 Affected attribute: GLUE2EndpointDowntimeStart and GLUE2EndpointDowntimeEnd\n"
                               "E012 Published value: %s and %s\n") % \
                               (self.dn, self.value[0], self.entry['GLUE2EndpointDowntimeEnd'][0])
                    status = False
            elif local_to_utc(starttime.timetuple()) > (now + year).timetuple():
                message = ("WARNING:\n"
                           "W009 Description: Downtime start time is scheduled more than one year ahead\n"
                           "W009 Affected DN: %s\n"
                           "W009 Affected attribute: GLUE2EndpointDowntimeStart\n"
                           "W009 Published value: %s\n") % (self.dn, self.value[0])
                status = False
            elif local_to_utc(starttime.timetuple()) < (now - year).timetuple():
                message = ("WARNING:\n"
                           "W010 Description: Downtime start time more than one year old\n"
                           "W010 Affected DN: %s\n"
                           "W010 Affected attribute: GLUE2EndpointDowntimeStart\n"
                           "W010 Published value: %s\n") % (self.dn, self.value[0])
                status = False
        except ValueError:
            message = "" 
            status = True
        self.assertTrue(status, message)

    def test_GLUE2EndpointDowntimeEnd_OK (self):
        try:
            status = True
            message = ""
            endtime = datetime.datetime(*(time.strptime(self.value[0],"%Y-%m-%dT%H:%M:%SZ")[0:6]))
            now = datetime.datetime.utcnow()
            year = datetime.timedelta(days=365)
            week = datetime.timedelta(days=7)
            if 'GLUE2EndpointDowntimeStart' not in self.entry:
                message = ("ERROR:\n"
                           "E013 Description: Downtime end time is published without a start time !\n"
                           "E013 Affected DN: %s\n"
                           "E013 Affected attribute: GLUE2EndpointDowntimeStart\n"
                           "E013 Published value: NA\n") % (self.dn)
                status = False
            elif local_to_utc(endtime.timetuple()) > (now + year).timetuple():
                message = ("WARNING:\n"
                           "W011 Description: Downtime end time is scheduled more than one year ahead\n"
                           "W011 Affected DN: %s\n"
                           "W011 Affected attribute: GLUE2EndpointDowntimeEnd\n"
                           "W011 Published value: %s\n") % (self.dn, self.value[0])
                status = False
            elif local_to_utc(endtime.timetuple()) < (now - week).timetuple():
                message = ("WARNING:\n"
                           "W012 Description: Downtime end time is more than one week old\n"
                           "W012 Affected DN: %s\n"
                           "W012 Affected attribute: GLUE2EndpointDowntimeEnd\n"
                           "W012 Published value: %s\n") % (self.dn, self.value[0])
                status = False
        except ValueError:
            message = ""
            status = True
        self.assertTrue(status, message)

    def test_GLUE2ComputingEndpointTotalJobs_OK (self):
        total = 0
        job_stats = ""
        for job in ['GLUE2ComputingEndpointRunningJobs',
                    'GLUE2ComputingEndpointWaitingJobs',
                    'GLUE2ComputingEndpointStagingJobs',
                    'GLUE2ComputingEndpointSuspendedJobs',
                    'GLUE2ComputingEndpointPreLRMSWaitingJobs']:
            if job in self.entry:
                total = total + int(self.entry[job][0])
                job_stats = job_stats + " %s=%s" % (job,self.entry[job][0])
        message = ("WARNING:\n"
                   "W013 Description: Incoherent number of total jobs\n"
                   "W013 Affected DN: %s\n"
                   "W013 Affected attribute: GLUE2ComputingEndpointTotalJobs\n"
                   "W013 Published value: %s vs %s\n") % (self.dn, self.value[0], job_stats)
        self.assertTrue( total == int(self.value[0]), message )

    def test_GLUE2ComputingEndpointRunningJobs_OK (self):
        message = ("INFO:\n"
                   "I021 Description: Number of jobs higher than 1 million !\n"
                   "I021 Affected DN: %s\n"
                   "I021 Affected attribute: GLUE2ComputingEndpointRunningJobs\n"
                   "I021 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingEndpointWaitingJobs_OK (self):
        message = ("INFO:\n"
                   "I022 Description: Number of jobs higher than 1 million !\n"
                   "I022 Affected DN: %s\n"
                   "I022 Affected attribute: GLUE2ComputingEndpointWaitingJobs\n"
                   "I022 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingEndpointStagingJobs_OK (self):
        message = ("INFO:\n"
                   "I023 Description: Number of jobs higher than 1 million !\n"
                   "I023 Affected DN: %s\n"
                   "I023 Affected attribute: GLUE2ComputingEndpointStagingJobs\n"
                   "I023 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingEndpointSuspendedJobs_OK (self):
        message = ("INFO:\n"
                   "I024 Description: Number of jobs higher than 1 million !\n"
                   "I024 Affected DN: %s\n"
                   "I024 Affected attribute: GLUE2ComputingEndpointSuspendedJobs\n"
                   "I024 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingEndpointPreLRMSWaitingJobs_OK (self):
        message = ("INFO:\n"
                   "I025 Description: Number of jobs higher than 1 million !\n"
                   "I025 Affected DN: %s\n"
                   "I025 Affected attribute: GLUE2ComputingEndpointPreLRMSWaitingJobs\n"
                   "I025 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

#------------------------------------- GLUE2ComputingShare ---------------------------------------

    def test_GLUE2ComputingShareMaxWallTime_OK (self):
        message = ("INFO:\n"
                   "I026 Description: Default value published\n"
                   "I026 Affected DN: %s\n"
                   "I026 Affected attribute: GLUE2ComputingShareMaxWallTime\n"
                   "I026 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMaxMultiSlotWallTime_OK (self):
        message = ("INFO:\n"
                   "I027 Description: Default value published\n"
                   "I027 Affected DN: %s\n"
                   "I027 Affected attribute: GLUE2ComputingShareMaxMultiSlotWallTime\n"
                   "I027 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareDefaultWallTime_OK (self):
        message = ("INFO:\n"
                   "I028 Description: Default value published\n"
                   "I028 Affected DN: %s\n"
                   "I028 Affected attribute: GLUE2ComputingShareDefaultWallTime\n"
                   "I028 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMinWallTime_OK (self):
        if 'GLUE2ComputingShareMaxWallTime' in self.entry:
            message = ("WARNING:\n"
                       "W014 Description: Incoherent attribute range\n"
                       "W014 Affected DN: %s\n"
                       "W014 Affected attribute: GLUE2ComputingShareMinWallTime and GLUE2ComputingShareMaxWallTime\n"
                       "W014 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxWallTime'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxWallTime'][0]), message )

    def test_GLUE2ComputingShareDefaultWallTime_MaxRange (self):
        if 'GLUE2ComputingShareMaxWallTime' in self.entry:
            message = ("WARNING:\n"
                       "W015 Description: Attribute out of predefined range \n"
                       "W015 Affected DN: %s\n"
                       "W015 Affected attribute: GLUE2ComputingShareDefaultWallTime and GLUE2ComputingShareMaxWallTime\n"
                       "W015 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxWallTime'][0])   
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxWallTime'][0]), message )  
            
    def test_GLUE2ComputingShareDefaultWallTime_MinRange (self):
        if 'GLUE2ComputingShareMinWallTime' in self.entry:
            message = ("WARNING:\n"
                       "W016 Description: Attribute out of predefined range\n"
                       "W016 Affected DN: %s\n"
                       "W016 Affected attribute: GLUE2ComputingShareDefaultWallTime and GLUE2ComputingShareMinWallTime\n"
                       "W016 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMinWallTime'][0])
            self.assertTrue ( int(self.value[0]) >= int(self.entry['GLUE2ComputingShareMinWallTime'][0]), message )

    def test_GLUE2ComputingShareMaxCPUTime_OK (self):
        message = ("INFO:\n"
                   "I029 Description: Default value published\n"
                   "I029 Affected DN: %s\n"
                   "I029 Affected attribute: GLUE2ComputingShareMaxCPUTime\n"
                   "I029 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMaxTotalCPUTime_OK (self):
        message = ("INFO:\n"
                   "I030 Description: Default value published\n"
                   "I030 Affected DN: %s\n"
                   "I030 Affected attribute: GLUE2ComputingShareMaxTotalCPUTime\n"
                   "I030 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareDefaultCPUTime_OK (self):
        message = ("INFO:\n"
                   "I031 Description: Default value published\n"
                   "I031 Affected DN: %s\n"
                   "I031 Affected attribute: GLUE2ComputingShareDefaultCPUTime\n"
                   "I031 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMinCPUTime_OK (self):
        if 'GLUE2ComputingShareMaxCPUTime' in self.entry:
            message = ("WARNING:\n"
                       "W017 Description: Incoherent attribute range\n"
                       "W017 Affected DN: %s\n"
                       "W017 Affected attribute: GLUE2ComputingShareMinCPUTime and GLUE2ComputingShareMaxCPUTime\n"
                       "W017 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxCPUTime'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxCPUTime'][0]), message )

    def test_GLUE2ComputingShareDefaultCPUTime_MaxRange (self):
        if 'GLUE2ComputingShareMaxCPUTime' in self.entry:
            message = ("WARNING:\n"
                       "W018 Description: Attribute out of predefined range\n"
                       "W018 Affected DN: %s\n"
                       "W018 Affected attribute: GLUE2ComputingShareDefaultCPUTime and GLUE2ComputingShareMaxCPUTime\n"
                       "W018 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxCPUTime'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxCPUTime'][0]), message )

    def test_GLUE2ComputingShareDefaultCPUTime_MinRange (self):
        if 'GLUE2ComputingShareMinCPUTime' in self.entry:
            message = ("WARNING:\n"
                       "W019 Description: Attribute out of predefined range\n"
                       "W019 Affected DN: %s\n"
                       "W019 Affected attribute: GLUE2ComputingShareDefaultCPUTime and GLUE2ComputingShareMinCPUTime\n"
                       "W019 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMinCPUTime'][0])
            self.assertTrue ( int(self.value[0]) >= int(self.entry['GLUE2ComputingShareMinCPUTime'][0]), message )

    def test_GLUE2ComputingShareMaxTotalJobs_default (self):
        message = ("INFO:\n"
                   "I032 Description: Default value published\n"
                   "I032 Affected DN: %s\n"
                   "I032 Affected attribute: GLUE2ComputingShareMaxTotalJobs\n"
                   "I032 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMaxTotalJobs_zero (self):
        message = ("WARNING:\n"
                   "W020 Description: Number of total jobs is zero\n"
                   "W020 Affected DN: %s\n"
                   "W020 Affected attribute: GLUE2ComputingShareMaxTotalJobs\n"
                   "W020 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) != 0, message )

    def test_GLUE2ComputingShareMaxTotalJobs_OK (self):
        running = True
        waiting = True
        if 'GLUE2ComputingShareMaxRunningJobs' in self.entry:
            message = ("WARNING:\n"
                       "W021 Description: Attribute out of predefined range\n"
                       "W021 Affected DN: %s\n"
                       "W021 Affected attribute: GLUE2ComputingShareMaxTotalJobs and GLUE2ComputingShareMaxRunningJobs\n"
                       "W021 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxRunningJobs'][0])
            running = int(self.value[0]) >= int(self.entry['GLUE2ComputingShareMaxRunningJobs'][0])
        if 'GLUE2ComputingShareMaxWaitingJobs' in self.entry:
            message = ("WARNING:\n"
                       "W021 Description: Attribute out of predefined range\n"
                       "W021 Affected DN: %s\n"
                       "W021 Affected attribute: GLUE2ComputingShareMaxTotalJobs and GLUE2ComputingShareMaxWaitingJobs\n"
                       "W021 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxWaitingJobs'][0])
            waiting = int(self.value[0]) >= int(self.entry['GLUE2ComputingShareMaxWaitingJobs'][0])
        self.assertTrue ( running or waiting, message )

    def test_GLUE2ComputingShareMaxUserRunningJobs_zero (self):
        message = ("WARNING:\n"
                   "W022 Description: Number of jobs is zero\n"
                   "W022 Affected DN: %s\n"
                   "W022 Affected attribute: GLUE2ComputingShareMaxUserRunningJobs\n"
                   "W022 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) != 0, message )

    def test_GLUE2ComputingShareMaxUserRunningJobs_OK (self):
        if 'GLUE2ComputingShareMaxRunningJobs' in self.entry:
           message = ("WARNING:\n"
                      "W023 Description: Incoherent attribute range\n"
                      "W023 Affected DN: %s\n"
                      "W023 Affected attribute: GLUE2ComputingShareMaxUserRunningJobs"
                            " and GLUE2ComputingShareMaxRunningJobs\n"
                      "W023 Published value: %s and %s\n") % \
                      (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxRunningJobs'][0])
           self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxRunningJobs'][0]), message )

    def test_GLUE2ComputingShareMaxRunningJobs_OK (self):
        message = ("INFO:\n"
                   "I033 Description: Default value published\n"
                   "I033 Affected DN: %s\n"
                   "I033 Affected attribute: GLUE2ComputingShareMaxRunningJobs\n"
                   "I033 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMaxWaitingJobs_OK (self):
        message = ("INFO:\n"
                   "I034 Description: Default value published\n"
                   "I034 Affected DN: %s\n"
                   "I034 Affected attribute: GLUE2ComputingShareMaxWaitingJobs\n"
                   "I034 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMaxSlotsPerJob_zero (self):
        message = ("WARNING:\n"
                   "W024 Description: Number of maximum slots per job is zero\n"
                   "W024 Affected DN: %s\n"
                   "W024 Affected attribute: GLUE2ComputingShareMaxSlotsPerJob\n"
                   "W024 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) != 0, message )

    def test_GLUE2ComputingShareTotalJobs_OK (self):
        total = 0
        job_stats = ""
        for job in ['GLUE2ComputingShareRunningJobs',
                    'GLUE2ComputingShareLocalRunningJobs',
                    'GLUE2ComputingShareWaitingJobs',
                    'GLUE2ComputingShareLocalWaitingJobs',
                    'GLUE2ComputingShareSuspendedJobs',
                    'GLUE2ComputingShareLocalSuspendedJobs',
                    'GLUE2ComputingShareStagingJobs',
                    'GLUE2ComputingSharePreLRMSWaitingJobs']:
            if job in self.entry:
                total = total + int(self.entry[job][0])
                job_stats = job_stats + " %s=%s" % (job,self.entry[job][0])
        message = ("WARNING:\n"
                   "W025 Description: Incoherent number of total jobs\n"
                   "W025 Affected DN: %s\n"
                   "W025 Affected attribute: GLUE2ComputingShareTotalJobs\n"
                   "W025 Published value: %s vs %s\n") % (self.dn, self.value[0], job_stats)
        self.assertTrue( total == int(self.value[0]), message )

    def test_GLUE2ComputingShareRunningJobs_OK (self):
        message = ("INFO:\n"
                   "I035 Description: Number of jobs higher than 1 million !\n"
                   "I035 Affected DN: %s\n"
                   "I035 Affected attribute: GLUE2ComputingShareRunningJobs\n"
                   "I035 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareLocalRunningJobs_OK (self):
        message = ("INFO:\n"
                   "I036 Description: Number of jobs higher than 1 million !\n"
                   "I036 Affected DN: %s\n"
                   "I036 Affected attribute: GLUE2ComputingShareLocalRunningJobs\n"
                   "I036 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareWaitingJobs_OK (self):
        message = ("INFO:\n"
                   "I037 Description: Number of jobs higher than 1 million !\n"
                   "I037 Affected DN: %s\n"
                   "I037 Affected attribute: GLUE2ComputingShareWaitingJobs\n"
                   "I037 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareLocalWaitingJobs_OK (self):
        message = ("INFO:\n"
                   "I038 Description: Number of jobs higher than 1 million !\n"
                   "I038 Affected DN: %s\n"
                   "I038 Affected attribute: GLUE2ComputingShareLocalWaitingJobs\n"
                   "I038 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareSuspendedJobs_OK (self):
        message = ("INFO:\n"
                   "I039 Description: Number of jobs higher than 1 million !\n"
                   "I039 Affected DN: %s\n"
                   "I039 Affected attribute: GLUE2ComputingShareSuspendedJobs\n"
                   "I039 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareLocalSuspendedJobs_OK (self):
        message = ("INFO:\n"
                   "I040 Description: Number of jobs higher than 1 million !\n"
                   "I040 Affected DN: %s\n"
                   "I040 Affected attribute: GLUE2ComputingShareLocalSuspendedJobs\n"
                   "I040 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareStagingJobs_OK (self):
        message = ("INFO:\n"
                   "I041 Description: Number of jobs higher than 1 million !\n"
                   "I041 Affected DN: %s\n"
                   "I041 Affected attribute: GLUE2ComputingShareStagingJobs\n"
                   "I041 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingSharePreLRMSWaitingJobs_OK (self):
        message = ("INFO:\n"
                   "I042 Description: Number of jobs higher than 1 million !\n"
                   "I042 Affected DN: %s\n"
                   "I042 Affected attribute: GLUE2ComputingSharePreLRMSWaitingJobs\n"
                   "I042 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareMaxMainMemory_MinRange (self):
        message = ("WARNING:\n"
                   "W026 Description: Memory lower than 100 MB !\n"
                   "W026 Affected DN: %s\n"
                   "W026 Affected attribute: GLUE2ComputingShareMaxMainMemory\n"
                   "W026 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) >= 100, message )
   
    def test_GLUE2ComputingShareMaxMainMemory_MaxRange (self):
        message = ("INFO:\n"
                   "I043 Description: Memory higher than 100,000 MB !\n"
                   "I043 Affected DN: %s\n"
                   "I043 Affected attribute: GLUE2ComputingShareMaxMainMemory\n"
                   "I043 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 100000, message )

    def test_GLUE2ComputingShareGuaranteedMainMemory_MinRange (self):
        if 'GLUE2ComputingShareMaxMainMemory' in self.entry:
            message = ("WARNING:\n"
                       "W027 Description: Incoherent attribute range\n"
                       "W027 Affected DN: %s\n"
                       "W027 Affected attribute: GLUE2ComputingShareGuaranteedMainMemory"
                             " and GLUE2ComputingShareMaxMainMemory\n"
                       "W027 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxMainMemory'][0])
            self.assertTrue( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxMainMemory'][0]), message )

    def test_GLUE2ComputingShareGuaranteedMainMemory_MaxRange (self):
        message = ("INFO:\n"
                   "I044 Description: Memory higher than 100,000 MB !\n"
                   "I044 Affected DN: %s\n"
                   "I044 Affected attribute: GLUE2ComputingShareGuaranteedMainMemory\n"
                   "I044 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 100000, message )

    def test_GLUE2ComputingShareMaxVirtualMemory_MinRange (self):
        if 'GLUE2ComputingShareMaxMainMemory' in self.entry:
            message = ("WARNING:\n"
                       "W028 Description: Incoherent attribute range\n"
                       "W028 Affected DN: %s\n"
                       "W028 Affected attribute: GLUE2ComputingShareMaxVirtualMemory"
                             " and GLUE2ComputingShareMaxMainMemory\n"
                       "W028 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxMainMemory'][0])
            self.assertTrue( int(self.value[0]) >= int(self.entry['GLUE2ComputingShareMaxMainMemory'][0]), message )

    def test_GLUE2ComputingShareMaxVirtualMemory_MaxRange (self):
        message = ("INFO:\n"
                   "I045 Description: Memory higher than 100,000 MB !\n"
                   "I045 Affected DN: %s\n"
                   "I045 Affected attribute: GLUE2ComputingShareMaxVirtualMemory\n"
                   "I045 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 100000, message )

    def test_GLUE2ComputingShareGuaranteedVirtualMemory_MinRange (self):
        if 'GLUE2ComputingShareMaxVirtualMemory' in self.entry:
            message = ("WARNING:\n"
                       "W029 Description: Incoherent attribute range\n"
                       "W029 Affected DN: %s\n"
                       "W029 Affected attribute: GLUE2ComputingShareGuaranteedVirtualMemory"
                             " and GLUE2ComputingShareMaxVirtualMemory\n"
                       "W029 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxVirtualMemory'][0])
            self.assertTrue( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxVirtualMemory'][0]), message )

    def test_GLUE2ComputingShareGuaranteedVirtualMemory_MaxRange (self):
        message = ("INFO:\n"
                   "I046 Description: Memory higher than 100,000 MB !\n"
                   "I046 Affected DN: %s\n"
                   "I046 Affected attribute: GLUE2ComputingShareGuaranteedVirtualMemory\n"
                   "I046 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 100000, message )

    def test_GLUE2ComputingShareEstimatedAverageWaitingTime_OK (self):
        message = ("INFO:\n"
                   "I046 Description: Number of seconds higher than 1 million !\n"
                   "I046 Affected DN: %s\n"
                   "I046 Affected attribute: GLUE2ComputingShareEstimatedAverageWaitingTime\n"
                   "I046 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareEstimatedWorstWaitingTime_OK (self):
        message = ("INFO:\n"
                   "I047 Description: Number of seconds higher than 1 million !\n"
                   "I047 Affected DN: %s\n"
                   "I047 Affected attribute: GLUE2ComputingShareEstimatedWorstWaitingTime\n"
                   "I047 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareFreeSlots_OK (self):
        message = ("INFO:\n"
                   "I048 Description: Number of slots higher than 1 million !\n"
                   "I048 Affected DN: %s\n"
                   "I048 Affected attribute: GLUE2ComputingShareFreeSlots\n"
                   "I048 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareUsedSlots_OK (self):
        message = ("INFO:\n"
                   "I049 Description: Number of slots higher than 1 million !\n"
                   "I049 Affected DN: %s\n"
                   "I049 Affected attribute: GLUE2ComputingShareUsedSlots\n"
                   "I049 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareRequestedSlots_OK (self):
        message = ("INFO:\n"
                   "I050 Description: Number of slots higher than 1 million !\n"
                   "I050 Affected DN: %s\n"
                   "I050 Affected attribute: GLUE2ComputingShareRequestedSlots\n"
                   "I050 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

#------------------------------------- GLUE2ComputingManager ---------------------------------------

    def test_GLUE2ComputingManagerTotalLogicalCPUs_MinRange (self):
        message = ("INFO:\n"
                   "I051 Description: Number of logical CPUs lower than 10 !\n"
                   "I051 Affected DN: %s\n"
                   "I051 Affected attribute: GLUE2ComputingManagerTotalLogicalCPUs\n"
                   "I051 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) >= 10, message )

    def test_GLUE2ComputingManagerTotalLogicalCPUs_MaxRange (self):
        message = ("INFO:\n"
                   "I052 Description: Number of logical CPUs greater than 1 million !\n"
                   "I052 Affected DN: %s\n"
                   "I052 Affected attribute: GLUE2ComputingManagerTotalLogicalCPUs\n"
                   "I052 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )
        
    def test_GLUE2ComputingManagerTotalPhysicalCPUs_OK (self):
        if 'GLUE2ComputingManagerTotalLogicalCPUs' in self.entry:
            message = ("WARNING:\n"
                       "W030 Description: Incoherent attribute range\n"
                       "W030 Affected DN: %s\n"
                       "W030 Affected attribute: GLUE2ComputingManagerTotalPhysicalCPUs"
                             " and GLUE2ComputingManagerTotalLogicalCPUs\n"
                       "W030 Published value: %s and %s\n") % \
                      (self.dn, self.value[0], self.entry['GLUE2ComputingManagerTotalLogicalCPUs'][0])
            self.assertTrue( int(self.value[0]) <= int(self.entry['GLUE2ComputingManagerTotalLogicalCPUs'][0]) , message) 

    def test_GLUE2ComputingManagerTotalPhysicalCPUs_MinRange (self):
        message = ("INFO:\n"
                   "I053 Description: Number of physical CPUs lower than 10 !\n"
                   "I053 Affected DN: %s\n"
                   "I053 Affected attribute: GLUE2ComputingManagerTotalPhysicalCPUs\n"
                   "I053 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) >= 10, message )

    def test_GLUE2ComputingManagerTotalPhysicalCPUs_MaxRange (self):
        message = ("INFO:\n"
                   "I054 Description: Number of logical CPUs greater than 1 million !\n"
                   "I054 Affected DN: %s\n"
                   "I054 Affected attribute: GLUE2ComputingManagerTotalPhysicalCPUs\n"
                   "I054 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerTotalSlots_OK (self):
        if 'GLUE2ComputingManagerTotalLogicalCPUs' in self.entry:
            message = ("WARNING:\n"
                       "W031 Description: Incoherent attribute range\n"
                       "W031 Affected DN: %s\n"
                       "W031 Affected attribute: GLUE2ComputingManagerTotalSlots"
                             " and GLUE2ComputingManagerTotalLogicalCPUs\n"
                       "W031 Published value: %s and %s\n") % \
                      (self.dn, self.value[0], self.entry['GLUE2ComputingManagerTotalLogicalCPUs'][0])
            self.assertTrue( int(self.value[0]) <= int(self.entry['GLUE2ComputingManagerTotalLogicalCPUs'][0])*2 , message)

    def test_GLUE2ComputingManagerTotalSlots_MinRange (self):
        message = ("INFO:\n"
                   "I055 Description: Number of total slots lower than 10 !\n"
                   "I055 Affected DN: %s\n"
                   "I055 Affected attribute: GLUE2ComputingManagerTotalSlots\n"
                   "I055 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) >= 10, message )

    def test_GLUE2ComputingManagerTotalSlots_MaxRange (self):
        message = ("INFO:\n"
                   "I056 Description: Number of total slots greater than 1 million !\n"
                   "I056 Affected DN: %s\n"
                   "I056 Affected attribute: GLUE2ComputingManagerTotalSlots\n"
                   "I056 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerSlotsUsedByLocalJobs_OK (self):
        if 'GLUE2ComputingManagerTotalSlots' in self.entry:
            message = ("WARNING:\n"
                       "W032 Description: Incoherent attribute range\n"
                       "W032 Affected DN: %s\n"
                       "W032 Affected attribute: GLUE2ComputingManagerSlotsUsedByLocalJobs"
                             " and GLUE2ComputingManagerTotalSlots\n"
                       "W032 Published value: %s and %s\n") % \
                       (self.dn, self.value[0],self.entry['GLUE2ComputingManagerTotalSlots'][0])
            self.assertTrue( int(self.value[0]) < int(self.entry['GLUE2ComputingManagerTotalSlots']), message )

    def test_GLUE2ComputingManagerSlotsUsedByGridJobs_OK (self):
        if 'GLUE2ComputingManagerTotalSlots' in self.entry:
            message = ("WARNING:\n"
                       "W033 Description: Incoherent attribute range\n"
                       "W033 Affected DN: %s\n"
                       "W033 Affected attribute: GLUE2ComputingManagerSlotsUsedByGridJobs"
                             " and GLUE2ComputingManagerTotalSlots\n"
                       "W033 Published value: %s and %s\n") % \
                       (self.dn, self.value[0],self.entry['GLUE2ComputingManagerTotalSlots'][0])
            self.assertTrue( int(self.value[0]) < int(self.entry['GLUE2ComputingManagerTotalSlots']), message )

    def test_GLUE2ComputingManagerWorkingAreaTotal_OK (self):
        message = ("INFO:\n"
                   "I057 Description: Total working area greater than 1 million GB !\n"
                   "I057 Affected DN: %s\n"
                   "I057 Affected attribute: GLUE2ComputingManagerWorkingAreaTotal\n"
                   "I057 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerWorkingAreaFree_OK (self):
        message = ("INFO:\n"
                   "I058 Description: Free working area greater than 1 million GB !\n"
                   "I058 Affected DN: %s\n"
                   "I058 Affected attribute: GLUE2ComputingManagerWorkingAreaFree\n"
                   "I058 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerWorkingAreaMultiSlotTotal_OK (self):
        message = ("INFO:\n"
                   "I059 Description: Multi slot total working area greater than 1 million GB !\n"
                   "I059 Affected DN: %s\n"
                   "I059 Affected attribute: GLUE2ComputingManagerWorkingAreaMultiSlotTotal\n"
                   "I059 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerWorkingAreaMultiSlotFree_OK (self):
        message = ("INFO:\n"
                   "I060 Description: Multi slot free working area greater than 1 million GB !\n"
                   "I060 Affected DN: %s\n"
                   "I060 Affected attribute: GLUE2ComputingManagerWorkingAreaMultiSlotFree\n"
                   "I060 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerCacheTotal_OK (self):
        message = ("INFO:\n"
                   "I061 Description: Total cache greater than 1 million GB !\n"
                   "I061 Affected DN: %s\n"
                   "I061 Affected attribute: GLUE2ComputingManagerCacheTotal\n"
                   "I061 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerCacheFree_OK (self):
        message = ("INFO:\n"
                   "I062 Description: Free cache greater than 1 million GB !\n"
                   "I062 Affected DN: %s\n"
                   "I062 Affected attribute: GLUE2ComputingManagerCacheTotal\n"
                   "I062 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

#------------------------------------- GLUE2ExecutionEnvironment ---------------------------------------

    def test_GLUE2ExecutionEnvironmentTotalInstances_MinRange (self):
        message = ("INFO:\n"
                   "I063 Description: Total instances less than 10 !\n"
                   "I063 Affected DN: %s\n"
                   "I063 Affected attribute: GLUE2ExecutionEnvironmentTotalInstances\n"
                   "I063 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) > 10, message )

    def test_GLUE2ExecutionEnvironmentTotalInstances_MaxRange (self):
        message = ("INFO:\n"
                   "I064 Description: Total instances more than 1 million !\n"
                   "I064 Affected DN: %s\n"
                   "I064 Affected attribute: GLUE2ExecutionEnvironmentTotalInstances\n"
                   "I064 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ExecutionEnvironmentUsedInstances_OK (self):
        if 'GLUE2ExecutionEnvironmentTotalInstances' in self.entry:
            message = ("INFO:\n"
                       "I065 Description: Incoherent attribute range\n"
                       "I065 Affected DN: %s\n"
                       "I065 Affected attribute: GLUE2ExecutionEnvironmentUsedInstances"
                             " and GLUE2ExecutionEnvironmentTotalInstances\n"
                       "I065 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2ExecutionEnvironmentTotalInstances'][0])
            self.assertTrue( int(self.value[0]) < int(self.entry['GLUE2ExecutionEnvironmentTotalInstances'][0]), message )

    def test_GLUE2ExecutionEnvironmentUnavailableInstances_OK (self):
        if 'GLUE2ExecutionEnvironmentTotalInstances' in self.entry:
            message = ("INFO:\n"
                       "I066 Description: Incoherent attribute range\n"
                       "I066 Affected DN: %s\n"
                       "I066 Affected attribute: GLUE2ExecutionEnvironmentUnavailableInstances"
                             " and GLUE2ExecutionEnvironmentTotalInstances\n"
                       "I066 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2ExecutionEnvironmentTotalInstances'][0])
            self.assertTrue( int(self.value[0]) < int(self.entry['GLUE2ExecutionEnvironmentTotalInstances'][0]), message )

    def test_GLUE2ExecutionEnvironmentPhysicalCPUs_MaxRange (self):
        message = ("INFO:\n"
                   "I067 Description: Number of physical CPUs greater than 10 !\n"
                   "I067 Affected DN: %s\n"
                   "I067 Affected attribute: GLUE2ExecutionEnvironmentPhysicalCPUs\n"
                   "I067 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) <= 10, message )

    def test_GLUE2ExecutionEnvironmentLogicalCPUs_MaxRange (self):
        message = ("INFO:\n"
                   "I068 Description: Number of logical CPUs greater than 1000 !\n"
                   "I068 Affected DN: %s\n"
                   "I068 Affected attribute: GLUE2ExecutionEnvironmentLogicalCPUs\n"
                   "I068 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000, message )

    def test_GLUE2ExecutionEnvironmentCPUClockSpeed_MaxRange (self):
        message = ("INFO:\n"
                   "I069 Description: CPU clock speed greater than 1000 !\n"
                   "I069 Affected DN: %s\n"
                   "I069 Affected attribute: GLUE2ExecutionEnvironmentCPUClockSpeed\n"
                   "I069 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) <= 10000, message )

    def test_GLUE2ExecutionEnvironmentCPUClockSpeed_MinRange (self):
        message = ("INFO:\n"
                   "I070 Description: CPU clock speed less than 100 !\n"
                   "I070 Affected DN: %s\n"
                   "I070 Affected attribute: GLUE2ExecutionEnvironmentCPUClockSpeed\n"
                   "I070 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) >= 100, message )

    def test_GLUE2ExecutionEnvironmentCPUTimeScalingFactor_MaxRange (self):
        message = ("INFO:\n"
                   "I071 Description: CPU time scaling factor greater than 1 !\n"
                   "I071 Affected DN: %s\n"
                   "I071 Affected attribute: GLUE2ExecutionEnvironmentCPUTimeScalingFactor\n"
                   "I071 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) <= 1, message )

    def test_GLUE2ExecutionEnvironmentCPUTimeScalingFactor_MinRange (self):
        message = ("INFO:\n"
                   "I072 Description: CPU time scaling factor less than 0.1 !\n"
                   "I072 Affected DN: %s\n"
                   "I072 Affected attribute: GLUE2ExecutionEnvironmentCPUTimeScalingFactor\n"
                   "I072 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( float(self.value[0]) > 0.1, message )

    def test_GLUE2ExecutionEnvironmentWallTimeScalingFactor_MaxRange (self):
        message = ("INFO:\n"
                   "I073 Description: Wall time scaling factor greater than 1 !\n"
                   "I073 Affected DN: %s\n"
                   "I073 Affected attribute: GLUE2ExecutionEnvironmentWallTimeScalingFactor\n"
                   "I073 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) <= 1, message )

    def test_GLUE2ExecutionEnvironmentWallTimeScalingFactor_MinRange (self):
        message = ("INFO:\n"
                   "I074 Description: Wall time scaling factor less than 0.1 !\n"
                   "I074 Affected DN: %s\n"
                   "I074 Affected attribute: GLUE2ExecutionEnvironmentWallTimeScalingFactor\n"
                   "I074 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( float(self.value[0]) > 0.1, message )

    def test_GLUE2ExecutionEnvironmentMainMemorySize_MaxRange (self):
        message = ("INFO:\n"
                   "I075 Description: Main memory size greater than 1 million MB !\n"
                   "I075 Affected DN: %s\n"
                   "I075 Affected attribute: GLUE2ExecutionEnvironmentMainMemorySize\n"
                   "I075 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ExecutionEnvironmentMainMemorySize_MinRange (self):
        message = ("INFO:\n"
                   "I076 Description: Main memory size less than 100 MB !\n"
                   "I076 Affected DN: %s\n"
                   "I076 Affected attribute: GLUE2ExecutionEnvironmentMainMemorySize\n"
                   "I076 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) >= 100, message )

    def test_GLUE2ExecutionEnvironmentVirtualMemorySize_MaxRange (self):
        message = ("INFO:\n"
                   "I077 Description: Virtual memory size greater than 1 million MB !\n"
                   "I077 Affected DN: %s\n"
                   "I077 Affected attribute: GLUE2ExecutionEnvironmentVirtualMemorySize\n"
                   "I077 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ExecutionEnvironmentVirtualMemorySize_MinRange (self):
        message = ("INFO:\n"
                   "I078 Description: Virtual memory size less than 100 MB !\n"
                   "I078 Affected DN: %s\n"
                   "I078 Affected attribute: GLUE2ExecutionEnvironmentVirtualMemorySize\n"
                   "I078 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) >= 100, message )

#------------------------------------- GLUE2ApplicationEnvironment ---------------------------------------

    def test_GLUE2ApplicationEnvironmentRemovalDate_OK (self):
        try:
           removaldate = datetime.datetime(*(time.strptime(self.value[0],"%Y-%m-%dT%H:%M:%SZ")[0:6]))
           now = datetime.datetime.utcnow()
           message = ("INFO:\n"
                      "I079 Description: Removal date in the past\n"
                      "I079 Affected DN: %s\n"
                      "I079 Affected attribute: GLUE2ApplicationEnvironmentRemovalDate\n"
                      "I079 Published value: %s\n") % (self.dn, self.value[0])
        except ValueError:
            message = ""
            status = True
        self.asserTrue ( local_to_utc(removaldate.timetuple()) < now.timetuple() , message )

    def test_GLUE2ApplicationEnvironmentMaxSlots_OK (self):
        message = ("INFO:\n"
                   "I080 Description: Number of maximum slots is zero\n"
                   "I080 Affected DN: %s\n"
                   "I080 Affected attribute: GLUE2ApplicationEnvironmentMaxSlots\n"
                   "I080 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) != 0, message )

    def test_GLUE2ApplicationEnvironmentMaxJobs_OK (self):
        message = ("INFO:\n"
                   "I081 Description: Number of maximum jobs is zero\n"
                   "I081 Affected DN: %s\n"
                   "I081 Affected attribute: GLUE2ApplicationEnvironmentMaxJobs\n"
                   "I081 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) != 0, message )
 
    def test_GLUE2ApplicationEnvironmentMaxUserSeats_OK (self):
        message = ("INFO:\n"
                   "I082 Description: Number of maximum user seats is zero\n"
                   "I082 Affected DN: %s\n"
                   "I082 Affected attribute: GLUE2ApplicationEnvironmentMaxUserSeats\n"
                   "I082 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) != 0, message )

    def test_GLUE2ApplicationEnvironmentFreeSlots_OK (self):
        if 'GLUE2ApplicationEnvironmentMaxSlots' in self.entry:
            message = ("INFO:\n"
                       "I083 Description: Incoherent attribute range\n"
                       "I083 Affected DN: %s\n"
                       "I083 Affected attribute: GLUE2ApplicationEnvironmentFreeSlots"
                             " and GLUE2ApplicationEnvironmentMaxSlots\n"
                       "I083 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2ApplicationEnvironmentMaxSlots'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ApplicationEnvironmentMaxSlots'][0]), message )

    def test_GLUE2ApplicationEnvironmentFreeJobs_OK (self):
        if 'GLUE2ApplicationEnvironmentMaxJobs' in self.entry:
            message = ("INFO:\n"
                       "I084 Description: Incoherent attribute range\n"
                       "I084 Affected DN: %s\n"
                       "I084 Affected attribute: GLUE2ApplicationEnvironmentFreeJobs"
                             " and GLUE2ApplicationEnvironmentMaxJobs\n"
                       "I084 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2ApplicationEnvironmentMaxJobs'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ApplicationEnvironmentMaxJobs'][0]), message )

    def test_GLUE2ApplicationEnvironmentFreeUserSeats_OK (self):
        if 'GLUE2ApplicationEnvironmentMaxUserSeats' in self.entry:
            message = ("INFO:\n"
                       "I085 Description: Incoherent attribute range\n"
                       "I085 Affected DN: %s\n"
                       "I085 Affected attribute: GLUE2ApplicationEnvironmentFreeUserSeats"
                             " and GLUE2ApplicationEnvironmentMaxUserSeats\n"
                       "I085 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2ApplicationEnvironmentMaxUserSeats'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ApplicationEnvironmentMaxUserSeats'][0]), message )

#------------------------------------- GLUE2StorageServiceCapacity ---------------------------------------

    def test_GLUE2StorageServiceCapacityTotalSize_OK (self):
        total = 0
        cap_stats = ""
        for cap in ['GLUE2StorageServiceCapacityFreeSize',
                    'GLUE2StorageServiceCapacityUsedSize',
                    'GLUE2StorageServiceCapacityReservedSize']:
            if cap in self.entry:
                total = total + int(self.entry[cap][0])
                cap_stats = cap_stats + " %s=%s" % (cap,self.entry[cap][0])
        message = ("ERROR:\n"
                   "E014 Description: Incoherent number of total capacity\n"
                   "E014 Affected DN: %s\n"
                   "E014 Affected attribute: GLUE2StorageServiceCapacityTotalSize\n"
                   "E014 Published value: %s vs %s\n") % (self.dn, self.value[0], cap_stats)
        self.assertTrue( total == int(self.value[0]), message )

    def test_GLUE2StorageServiceCapacityTotalSize_MinRange (self):
        if 'GLUE2StorageServiceCapacityType' in self.entry:
            if self.entry['GLUE2StorageServiceCapacityType'][0] == 'online' or \
               self.entry['GLUE2StorageServiceCapacityType'][0] == 'nearline':
                   message = ("INFO:\n"
                              "I086 Description: Total capacity size less than 1000 GB !\n"
                              "I086 Affected DN: %s\n"
                              "I086 Affected attribute: GLUE2StorageServiceCapacityTotalSize\n"
                              "I086 Published value: %s\n") % (self.dn, self.value[0])
                   self.assertTrue ( int(self.value[0]) >= 1000 , message ) 

    def test_GLUE2StorageServiceCapacityTotalSize_MaxRange (self):
        if 'GLUE2StorageServiceCapacityType' in self.entry:
            if self.entry['GLUE2StorageServiceCapacityType'][0] == 'online' or \
               self.entry['GLUE2StorageServiceCapacityType'][0] == 'nearline':
                   message = ("INFO:\n"
                              "I087 Description: Total capacity size greater than 1 million GB !\n"
                              "I087 Affected DN: %s\n"
                              "I087 Affected attribute: GLUE2StorageServiceCapacityTotalSize\n"
                              "I087 Published value: %s\n") % (self.dn, self.value[0])
                   self.assertTrue ( int(self.value[0]) <= 1000000 , message )

    def test_GLUE2StorageServiceCapacityFreeSize_OK (self):
        if 'GLUE2StorageServiceCapacityTotalSize' in self.entry:
            message = ("ERROR:\n"
                       "E015 Description: Incoherent attribute range\n"
                       "E015 Affected DN: %s\n"
                       "E015 Affected attribute: GLUE2StorageServiceCapacityFreeSize"
                             " and GLUE2StorageServiceCapacityTotalSize\n "
                       "E015 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2StorageServiceCapacityTotalSize'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2StorageServiceCapacityTotalSize'][0]), message )

    def test_GLUE2StorageServiceCapacityUsedSize_OK (self):
        if 'GLUE2StorageServiceCapacityTotalSize' in self.entry:
            message = ("ERROR:\n"
                       "E016 Description: Incoherent attribute range\n"
                       "E016 Affected DN: %s\n"
                       "E016 Affected attribute: GLUE2StorageServiceCapacityUsedSize"
                             " and GLUE2StorageServiceCapacityTotalSize\n "
                       "E016 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2StorageServiceCapacityTotalSize'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2StorageServiceCapacityTotalSize'][0]), message )

    def test_GLUE2StorageServiceCapacityReservedSize_OK (self):
        if 'GLUE2StorageServiceCapacityTotalSize' in self.entry:
            message = ("ERROR:\n"
                       "E017 Description: Incoherent attribute range\n"
                       "E017 Affected DN: %s\n"
                       "E017 Affected attribute: GLUE2StorageServiceCapacityReservedSize"
                             " and GLUE2StorageServiceCapacityTotalSize\n "
                       "E017 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2StorageServiceCapacityTotalSize'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2StorageServiceCapacityTotalSize'][0]), message )

#------------------------------------- GLUE2StorageShare ---------------------------------------

    def test_GLUE2StorageShareAccessLatency_OK (self):
        message = ("INFO:\n"
                   "I088 Description: Access latency is 'offline'\n"
                   "I088 Affected DN: %s\n"
                   "I088 Affected attribute: GLUE2StorageShareAccessLatency\n"
                   "I088 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( self.value[0] != 'offline', message )

    def test_GLUE2StorageShareDefaultLifeTime_OK (self):
        message = ("INFO:\n"
                   "I089 Description: Default life time less than 100000 seconds\n"
                   "I089 Affected DN: %s\n"
                   "I089 Affected attribute: GLUE2StorageShareDefaultLifeTime\n"
                   "I089 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) >= 100000 , message )

    def test_GLUE2StorageShareMaximumLifeTime_OK (self):
        message = ("INFO:\n"
                   "I090 Description: Maximum life time less than 100000 seconds\n"
                   "I090 Affected DN: %s\n"
                   "I090 Affected attribute: GLUE2StorageShareMaximumLifeTime\n"
                   "I090 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) >= 100000 , message )

#------------------------------------- GLUE2StorageShareCapacity ---------------------------------------

    def test_GLUE2StorageShareCapacityTotalSize_OK (self):
        total = 0
        share_stats = ""
        for share in ['GLUE2StorageShareCapacityFreeSize', 'GLUE2StorageShareCapacityUsedSize']:
            if share in self.entry:
                total = total + int(self.entry[share][0])
                share_stats = share_stats + " %s=%s" % (share,self.entry[share][0])
        message = ("ERROR:\n"
                   "E018 Description: Incoherent number of total share capacity\n"
                   "E018 Affected DN: %s\n"
                   "E018 Affected attribute: GLUE2StorageShareCapacityTotalSize\n"
                   "E018 Published value: %s vs %s\n") % (self.dn, self.value[0], share_stats)
        self.assertTrue( total <= int(self.value[0]), message )

    def test_GLUE2StorageShareCapacityTotalSize_MinRange (self):
        message = ("INFO:\n"
                   "I091 Description: Total share capacity size less than 1000 GB !\n"
                   "I091 Affected DN: %s\n"
                   "I091 Affected attribute: GLUE2StorageShareCapacityTotalSize\n"
                   "I091 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) >= 1000, message )

    def test_GLUE2StorageShareCapacityTotalSize_MaxRange (self):
        message = ("INFO:\n"
                   "I092 Description: Total share capacity size greater than 1 million GB !\n"
                   "I092 Affected DN: %s\n"
                   "I092 Affected attribute: GLUE2StorageShareCapacityTotalSize\n"
                   "I092 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) <= 1000000, message )

    def test_GLUE2StorageShareCapacityFreeSize_OK (self):
        if 'GLUE2StorageShareCapacityTotalSize' in self.entry:
            message = ("ERROR:\n"
                       "E019 Description: Incoherent attribute range\n"
                       "E019 Affected DN: %s\n"
                       "E019 Affected attribute: "
                             " and GLUE2StorageShareCapacityTotalSize\n "
                       "E019 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2StorageShareCapacityTotalSize'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2StorageShareCapacityTotalSize'][0]), message )

    def test_GLUE2StorageShareCapacityUsedSize_OK (self):
        if 'GLUE2StorageShareCapacityTotalSize' in self.entry:
            message = ("ERROR:\n"
                       "E020 Description: Incoherent attribute range\n"
                       "E020 Affected DN: %s\n"
                       "E020 Affected attribute: GLUE2StorageShareCapacityUsedSize"
                             " and GLUE2StorageShareCapacityTotalSize\n "
                       "E020 Published value: %s and %s\n") % \
                       (self.dn, self.value[0], self.entry['GLUE2StorageShareCapacityTotalSize'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2StorageShareCapacityTotalSize'][0]), message )

#------------------------------------- GLUE2ToComputingService ---------------------------------------

    def test_GLUE2ToComputingServiceBandwidth_MinRange (self):
        message = ("INFO:\n"
                   "I093 Description: Bandwidth less than 100\n"
                   "I093 Affected DN: %s\n"
                   "I093 Affected attribute: GLUE2ToComputingServiceBandwidth\n"
                   "I093 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) >= 100 , message )

    def test_GLUE2ToComputingServiceBandwidth_MaxRange (self):
        message = ("INFO:\n"
                   "I094 Description: Bandwidth greater than 100000\n"
                   "I094 Affected DN: %s\n"
                   "I094 Affected attribute: GLUE2ToComputingServiceBandwidth\n"
                   "I094 Published value: %s\n") % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) <= 100000 , message )


