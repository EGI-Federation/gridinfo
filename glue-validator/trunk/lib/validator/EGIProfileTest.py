import re
import unittest
import datetime
import time
import validator.utils

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
            margin = datetime.timedelta(seconds=120)
            year = datetime.timedelta(days=730)
            if creationtime.timetuple() > (now + margin).timetuple():
                message = validator.utils.message_generator("ERROR","E001",self.dn,"GLUE2EntityCreationTime",self.value[0])
                status = False
            elif creationtime.timetuple() < (now - year).timetuple():
                message = validator.utils.message_generator("WARNING","W001",self.dn,"GLUE2EntityCreationTime",self.value[0])
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
            message = validator.utils.message_generator("WARNING","W002",self.dn,"GLUE2EntityValidity","NA")
        else:
            try:
                creationtime =  datetime.datetime\
                                (*(time.strptime(self.entry['GLUE2EntityCreationTime'][0],"%Y-%m-%dT%H:%M:%SZ")[0:6])) 
                now = datetime.datetime.utcnow()
                if ( self.value[0] == "60" ):
                    validity = datetime.timedelta(seconds=600)
                else:
                    validity = datetime.timedelta(seconds=int(self.value[0]))
                # ARC validity bug.
                due_time = (creationtime + validity).timetuple() 
                if due_time < now.timetuple():
                    message = validator.utils.message_generator\
                              ("ERROR","E002",self.dn,"GLUE2EntityValidity",self.value[0],\
                               "GLUE2EntityCreationTime is %s" % self.entry['GLUE2EntityCreationTime'][0] )
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
                        message = message + \
                                  validator.utils.message_generator("WARNING","W003",self.dn,\
                                  "GLUE2EntityOtherInfo: ProfileName",val)
                        status = False
                if att == 'ProfileVersion':
                    if not self.types.is_String(val):
                        message = message + \
                                  validator.utils.message_generator("WARNING","W004",self.dn,\
                                  "GLUE2EntityOtherInfo: ProfileVersion",val)
                        status = False
                elif att == 'GRID':
                    if not self.types.is_Grid_t(val):
                        message = message + \
                                  validator.utils.message_generator("INFO","I001",self.dn,\
                                  "GLUE2EntityOtherInfo: GRID",val)
                        status = False
                elif att == 'CONFIG':
                    if not self.types.is_Config_t(val):
                        message = message + \
                                  validator.utils.message_generator("INFO","I002",self.dn,\
                                  "GLUE2EntityOtherInfo: CONFIG",val)
                        status = False
                elif att == 'EGI_NGI':
                    if not self.types.is_EGIngi_t(val):
                        message = message + \
                                  validator.utils.message_generator("INFO","I003",self.dn,\
                                  "GLUE2EntityOtherInfo: EGI_NGI",val)
                        status = False
                elif att == 'BLOG':
                    if not self.types.is_URL(val):
                        message = message + \
                                  validator.utils.message_generator("INFO","I004",self.dn,\
                                  "GLUE2EntityOtherInfo: BLOG",val)
                        status = False
                elif att == 'ICON':
                    if not self.types.is_URL(val):
                        message = message + \
                                  validator.utils.message_generator("INFO","I005",self.dn,\
                                  "GLUE2EntityOtherInfo: ICON",val)
                        status = False
                elif att == 'WLCG_TIER':
                    if not self.types.is_Tier_t(val):
                        message = message + \
                                  validator.utils.message_generator("INFO","I006",self.dn,\
                                  "GLUE2EntityOtherInfo: WLCG_TIER",val)
                        status = False
                elif att == 'WLCG_NAME' or att == 'WLCG_PARENT':
                    if not self.types.is_WLCGname_t(val):
                        message = message + \
                                  validator.utils.message_generator("INFO","I007",self.dn,\
                                  "GLUE2EntityOtherInfo: WLCG_NAME",val)
                        status = False
                elif att == 'WLCG_NAMEICON':
                    if not self.types.is_URL(val):
                        message = message + \
                                  validator.utils.message_generator("INFO","I008",self.dn,\
                                  "GLUE2EntityOtherInfo: WLCG_NAMEICON",val)
                        status = False
                elif att == 'MiddlewareName':
                    if not self.types.is_Middleware_t(val):
                        message = message + \
                                  validator.utils.message_generator("INFO","I009",self.dn,\
                                  "GLUE2EntityOtherInfo: MiddlewareName",val)
                        status = False
                elif att == 'MiddlewareVersion':
                    if not self.types.is_String(val):
                        message = message + \
                                  validator.utils.message_generator("INFO","I010",self.dn,\
                                  "GLUE2EntityOtherInfo: MiddlewareVersion",val)
                        status = False
                elif att == 'HostDN':
                    if not self.types.is_DN_t(val):
                        message = message + \
                                  validator.utils.message_generator("INFO","I011",self.dn,\
                                  "GLUE2EntityOtherInfo: HostDN",val)
                        status = False
                elif att == 'Share':
                    index2 = val.find(":")
                    if (index2 > -1):
                        voname = val[:index2]
                        percentage = val[index2 +1:]
                        if not self.types.is_VO_t(voname):
                            message = message + \
                                      validator.utils.message_generator("INFO","I012",self.dn,\
                                      "GLUE2EntityOtherInfo: Share",voname)
                            status = False
                        elif voname not in sharedict:
                            if (int(percentage) < 0) or (int(percentage) > 100):
                                message = message + \
                                          validator.utils.message_generator("ERROR","E003",self.dn,\
                                          "GLUE2EntityOtherInfo: Share","%s:%s" % (voname,percentage))
                                status = False
                            sharedict[voname] = int(percentage)
                        else:
                            message = message + \
                                      validator.utils.message_generator("ERROR","E004",self.dn,\
                                      "GLUE2EntityOtherInfo: Share",voname)
                            status = False
                    else:
                        message = message + \
                                  validator.utils.message_generator("ERROR","E005",self.dn,\
                                  "GLUE2EntityOtherInfo: Share",val)
                        status = False
                elif att.startswith('CPUScalingReference'):
                    if not self.types.is_Benchmarkabbr_t(att.split('CPUScalingReference')[1]):
                        message = message + \
                                  validator.utils.message_generator("INFO","I013",self.dn,\
                                  "GLUE2EntityOtherInfo: CPUScalingReference",att.split('CPUScalingReference')[1])
                        status = False
        totalshare=0 
        for i in sharedict:
            totalshare = totalshare + sharedict[i]
        if ( totalshare > 100 ):
            message = message + \
                      validator.utils.message_generator("ERROR","E007",self.dn,"GLUE2EntityOtherInfo: Share",totalshare)
            status = False 
        self.assertTrue(status, message)
    
#------------------------------------- GLUE2Location --------------------------------------------

    def test_GLUE2LocationLongitude_OK (self):
        message = validator.utils.message_generator("ERROR","E008",self.dn,"GLUE2LocationLongitude",self.value[0])
        self.assertTrue( float(self.value[0]) > -180 and float(self.value[0]) < 180, message)     

    def test_GLUE2LocationLatitude_OK (self):
        message = validator.utils.message_generator("ERROR","E009",self.dn,"GLUE2LocationLatitude",self.value[0])
        self.assertTrue( float(self.value[0]) > -90 and float(self.value[0]) < 90, message)

#------------------------------------- GLUE2Service -----------------------------------------------

    def test_GLUE2ServiceID_OK (self):
        status = re.match('^_',self.value[0])
        message = validator.utils.message_generator("WARNING","W039",self.dn,"GLUE2ServiceID",self.value[0])
        self.assertFalse(status, message)

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
        job_stats = job_stats + " Difference is %s" % (total - int(self.value[0]))
        low = int(self.value[0]) - (int(self.value[0]) * 0.1)
        #low = low - 1
        high = int(self.value[0]) + (int(self.value[0]) * 0.1)
        #high = high + 1
        job_stats = job_stats + "; %s <= %s <= %s; Difference is %s" % (low, total, high, total - int(self.value[0]))
        message = validator.utils.message_generator("WARNING","W005",self.dn,"GLUE2ComputingServiceTotalJobs",\
                  self.value[0],job_stats )
        if not ( low <= total <= high ):
            value = False
        self.assertTrue( value , message )


    def test_GLUE2ComputingServiceRunningJobs_OK (self):
        message = validator.utils.message_generator("INFO","I014",self.dn,"GLUE2ComputingServiceRunningJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingServiceWaitingJobs_OK (self):
        message = validator.utils.message_generator("INFO","I015",self.dn,"GLUE2ComputingServiceWaitingJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingServiceStagingJobs_OK (self):
        message = validator.utils.message_generator("INFO","I016",self.dn,"GLUE2ComputingServiceStagingJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingServiceSuspendedJobs_OK (self):
        message = validator.utils.message_generator("INFO","I017",self.dn,"GLUE2ComputingServiceSuspendedJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingServicePreLRMSWaitingJobs_OK (self):
        message = validator.utils.message_generator("INFO","I018",self.dn,\
                  "GLUE2ComputingServicePreLRMSWaitingJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

#------------------------------------- GLUE2Endpoint ---------------------------------------

    def test_GLUE2EndpointID_OK (self):
        status = re.match('^_',self.value[0])
        message = validator.utils.message_generator("WARNING","W040",self.dn,"GLUE2EndpointID",self.value[0])
        self.assertFalse(status, message)

    def test_GLUE2EndpointImplementationVersion_OK (self):
        message = validator.utils.message_generator("WARNING","W041",self.dn,\
                  "GLUE2EndpointImplementationVersion",self.value[0])
        self.assertTrue( self.value[0].find("is not installed") == -1, message )
          
    def test_GLUE2EndpointStartTime_OK (self):
        try:
            creationtime = datetime.datetime(*(time.strptime(self.value[0],"%Y-%m-%dT%H:%M:%SZ")[0:6]))
            now = datetime.datetime.utcnow()
            margin = datetime.timedelta(seconds=120)
            twoyears = datetime.timedelta(days=730)
            if creationtime.timetuple() > (now + margin).timetuple():
                message = validator.utils.message_generator("ERROR","E010",self.dn,"GLUE2EndpointStartTime",self.value[0])
                status = False
            elif creationtime.timetuple() < (now - twoyears).timetuple():
                message = validator.utils.message_generator("WARNING","W006",self.dn,"GLUE2EndpointStartTime",self.value[0])
                status = False
            else:
                message = ""
                status = True
        except ValueError:
            message = "" 
            status = True
        self.assertTrue(status, message)

    def test_GLUE2EndpointIssuerCA_OK (self):
        message = validator.utils.message_generator("INFO","I019",self.dn,"GLUE2EndpointIssuerCA",self.value[0])
        self.assertTrue( self.value[0] != 'unknown', message )

    def test_GLUE2EndpointTrustedCA_OK (self):
        message = validator.utils.message_generator("INFO","I020",self.dn,"GLUE2EndpointTrustedCA",self.value[0])
        self.assertTrue( self.value[0] != 'unknown', message )

    def test_GLUE2EndpointDowntimeAnnounce_OK (self):
        try:
            creationtime = datetime.datetime(*(time.strptime(self.value[0],"%Y-%m-%dT%H:%M:%SZ")[0:6]))
            now = datetime.datetime.utcnow()
            margin = datetime.timedelta(seconds=120)
            year = datetime.timedelta(days=365)
            if creationtime.timetuple() > (now + margin).timetuple():
                message = validator.utils.message_generator("ERROR","E011",self.dn,\
                          "GLUE2EndpointDowntimeAnnounce",self.value[0])
                status = False
            elif creationtime.timetuple() < (now - year).timetuple():
                message = validator.utils.message_generator("WARNING","W007",self.dn,\
                          "GLUE2EndpointDowntimeAnnounce",self.value[0])
                status = False
            else:
                message = ""
                status = True
        except ValueError:
            message = ""
            status = True
        self.assertTrue(status, message)

    def test_GLUE2EndpointDowntimeAnnounce_checkStart (self):
       message = validator.utils.message_generator("WARNING","W008",self.dn,"GLUE2EndpointDowntimeAnnounce",self.value[0])
       self.assertTrue('GLUE2EndpointDowntimeStart' in self.entry, message)

    def test_GLUE2EndpointDowntimeStart_OK (self):
        try:
            status = True
            message = ""
            starttime = datetime.datetime(*(time.strptime(self.value[0],"%Y-%m-%dT%H:%M:%SZ")[0:6]))
            now = datetime.datetime.utcnow()
            year = datetime.timedelta(days=365)
            if 'GLUE2EndpointDowntimeEnd' in self.entry:
                endtime = datetime.datetime(*(time.strptime(self.entry['GLUE2EndpointDowntimeEnd'][0],\
                          "%Y-%m-%dT%H:%M:%SZ")[0:6]))
                if starttime > endtime:
                    message = validator.utils.message_generator("ERROR","E012",self.dn,"GLUE2EndpointDowntimeStart",\
                              self.value[0],"GLUE2EndpointDowntimeEnd is %s" % self.entry['GLUE2EndpointDowntimeEnd'][0])
                    status = False
            elif starttime.timetuple() > (now + year).timetuple():
                message = validator.utils.message_generator("WARNING","W009",self.dn,\
                          "GLUE2EndpointDowntimeStart",self.value[0])
                status = False
            elif starttime.timetuple() < (now - year).timetuple():
                message = validator.utils.message_generator("WARNING","W010",self.dn,\
                          "GLUE2EndpointDowntimeStart",self.value[0])
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
                message = validator.utils.message_generator("ERROR","E013",self.dn,"GLUE2EndpointDowntimeEnd",self.value[0])
                status = False
            elif endtime.timetuple() > (now + year).timetuple():
                message = validator.utils.message_generator("WARNING","W011",self.dn,\
                          "GLUE2EndpointDowntimeEnd",self.value[0])
                status = False
            elif endtime.timetuple() < (now - week).timetuple():
                message = validator.utils.message_generator("WARNING","W012",self.dn,\
                          "GLUE2EndpointDowntimeEnd",self.value[0])
                status = False
        except ValueError:
            message = ""
            status = True
        self.assertTrue(status, message)

#------------------------------------- GLUE2ComputingEndpoint ---------------------------------------

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
        job_stats = job_stats + " Difference is %s" % (total - int(self.value[0]))
        low = int(self.value[0]) - (int(self.value[0]) * 0.1)
        #low = low - 1
        high = int(self.value[0]) + (int(self.value[0]) * 0.1)
        #high = high + 1
        job_stats = job_stats + "; %s <= %s <= %s; Difference is %s" % (low, total, high, total - int(self.value[0]))
        message = validator.utils.message_generator("WARNING","W013",self.dn,"GLUE2ComputingEndpointTotalJobs",\
                  self.value[0],job_stats )
        if not ( low <= total <= high ):
            value = False
        self.assertTrue( value , message )

    def test_GLUE2ComputingEndpointRunningJobs_OK (self):
        message = validator.utils.message_generator("INFO","I021",self.dn,"GLUE2ComputingEndpointRunningJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingEndpointWaitingJobs_OK (self):
        message = validator.utils.message_generator("INFO","I022",self.dn,"GLUE2ComputingEndpointWaitingJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingEndpointStagingJobs_OK (self):
        message = validator.utils.message_generator("INFO","I023",self.dn,"GLUE2ComputingEndpointStagingJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingEndpointSuspendedJobs_OK (self):
        message = validator.utils.message_generator("INFO","I024",self.dn,\
                  "GLUE2ComputingEndpointSuspendedJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingEndpointPreLRMSWaitingJobs_OK (self):
        message = validator.utils.message_generator("INFO","I025",self.dn,\
                  "GLUE2ComputingEndpointPreLRMSWaitingJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

#------------------------------------- GLUE2ComputingShare ---------------------------------------

    def test_GLUE2ComputingShareMaxWallTime_OK (self):
        message = validator.utils.message_generator("INFO","I026",self.dn,"GLUE2ComputingShareMaxWallTime",self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMaxMultiSlotWallTime_OK (self):
        message = validator.utils.message_generator("INFO","I027",self.dn,\
                  "GLUE2ComputingShareMaxMultiSlotWallTime",self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareDefaultWallTime_OK (self):
        message = validator.utils.message_generator("INFO","I028",self.dn,"GLUE2ComputingShareDefaultWallTime",self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMinWallTime_OK (self):
        if 'GLUE2ComputingShareMaxWallTime' in self.entry:
            message = validator.utils.message_generator("WARNING","W014",self.dn,"GLUE2ComputingShareMinWallTime",\
                      self.value[0],"GLUE2ComputingShareMaxWallTime is %s" % self.entry['GLUE2ComputingShareMaxWallTime'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxWallTime'][0]), message )

    def test_GLUE2ComputingShareDefaultWallTime_MaxRange (self):
        if 'GLUE2ComputingShareMaxWallTime' in self.entry:
            message = validator.utils.message_generator("WARNING","W015",self.dn,"GLUE2ComputingShareDefaultWallTime",\
                      self.value[0],"GLUE2ComputingShareMaxWallTime is %s" % self.entry['GLUE2ComputingShareMaxWallTime'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxWallTime'][0]), message )  
            
    def test_GLUE2ComputingShareDefaultWallTime_MinRange (self):
        if 'GLUE2ComputingShareMinWallTime' in self.entry:
            message = validator.utils.message_generator("WARNING","W016",self.dn,"GLUE2ComputingShareDefaultWallTime",\
                      self.value[0],"GLUE2ComputingShareMinWallTime is %s" % self.entry['GLUE2ComputingShareMinWallTime'][0])
            self.assertTrue ( int(self.value[0]) >= int(self.entry['GLUE2ComputingShareMinWallTime'][0]), message )

    def test_GLUE2ComputingShareMaxCPUTime_OK (self):
        message = validator.utils.message_generator("INFO","I029",self.dn,"GLUE2ComputingShareMaxCPUTime",self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMaxTotalCPUTime_OK (self):
        message = validator.utils.message_generator("INFO","I030",self.dn,"GLUE2ComputingShareMaxTotalCPUTime",self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareDefaultCPUTime_OK (self):
        message = validator.utils.message_generator("INFO","I031",self.dn,"GLUE2ComputingShareDefaultCPUTime",self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMinCPUTime_OK (self):
        if 'GLUE2ComputingShareMaxCPUTime' in self.entry:
            message = validator.utils.message_generator("WARNING","W017",self.dn,"GLUE2ComputingShareMinCPUTime",\
                      self.value[0],"GLUE2ComputingShareMaxCPUTime is %s" % self.entry['GLUE2ComputingShareMaxCPUTime'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxCPUTime'][0]), message )

    def test_GLUE2ComputingShareDefaultCPUTime_MaxRange (self):
        if 'GLUE2ComputingShareMaxCPUTime' in self.entry:
            message = validator.utils.message_generator("WARNING","W018",self.dn,"GLUE2ComputingShareDefaultCPUTime",\
                      self.value[0],"GLUE2ComputingShareMaxCPUTime is %s" % self.entry['GLUE2ComputingShareMaxCPUTime'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxCPUTime'][0]), message )

    def test_GLUE2ComputingShareDefaultCPUTime_MinRange (self):
        if 'GLUE2ComputingShareMinCPUTime' in self.entry:
            message = validator.utils.message_generator("WARNING","W019",self.dn,"GLUE2ComputingShareDefaultCPUTime",\
                      self.value[0],"GLUE2ComputingShareMinCPUTime is %s" % self.entry['GLUE2ComputingShareMinCPUTime'][0])
            self.assertTrue ( int(self.value[0]) >= int(self.entry['GLUE2ComputingShareMinCPUTime'][0]), message )

    def test_GLUE2ComputingShareMaxTotalJobs_default (self):
        message = validator.utils.message_generator("INFO","I032",self.dn,"GLUE2ComputingShareMaxTotalJobs",self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMaxTotalJobs_zero (self):
        message = validator.utils.message_generator("WARNING","W020",self.dn,"GLUE2ComputingShareMaxTotalJobs",self.value[0])
        self.assertTrue ( int(self.value[0]) != 0, message )

    def test_GLUE2ComputingShareMaxTotalJobs_MaxRunningJobs (self):
        if 'GLUE2ComputingShareMaxRunningJobs' in self.entry:
            message = validator.utils.message_generator("WARNING","W021",self.dn,"GLUE2ComputingShareMaxTotalJobs",\
                      self.value[0],"GLUE2ComputingShareMaxRunningJobs is %s" % \
                      self.entry['GLUE2ComputingShareMaxRunningJobs'][0])
            self.assertTrue ( int(self.value[0]) >= int(self.entry['GLUE2ComputingShareMaxRunningJobs'][0]), message )

    def test_GLUE2ComputingShareMaxTotalJobs_MaxWaitingJobs (self):
        if 'GLUE2ComputingShareMaxWaitingJobs' in self.entry:
            message = validator.utils.message_generator("WARNING","W021",self.dn,"GLUE2ComputingShareMaxTotalJobs",\
                      self.value[0],"GLUE2ComputingShareMaxWaitingJobs is %s" % \
                      self.entry['GLUE2ComputingShareMaxWaitingJobs'][0])
            self.assertTrue ( int(self.value[0]) >= int(self.entry['GLUE2ComputingShareMaxWaitingJobs'][0]), message )

    def test_GLUE2ComputingShareMaxUserRunningJobs_zero (self):
        message = validator.utils.message_generator("WARNING","W022",self.dn,"GLUE2ComputingShareMaxUserRunningJobs",\
                  self.value[0])
        self.assertTrue ( int(self.value[0]) != 0, message )

    def test_GLUE2ComputingShareMaxUserRunningJobs_OK (self):
        if 'GLUE2ComputingShareMaxRunningJobs' in self.entry:
           message = validator.utils.message_generator("WARNING","W023",self.dn,"GLUE2ComputingShareMaxUserRunningJobs",\
                     self.value[0],"GLUE2ComputingShareMaxRunningJobs is %s" % \
                     self.entry['GLUE2ComputingShareMaxRunningJobs'][0])
           self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxRunningJobs'][0]), message )

    def test_GLUE2ComputingShareMaxRunningJobs_OK (self):
        message = validator.utils.message_generator("INFO","I033",self.dn,"GLUE2ComputingShareMaxRunningJobs",self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMaxWaitingJobs_OK (self):
        message = validator.utils.message_generator("INFO","I034",self.dn,"GLUE2ComputingShareMaxWaitingJobs",self.value[0])
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMaxSlotsPerJob_zero (self):
        message = validator.utils.message_generator("WARNING","W024",self.dn,\
                  "GLUE2ComputingShareMaxSlotsPerJob",self.value[0])
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
        job_stats = job_stats + " Difference is %s" % (total - int(self.value[0]))
        low = int(self.value[0]) - (int(self.value[0]) * 0.1)
        #low = low - 1
        high = int(self.value[0]) + (int(self.value[0]) * 0.1)
        #high = high + 1
        job_stats = job_stats + "; %s <= %s <= %s; Difference is %s" % (low, total, high, total - int(self.value[0]))
        message = validator.utils.message_generator("WARNING","W025",self.dn,"GLUE2ComputingShareTotalJobs",\
                  self.value[0],job_stats)
        if not ( low <= total <= high ):
            value = False
        self.assertTrue( value , message )

    def test_GLUE2ComputingShareRunningJobs_OK (self):
        message = validator.utils.message_generator("INFO","I035",self.dn,"GLUE2ComputingShareRunningJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareLocalRunningJobs_OK (self):
        message = validator.utils.message_generator("INFO","I036",self.dn,\
                  "GLUE2ComputingShareLocalRunningJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareWaitingJobs_OK (self):
        message = validator.utils.message_generator("INFO","I037",self.dn,"GLUE2ComputingShareWaitingJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareWaitingJobs_default (self):
        message = validator.utils.message_generator("ERROR","E022",self.dn,"GLUE2ComputingShareWaitingJobs",self.value[0])
        self.assertTrue( int(self.value[0]) != 444444, message )

    def test_GLUE2ComputingShareLocalWaitingJobs_OK (self):
        message = validator.utils.message_generator("INFO","I038",self.dn,\
                  "GLUE2ComputingShareLocalWaitingJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareSuspendedJobs_OK (self):
        message = validator.utils.message_generator("INFO","I039",self.dn,"GLUE2ComputingShareSuspendedJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareLocalSuspendedJobs_OK (self):
        message = validator.utils.message_generator("INFO","I040",self.dn,\
                  "GLUE2ComputingShareLocalSuspendedJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareStagingJobs_OK (self):
        message = validator.utils.message_generator("INFO","I041",self.dn,"GLUE2ComputingShareStagingJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingSharePreLRMSWaitingJobs_OK (self):
        message = validator.utils.message_generator("INFO","I042",self.dn,\
                  "GLUE2ComputingSharePreLRMSWaitingJobs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareMaxMainMemory_MinRange (self):
        message = validator.utils.message_generator("WARNING","W026",self.dn,\
                  "GLUE2ComputingShareMaxMainMemory",self.value[0])
        self.assertTrue( int(self.value[0]) >= 100, message )
   
    def test_GLUE2ComputingShareMaxMainMemory_MaxRange (self):
        message = validator.utils.message_generator("INFO","I043",self.dn,"GLUE2ComputingShareMaxMainMemory",self.value[0])
        self.assertTrue( int(self.value[0]) < 100000, message )

    def test_GLUE2ComputingShareMaxMainMemory_Default (self):
        message = validator.utils.message_generator("INFO","I096",self.dn,"GLUE2ComputingShareMaxMainMemory",self.value[0])
        self.assertTrue( int(self.value[0]) != 444444, message )

    def test_GLUE2ComputingShareGuaranteedMainMemory_MinRange (self):
        if 'GLUE2ComputingShareMaxMainMemory' in self.entry:
            message = validator.utils.message_generator("WARNING","W027",self.dn,"GLUE2ComputingShareGuaranteedMainMemory",\
                      self.value[0],"GLUE2ComputingShareMaxMainMemory is %s" % \
                      self.entry['GLUE2ComputingShareMaxMainMemory'][0])
            self.assertTrue( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxMainMemory'][0]), message )

    def test_GLUE2ComputingShareGuaranteedMainMemory_MaxRange (self):
        message = validator.utils.message_generator("INFO","I044",self.dn,\
                  "GLUE2ComputingShareGuaranteedMainMemory",self.value[0])
        self.assertTrue( int(self.value[0]) < 100000, message )

    def test_GLUE2ComputingShareMaxVirtualMemory_MinRange (self):
        if 'GLUE2ComputingShareMaxMainMemory' in self.entry:
            message = validator.utils.message_generator("WARNING","W028",self.dn,"GLUE2ComputingShareMaxVirtualMemory",\
                      self.value[0],"GLUE2ComputingShareMaxMainMemory is %s" % 
                      self.entry['GLUE2ComputingShareMaxMainMemory'][0])
            self.assertTrue( int(self.value[0]) >= int(self.entry['GLUE2ComputingShareMaxMainMemory'][0]), message )

    def test_GLUE2ComputingShareMaxVirtualMemory_MaxRange (self):
        message = validator.utils.message_generator("INFO","I045",self.dn,\
                  "GLUE2ComputingShareMaxVirtualMemory",self.value[0])
        self.assertTrue( int(self.value[0]) < 100000, message )

    def test_GLUE2ComputingShareMaxVirtualMemory_Default (self):
        message = validator.utils.message_generator("INFO","I097",self.dn,"GLUE2ComputingShareMaxVirtualMemory",\
                  self.value[0])
        self.assertTrue( int(self.value[0]) != 444444, message )

    def test_GLUE2ComputingShareGuaranteedVirtualMemory_MinRange (self):
        if 'GLUE2ComputingShareMaxVirtualMemory' in self.entry:
            message = validator.utils.message_generator("WARNING","W029",self.dn,\
                      "GLUE2ComputingShareGuaranteedVirtualMemory",self.value[0],\
                      "GLUE2ComputingShareMaxVirtualMemory is %s" % \
                      self.entry['GLUE2ComputingShareMaxVirtualMemory'][0])
            self.assertTrue( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxVirtualMemory'][0]), message )

    def test_GLUE2ComputingShareGuaranteedVirtualMemory_MaxRange (self):
        message = validator.utils.message_generator("INFO","I046",self.dn,\
                  "GLUE2ComputingShareGuaranteedVirtualMemory",self.value[0])
        self.assertTrue( int(self.value[0]) < 100000, message )

    def test_GLUE2ComputingShareEstimatedAverageWaitingTime_OK (self):
        message = validator.utils.message_generator("INFO","I046",self.dn,\
                  "GLUE2ComputingShareEstimatedAverageWaitingTime",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareEstimatedAverageWaitingTime_default (self):
        message = validator.utils.message_generator("ERROR","E023",self.dn,\
                  "GLUE2ComputingShareEstimatedAverageWaitingTime",self.value[0])
        self.assertTrue( int(self.value[0]) != 2146660842, message )

    def test_GLUE2ComputingShareEstimatedWorstWaitingTime_OK (self):
        message = validator.utils.message_generator("INFO","I047",self.dn,\
                  "GLUE2ComputingShareEstimatedWorstWaitingTime",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareEstimatedWorstWaitingTime_default (self):
        message = validator.utils.message_generator("ERROR","E024",self.dn,\
                  "GLUE2ComputingShareEstimatedWorstWaitingTime",self.value[0])
        self.assertTrue( int(self.value[0]) != 2146660842, message )

    def test_GLUE2ComputingShareFreeSlots_OK (self):
        message = validator.utils.message_generator("INFO","I048",self.dn,"GLUE2ComputingShareFreeSlots",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareUsedSlots_OK (self):
        message = validator.utils.message_generator("INFO","I049",self.dn,"GLUE2ComputingShareUsedSlots",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareRequestedSlots_OK (self):
        message = validator.utils.message_generator("INFO","I050",self.dn,"GLUE2ComputingShareRequestedSlots",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

#------------------------------------- GLUE2ComputingManager ---------------------------------------

    def test_GLUE2ComputingManagerTotalLogicalCPUs_MinRange (self):
        message = validator.utils.message_generator("INFO","I051",self.dn,\
                  "GLUE2ComputingManagerTotalLogicalCPUs",self.value[0])
        self.assertTrue( int(self.value[0]) >= 10, message )

    def test_GLUE2ComputingManagerTotalLogicalCPUs_MaxRange (self):
        message = validator.utils.message_generator("INFO","I052",self.dn,\
                  "GLUE2ComputingManagerTotalLogicalCPUs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )
        
    def test_GLUE2ComputingManagerTotalPhysicalCPUs_OK (self):
        if 'GLUE2ComputingManagerTotalLogicalCPUs' in self.entry:
            message = validator.utils.message_generator("WARNING","W030",self.dn,"GLUE2ComputingManagerTotalPhysicalCPUs",\
                      self.value[0],"GLUE2ComputingManagerTotalLogicalCPUs is %s" % \
                      self.entry['GLUE2ComputingManagerTotalLogicalCPUs'][0])
            self.assertTrue( int(self.value[0]) <= int(self.entry['GLUE2ComputingManagerTotalLogicalCPUs'][0]) , message) 

    def test_GLUE2ComputingManagerTotalPhysicalCPUs_MinRange (self):
        message = validator.utils.message_generator("INFO","I053",self.dn,\
                  "GLUE2ComputingManagerTotalPhysicalCPUs",self.value[0])
        self.assertTrue( int(self.value[0]) >= 10, message )

    def test_GLUE2ComputingManagerTotalPhysicalCPUs_MaxRange (self):
        message = validator.utils.message_generator("INFO","I054",self.dn,\
                  "GLUE2ComputingManagerTotalPhysicalCPUs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerTotalSlots_OK (self):
        if 'GLUE2ComputingManagerTotalLogicalCPUs' in self.entry:
            message = validator.utils.message_generator("WARNING","W031",self.dn,"GLUE2ComputingManagerTotalSlots",\
                      self.value[0],"GLUE2ComputingManagerTotalLogicalCPUs is %s" %\
                      self.entry['GLUE2ComputingManagerTotalLogicalCPUs'][0])
            self.assertTrue( int(self.value[0]) <= int(self.entry['GLUE2ComputingManagerTotalLogicalCPUs'][0])*2 , message)

    def test_GLUE2ComputingManagerTotalSlots_MinRange (self):
        message = validator.utils.message_generator("INFO","I055",self.dn,"GLUE2ComputingManagerTotalSlots",self.value[0])
        self.assertTrue( int(self.value[0]) >= 10, message )

    def test_GLUE2ComputingManagerTotalSlots_MaxRange (self):
        message = validator.utils.message_generator("INFO","I056",self.dn,"GLUE2ComputingManagerTotalSlots",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerSlotsUsedByLocalJobs_OK (self):
        if 'GLUE2ComputingManagerTotalSlots' in self.entry:
            message = validator.utils.message_generator("WARNING","W032",self.dn,\
                      "GLUE2ComputingManagerSlotsUsedByLocalJobs",\
                      self.value[0],"GLUE2ComputingManagerTotalSlots is %s" % \
                      self.entry['GLUE2ComputingManagerTotalSlots'][0])
            self.assertTrue( int(self.value[0]) < int(self.entry['GLUE2ComputingManagerTotalSlots'][0]), message )

    def test_GLUE2ComputingManagerSlotsUsedByGridJobs_OK (self):
        if 'GLUE2ComputingManagerTotalSlots' in self.entry:
            message = validator.utils.message_generator("WARNING","W033",self.dn,"GLUE2ComputingManagerSlotsUsedByGridJobs",\
                      self.value[0],"GLUE2ComputingManagerTotalSlots is %s" %\
                      self.entry['GLUE2ComputingManagerTotalSlots'][0])
            self.assertTrue( int(self.value[0]) < int(self.entry['GLUE2ComputingManagerTotalSlots'][0]), message )

    def test_GLUE2ComputingManagerWorkingAreaTotal_OK (self):
        message = validator.utils.message_generator("INFO","I057",self.dn,\
                  "GLUE2ComputingManagerWorkingAreaTotal",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerWorkingAreaFree_OK (self):
        message = validator.utils.message_generator("INFO","I058",self.dn,\
                  "GLUE2ComputingManagerWorkingAreaFree",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerWorkingAreaMultiSlotTotal_OK (self):
        message = validator.utils.message_generator("INFO","I059",self.dn,\
                  "GLUE2ComputingManagerWorkingAreaMultiSlotTotal",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerWorkingAreaMultiSlotFree_OK (self):
        message = validator.utils.message_generator("INFO","I060",self.dn,\
                  "GLUE2ComputingManagerWorkingAreaMultiSlotFree",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerCacheTotal_OK (self):
        message = validator.utils.message_generator("INFO","I061",self.dn,"GLUE2ComputingManagerCacheTotal",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerCacheFree_OK (self):
        message = validator.utils.message_generator("INFO","I062",self.dn,"GLUE2ComputingManagerCacheTotal",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

#------------------------------------- GLUE2ExecutionEnvironment ---------------------------------------

    # Until info providers fix types, the general type checking is in "Known Issues" 
    # OS and Platform types that depend on sys admin are explicitely executed
    def test_GLUE2ExecutionEnvironmentPlatform_OK (self):
        status = self.types.is_Platform_t(self.value[0])
        message = validator.utils.message_generator\
                 ("WARNING","W042",self.dn,"GLUE2ExecutionEnvironmentPlatform",self.value[0],\
                  "Expected type is Platform_t")
        self.assertTrue(status, message)

    def test_GLUE2ExecutionEnvironmentOSFamily_OK (self):
        status = self.types.is_OSFamily_t(self.value[0])
        message = validator.utils.message_generator\
                 ("WARNING","W043",self.dn,"GLUE2ExecutionEnvironmentOSFamily",self.value[0],\
                  "Expected type is OSFamily_t")
        self.assertTrue(status, message)

    def test_GLUE2ExecutionEnvironmentOSName_OK (self):
        status = self.types.is_OSName_t(self.value[0])
        message = validator.utils.message_generator\
                 ("WARNING","W044",self.dn,"GLUE2ExecutionEnvironmentOSName",self.value[0],\
                  "Expected type is OSName_t")
        self.assertTrue(status, message)

    def test_GLUE2ExecutionEnvironmentTotalInstances_MinRange (self):
        message = validator.utils.message_generator("INFO","I063",self.dn,\
                  "GLUE2ExecutionEnvironmentTotalInstances",self.value[0])
        self.assertTrue( int(self.value[0]) >= 10, message )

    def test_GLUE2ExecutionEnvironmentTotalInstances_MaxRange (self):
        message = validator.utils.message_generator("INFO","I064",self.dn,\
                  "GLUE2ExecutionEnvironmentTotalInstances",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ExecutionEnvironmentUsedInstances_OK (self):
        if 'GLUE2ExecutionEnvironmentTotalInstances' in self.entry:
            message = validator.utils.message_generator("INFO","I065",self.dn,"GLUE2ExecutionEnvironmentUsedInstances",\
                      self.value[0],"GLUE2ExecutionEnvironmentTotalInstances is %s" % \
                      self.entry['GLUE2ExecutionEnvironmentTotalInstances'][0])
            self.assertTrue( int(self.value[0]) < int(self.entry['GLUE2ExecutionEnvironmentTotalInstances'][0]), message )

    def test_GLUE2ExecutionEnvironmentUnavailableInstances_OK (self):
        if 'GLUE2ExecutionEnvironmentTotalInstances' in self.entry:
            message = validator.utils.message_generator("INFO","I066",self.dn,\
                      "GLUE2ExecutionEnvironmentUnavailableInstances",\
                      self.value[0],"GLUE2ExecutionEnvironmentTotalInstances is %s" % \
                      self.entry['GLUE2ExecutionEnvironmentTotalInstances'][0])
            self.assertTrue( int(self.value[0]) < int(self.entry['GLUE2ExecutionEnvironmentTotalInstances'][0]), message )

    def test_GLUE2ExecutionEnvironmentPhysicalCPUs_MaxRange (self):
        message = validator.utils.message_generator("INFO","I067",self.dn,\
                  "GLUE2ExecutionEnvironmentPhysicalCPUs",self.value[0])
        self.assertTrue( int(self.value[0]) <= 10, message )

    def test_GLUE2ExecutionEnvironmentLogicalCPUs_MaxRange (self):
        message = validator.utils.message_generator("INFO","I068",self.dn,\
                  "GLUE2ExecutionEnvironmentLogicalCPUs",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000, message )

    def test_GLUE2ExecutionEnvironmentCPUClockSpeed_MaxRange (self):
        message = validator.utils.message_generator("INFO","I069",self.dn,\
                  "GLUE2ExecutionEnvironmentCPUClockSpeed",self.value[0])
        self.assertTrue( int(self.value[0]) <= 10000, message )

    def test_GLUE2ExecutionEnvironmentCPUClockSpeed_MinRange (self):
        message = validator.utils.message_generator("INFO","I070",self.dn,\
                  "GLUE2ExecutionEnvironmentCPUClockSpeed",self.value[0])
        self.assertTrue( int(self.value[0]) >= 100, message )

    def test_GLUE2ExecutionEnvironmentCPUTimeScalingFactor_MaxRange (self):
        message = validator.utils.message_generator("INFO","I071",self.dn,\
                  "GLUE2ExecutionEnvironmentCPUTimeScalingFactor",self.value[0])
        self.assertTrue( int(self.value[0]) <= 1, message )

    def test_GLUE2ExecutionEnvironmentCPUTimeScalingFactor_MinRange (self):
        message = validator.utils.message_generator("INFO","I072",self.dn,\
                  "GLUE2ExecutionEnvironmentCPUTimeScalingFactor",self.value[0])
        self.assertTrue( float(self.value[0]) > 0.1, message )

    def test_GLUE2ExecutionEnvironmentWallTimeScalingFactor_MaxRange (self):
        message = validator.utils.message_generator("INFO","I073",self.dn,\
                  "GLUE2ExecutionEnvironmentWallTimeScalingFactor",self.value[0])
        self.assertTrue( int(self.value[0]) <= 1, message )

    def test_GLUE2ExecutionEnvironmentWallTimeScalingFactor_MinRange (self):
        message = validator.utils.message_generator("INFO","I074",self.dn,\
                  "GLUE2ExecutionEnvironmentWallTimeScalingFactor",self.value[0])
        self.assertTrue( float(self.value[0]) > 0.1, message )

    def test_GLUE2ExecutionEnvironmentMainMemorySize_MaxRange (self):
        message = validator.utils.message_generator("INFO","I075",self.dn,\
                  "GLUE2ExecutionEnvironmentMainMemorySize",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ExecutionEnvironmentMainMemorySize_MinRange (self):
        message = validator.utils.message_generator("INFO","I076",self.dn,\
                  "GLUE2ExecutionEnvironmentMainMemorySize",self.value[0])
        self.assertTrue( int(self.value[0]) >= 100, message )

    def test_GLUE2ExecutionEnvironmentVirtualMemorySize_MaxRange (self):
        message = validator.utils.message_generator("INFO","I077",self.dn,\
                  "GLUE2ExecutionEnvironmentVirtualMemorySize",self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ExecutionEnvironmentVirtualMemorySize_MinRange (self):
        message = validator.utils.message_generator("INFO","I078",self.dn,\
                  "GLUE2ExecutionEnvironmentVirtualMemorySize",self.value[0])
        self.assertTrue( int(self.value[0]) >= 100, message )

#------------------------------------- GLUE2ApplicationEnvironment ---------------------------------------

    def test_GLUE2ApplicationEnvironmentRemovalDate_OK (self):
        try:
           removaldate = datetime.datetime(*(time.strptime(self.value[0],"%Y-%m-%dT%H:%M:%SZ")[0:6]))
           now = datetime.datetime.utcnow()
           message = validator.utils.message_generator("INFO","I079",self.dn,\
                     "GLUE2ApplicationEnvironmentRemovalDate",self.value[0])
        except ValueError:
            message = ""
            status = True
        self.asserTrue ( removaldate.timetuple() < now.timetuple() , message )

    def test_GLUE2ApplicationEnvironmentMaxSlots_OK (self):
        message = validator.utils.message_generator("INFO","I080",self.dn,\
                  "GLUE2ApplicationEnvironmentMaxSlots",self.value[0])
        self.assertTrue ( int(self.value[0]) != 0, message )

    def test_GLUE2ApplicationEnvironmentMaxJobs_OK (self):
        message = validator.utils.message_generator("INFO","I081",self.dn,\
                  "GLUE2ApplicationEnvironmentMaxJobs",self.value[0])
        self.assertTrue ( int(self.value[0]) != 0, message )
 
    def test_GLUE2ApplicationEnvironmentMaxUserSeats_OK (self):
        message = validator.utils.message_generator("INFO","I082",self.dn,\
                  "GLUE2ApplicationEnvironmentMaxUserSeats",self.value[0])
        self.assertTrue ( int(self.value[0]) != 0, message )

    def test_GLUE2ApplicationEnvironmentFreeSlots_OK (self):
        if 'GLUE2ApplicationEnvironmentMaxSlots' in self.entry:
            message = validator.utils.message_generator("INFO","I083",self.dn,"GLUE2ApplicationEnvironmentFreeSlots",\
                      self.value[0],"GLUE2ApplicationEnvironmentMaxSlots is %s" %\
                      self.entry['GLUE2ApplicationEnvironmentMaxSlots'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ApplicationEnvironmentMaxSlots'][0]), message )

    def test_GLUE2ApplicationEnvironmentFreeJobs_OK (self):
        if 'GLUE2ApplicationEnvironmentMaxJobs' in self.entry:
            message = validator.utils.message_generator("INFO","I084",self.dn,"GLUE2ApplicationEnvironmentFreeJobs",\
                      self.value[0],"GLUE2ApplicationEnvironmentMaxJobs is %s" %\
                      self.entry['GLUE2ApplicationEnvironmentMaxJobs'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ApplicationEnvironmentMaxJobs'][0]), message )

    def test_GLUE2ApplicationEnvironmentFreeUserSeats_OK (self):
        if 'GLUE2ApplicationEnvironmentMaxUserSeats' in self.entry:
            message = validator.utils.message_generator("INFO","I085",self.dn,"GLUE2ApplicationEnvironmentFreeUserSeats",\
                      self.value[0],"GLUE2ApplicationEnvironmentMaxUserSeats is %s" %\
                      self.entry['GLUE2ApplicationEnvironmentMaxUserSeats'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ApplicationEnvironmentMaxUserSeats'][0]), message )

#------------------------------------- GLUE2StorageServiceCapacity ---------------------------------------

    def test_GLUE2StorageServiceCapacityTotalSize_OK (self):
        total = 0
        cap_stats = ""
        value = True
        for cap in ['GLUE2StorageServiceCapacityFreeSize',
                    'GLUE2StorageServiceCapacityUsedSize',
                    'GLUE2StorageServiceCapacityReservedSize']:
            if cap in self.entry:
                total = total + int(self.entry[cap][0])
                cap_stats = cap_stats + " %s=%s" % (cap,self.entry[cap][0])
            else:
                cap_stats = cap_stats + " %s=Not published" % (cap)
        low = int(self.value[0]) - (int(self.value[0]) * 0.005)
        low = low - 1
        high = int(self.value[0]) + (int(self.value[0]) * 0.005)
        high = high + 1
        cap_stats = cap_stats + " %s <= %s <= %s; Difference is %s" % (low, total, high, total - int(self.value[0]))
        message = validator.utils.message_generator("ERROR","E014",self.dn,\
                  "GLUE2StorageServiceCapacityTotalSize",self.value[0],cap_stats)
        if not ( low <= total <= high ):
            value = False
        self.assertTrue( value , message )

    def test_GLUE2StorageServiceCapacityTotalSize_MinRange (self):
        if 'GLUE2StorageServiceCapacityType' in self.entry:
            if self.entry['GLUE2StorageServiceCapacityType'][0] == 'online' or \
               self.entry['GLUE2StorageServiceCapacityType'][0] == 'nearline':
                   message = validator.utils.message_generator("INFO","I086",self.dn,\
                             "GLUE2StorageServiceCapacityTotalSize",self.value[0])
                   self.assertTrue ( int(self.value[0]) >= 1000 , message ) 

    def test_GLUE2StorageServiceCapacityTotalSize_MaxRange (self):
        if 'GLUE2StorageServiceCapacityType' in self.entry:
            if self.entry['GLUE2StorageServiceCapacityType'][0] == 'online' or \
               self.entry['GLUE2StorageServiceCapacityType'][0] == 'nearline':
                   message = validator.utils.message_generator("INFO","I087",self.dn,\
                             "GLUE2StorageServiceCapacityTotalSize",self.value[0])
                   self.assertTrue ( int(self.value[0]) <= 1000000000 , message )

    def test_GLUE2StorageServiceCapacityFreeSize_OK (self):
        if 'GLUE2StorageServiceCapacityTotalSize' in self.entry:
            message = validator.utils.message_generator("ERROR","E015",self.dn,"GLUE2StorageServiceCapacityFreeSize",\
                      self.value[0],"GLUE2StorageServiceCapacityTotalSize is %s" %\
                      self.entry['GLUE2StorageServiceCapacityTotalSize'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2StorageServiceCapacityTotalSize'][0]), message )

    def test_GLUE2StorageServiceCapacityUsedSize_OK (self):
        if 'GLUE2StorageServiceCapacityTotalSize' in self.entry:
            message = validator.utils.message_generator("ERROR","E016",self.dn,"GLUE2StorageServiceCapacityUsedSize",\
                      self.value[0],"GLUE2StorageServiceCapacityTotalSize is %s" %\
                      self.entry['GLUE2StorageServiceCapacityTotalSize'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2StorageServiceCapacityTotalSize'][0]), message )

    def test_GLUE2StorageServiceCapacityReservedSize_OK (self):
        if 'GLUE2StorageServiceCapacityTotalSize' in self.entry:
            message = validator.utils.message_generator("ERROR","E017",self.dn,"GLUE2StorageServiceCapacityReservedSize",\
                      self.value[0],"GLUE2StorageServiceCapacityTotalSize is %s" %\
                      self.entry['GLUE2StorageServiceCapacityTotalSize'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2StorageServiceCapacityTotalSize'][0]), message )

#------------------------------------- GLUE2StorageShare ---------------------------------------

    def test_GLUE2StorageShareAccessLatency_OK (self):
        message = validator.utils.message_generator("INFO","I088",self.dn,"GLUE2StorageShareAccessLatency",self.value[0])
        self.assertTrue ( self.value[0] != 'offline', message )

    def test_GLUE2StorageShareDefaultLifeTime_OK (self):
        message = validator.utils.message_generator("INFO","I089",self.dn,"GLUE2StorageShareDefaultLifeTime",self.value[0])
        self.assertTrue ( int(self.value[0]) >= 100000 , message )

    def test_GLUE2StorageShareMaximumLifeTime_OK (self):
        message = validator.utils.message_generator("INFO","I090",self.dn,"GLUE2StorageShareMaximumLifeTime",self.value[0])
        self.assertTrue ( int(self.value[0]) >= 100000 , message )

#------------------------------------- GLUE2StorageShareCapacity ---------------------------------------

    def test_GLUE2StorageShareCapacityTotalSize_OK (self):
        total = 0
        share_stats = ""
        value = True
        for share in ['GLUE2StorageShareCapacityFreeSize',\
                      'GLUE2StorageShareCapacityUsedSize',\
                      'GLUE2StorageShareCapacityReservedSize']:
            if share in self.entry:
                if (share == 'GLUE2StorageShareCapacityReservedSize') and \
                   (self.entry['GLUE2StorageShareCapacityReservedSize'][0] == self.value[0]):
                       share_stats = share_stats + " %s=%s (Not added)" % (share,self.entry[share][0])
                else:
                       total = total + int(self.entry[share][0])
                       share_stats = share_stats + " %s=%s" % (share,self.entry[share][0])
            else:
                share_stats = share_stats + " %s=Not published" % (share)
        low = int(self.value[0]) - (int(self.value[0]) * 0.005)
        low = low - 1
        high = int(self.value[0]) + (int(self.value[0]) * 0.005)
        high = high + 1
        share_stats = share_stats + "; %s <= %s <= %s; Difference is %s" % (low, total, high, total - int(self.value[0]))
        message = validator.utils.message_generator("ERROR","E018",self.dn,\
                  "GLUE2StorageShareCapacityTotalSize",self.value[0],share_stats)
        if not ( low <= total <= high ):
            value = False
        self.assertTrue( value , message )

    def test_GLUE2StorageShareCapacityTotalSize_MinRange (self):
        message = validator.utils.message_generator("INFO","I091",self.dn,"GLUE2StorageShareCapacityTotalSize",self.value[0])
        self.assertTrue ( int(self.value[0]) >= 1000, message )

    def test_GLUE2StorageShareCapacityTotalSize_MaxRange (self):
        message = validator.utils.message_generator("INFO","I092",self.dn,"GLUE2StorageShareCapacityTotalSize",self.value[0])
        self.assertTrue ( int(self.value[0]) <= 1000000000, message )

    def test_GLUE2StorageShareCapacityFreeSize_OK (self):
        if 'GLUE2StorageShareCapacityTotalSize' in self.entry:
            message = validator.utils.message_generator("ERROR","E019",self.dn,"GLUE2StorageShareCapacityFreeSize",\
                      self.value[0],"GLUE2StorageShareCapacityTotalSize is %s" %\
                      self.entry['GLUE2StorageShareCapacityTotalSize'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2StorageShareCapacityTotalSize'][0]), message )

    def test_GLUE2StorageShareCapacityUsedSize_OK (self):
        if 'GLUE2StorageShareCapacityTotalSize' in self.entry:
            message = validator.utils.message_generator("ERROR","E020",self.dn,"GLUE2StorageShareCapacityUsedSize",\
                      self.value[0],"GLUE2StorageShareCapacityTotalSize is %s" %\
                      self.entry['GLUE2StorageShareCapacityTotalSize'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2StorageShareCapacityTotalSize'][0]), message )

#------------------------------------- GLUE2ToComputingService ---------------------------------------

    def test_GLUE2ToComputingServiceBandwidth_MinRange (self):
        message = validator.utils.message_generator("INFO","I093",self.dn,"GLUE2ToComputingServiceBandwidth",self.value[0])
        self.assertTrue ( int(self.value[0]) >= 100 , message )

    def test_GLUE2ToComputingServiceBandwidth_MaxRange (self):
        message = validator.utils.message_generator("INFO","I094",self.dn,"GLUE2ToComputingServiceBandwidth",self.value[0])
        self.assertTrue ( int(self.value[0]) <= 100000 , message )


