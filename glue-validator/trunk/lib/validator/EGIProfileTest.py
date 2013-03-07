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

#------------------------------------- GLUE2Entity --------------------------------------------

    def test_GLUE2EntityCreationTime_OK (self):
        try:
            creationtime = datetime.datetime.strptime( self.value[0], "%Y-%m-%dT%H:%M:%SZ" )
            now = datetime.datetime.utcnow()
            year = datetime.timedelta(days=365)
            if creationtime > now:
                message = "ERROR: %s has a creation time '%s' in the future!" % (self.dn, self.value[0])
                status = False
            elif creationtime < (now - year):
                message = "WARNING: %s has a creation time '%s' of more than one year ago" % (self.dn, self.value[0]) 
                status = False
            else: 
                message = ""
                status = True
        except ValueError:
            message = ("WARNING: %s publishes CreationTime '%s' that does not follow "
                       "the type Datetime_t") % (self.dn, self.value[0])
            status = False
        self.assertTrue(status, message)

    def test_GLUE2EntityValidity_OK (self):
        if 'GLUE2EntityCreationTime' not in self.entry:
            status = False
            message = ("WARNING: %s should not publish GLUE2EntityValidity since "
                       "GLUE2EntityCreationTime is not published") % (self.dn)
        else:
            try:
                creationtime = datetime.datetime.strptime( self.entry['GLUE2EntityCreationTime'][0], "%Y-%m-%dT%H:%M:%SZ" ) 
                now = datetime.datetime.utcnow()
                validity = datetime.timedelta(seconds=int(self.value[0]))
                if ( creationtime + validity ) < now:
                    message = ("ERROR: %s created in '%s' is no longer valid according to " 
                              "the published validity '%s' seconds!") % \
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
                        message = message + ("\n WARNING: %s publishes unknown value '%s' for the Profile Name "
                                             "in the GLUE2EntityOtherInfo attribute") % (self.dn, val)
                        status = False
                if att == 'ProfileVersion':
                    if not self.types.is_String(val):
                        message = message + ("\n WARNING: %s publishes incorrect profile version '%s' in the "
                                             "GLUE2EntityOtherInfo attribute") % (self.dn, val)
                        status = False
                elif att == 'GRID':
                    if not self.types.is_Grid_t(val):
                        message = message + ("\n INFO: %s publishes wrong Grid Infrastructure '%s' in the "
                                             "GLUE2EntityOtherInfo attribute") % (self.dn, val)
                        status = False
                elif att == 'CONFIG':
                    if not self.types.is_Config_t(val):
                        message = message + ("\n INFO: %s publishes unknown configuration tool '%s' in the "
                                             "GLUE2EntityOtherInfo attribute") % (self.dn, val)
                        status = False
                elif att == 'EGI_NGI':
                    if not self.types.is_EGIngi_t(val):
                        message = message + ("\n INFO: %s publishes unknown EGI NGI '%s' in the "
                                             "GLUE2EntityOtherInfo attribute") % (self.dn, val)
                        status = False
                elif att == 'BLOG':
                    if not self.types.is_URL(val):
                        message = message + ("\n INFO: %s publishes incorrect URL type '%s' for BLOG in the "
                                             "GLUE2EntityOtherInfo attribute") % (self.dn, val)
                        status = False
                elif att == 'ICON':
                    if not self.types.is_URL(val):
                        message = message + ("\n INFO: %s publishes incorrect URL type '%s' for ICON in the "
                                             "GLUE2EntityOtherInfo attribute") % (self.dn, val)
                        status = False
                elif att == 'WLCG_TIER':
                    if not self.types.is_Tier_t(val):
                        message = message + ("\n INFO: %s publishes wrong value '%s' for WLCG Tier in the "
                                             "GLUE2EntityOtherInfo attribute") % (self.dn, val)
                        status = False
                elif att == 'WLCG_NAME' or att == 'WLCG_PARENT':
                    if not self.types.is_WLCGname_t(val):
                        message = message + ("\n INFO: %s publishes unknown WLCG name '%s' for %s attribute in the "
                                             "GLUE2EntityOtherInfo attribute") % (self.dn, val, att)
                        status = False
                elif att == 'WLCG_NAMEICON':
                    if not self.types.is_URL(val):
                        message = message + ("\n INFO: %s publishes incorrect URL type '%s' for WLCG_NAMEICON in the "
                                             "GLUE2EntityOtherInfo attribute") % (self.dn, val)
                        status = False
                elif att == 'MiddlewareName':
                    if not self.types.is_Middleware_t(val):
                        message = message + ("\n INFO: %s publishes incorrect Middleware name '%s' in the "
                                             "GLUE2EntityOtherInfo attribute") % (self.dn, val)
                        status = False
                elif att == 'MiddlewareVersion':
                    if not self.types.is_String(val):
                        message = message + ("\n INFO: %s publishes incorrect Middleware version '%s' in the "
                                             "GLUE2EntityOtherInfo attribute") % (self.dn, val)
                        status = False
                elif att == 'HostDN':
                    if not self.types.is_DN_t(val):
                        message = message + ("\n INFO: %s publishes incorrect Host DN '%s' in the "
                                             "GLUE2EntityOtherInfo attribute") % (self.dn, val)
                        status = False
                elif att == 'Share':
                    index2 = val.find(":")
                    if (index2 > -1):
                        voname = val[:index2]
                        percentage = val[index2 +1:]
                        if not self.types.is_VO_t(voname):
                            message = message + ("\n INFO: %s publishes unknown VO name '%s' for Share in the "
                                                 "GLUE2EntityOtherInfo attribute") % (self.dn, voname)
                            status = False
                        elif voname not in sharedict:
                            if (int(percentage) < 0) or (int(percentage) > 100):
                                message = message + ("\n ERROR: %s publishes wrong percentage '%s' for %s Share in the "
                                                     "GLUE2EntityOtherInfo attribute") % (self.dn, percentage, voname) 
                                status = False
                            sharedict[voname] = int(percentage)
                        else:  
                            message = message + ("\n ERROR: %s publishes VO name '%s' appears more than once in Share "
                                                 "in the GLUE2EntityOtherInfo attribute") % (self.dn, voname)
                            status = False
                    else:
                        message = message + "\n ERROR: %s publishes wrong Share format '%s'" % (self.dn, val)
                        status = False
                elif att.startswith('CPUScalingReference'):
                    if not self.types.is_Benchmarkabbr_t(att.split('CPUScalingReference')[1]):
                        message = message + ("\n INFO: %s publishes incorrect benchmark name '%s' in the "
                                            "GLUE2EntityOtherInfo attribute") % (self.dn,att.split('CPUScalingReference')[1])
                        status = False
            else:
                message = message + ("\n ERROR: %s publishes wrong format specified '%s' in the "
                                     "GLUE2EntityOtherInfo attribute") % (self.dn, pair)
                status = False
        totalshare=0 
        for i in sharedict:
            totalshare = totalshare + sharedict[i]
        if ( totalshare > 100 ):
            message = message + ("\n ERROR: %s publishes shares whose sum '%s' exceeds 100 in the "
                                 "GLUE2EntityOtherInfo attribute !") % (self.dn, totalshare)
            status = False 
        self.assertTrue(status, message)
    
#------------------------------------- GLUE2Location --------------------------------------------

    def test_GLUE2LocationLongitude_OK (self):
        message = "ERROR: %s has Longitude attribute '%s' out of range!" % (self.dn, self.value[0]) 
        self.assertTrue( float(self.value[0]) > -180 and float(self.value[0]) < 180, message)     

    def test_GLUE2LocationLatitude_OK (self):
        message = "ERROR: %s has Latitude attribute '%s' out of range!" % (self.dn, self.value[0])
        self.assertTrue( float(self.value[0]) > -90 and float(self.value[0]) < 90, message)

#------------------------------------- GLUE2Service -----------------------------------------------

    def test_GLUE2ServiceQualityLevel_OK (self):
        message = "INFO: %s should publish 'production' QualityLevel instead of '%s'" % (self.dn, self.value[0])
        self.assertTrue( self.value[0] == 'production', message )

#------------------------------------- GLUE2ComputingService ---------------------------------------

    def test_GLUE2ComputingServiceTotalJobs_OK (self):
        total = 0
        for job in ['GLUE2ComputingServiceRunningJobs',
                    'GLUE2ComputingServiceWaitingJobs',
                    'GLUE2ComputingServiceStagingJobs',
                    'GLUE2ComputingServiceSuspendedJobs',
                    'GLUE2ComputingServicePreLRMSWaitingJobs']:
            if job in self.entry:
                total = total + int(self.entry[job][0])
        message = ("WARNING: %s is publishing a wrong number of total jobs '%s', that does not sum up "
                   "RunningJobs=%s, WaitingJobs=%s, StagingJobs=%s, SuspendedJobs=%s and PreLRMSWaitingJobs=%s")\
                   % (self.dn, self.value[0], self.entry['GLUE2ComputingServiceRunningJobs'][0], \
                      self.entry['GLUE2ComputingServiceWaitingJobs'][0], \
                      self.entry['GLUE2ComputingServiceStagingJobs'][0], \
                      self.entry['GLUE2ComputingServiceSuspendedJobs'][0], \
                      self.entry['GLUE2ComputingServicePreLRMSWaitingJobs'][0])           
        self.assertTrue( total == int(self.value[0]), message ) 

    def test_GLUE2ComputingServiceRunningJobs_OK (self):
        message = "INFO: %s publishes Running Jobs '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingServiceWaitingJobs_OK (self):
        message = "INFO: %s publishes WaitingJobs '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingServiceStagingJobs_OK (self):
        message = "INFO: %s publishes StagingJob '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingServiceSuspendedJobs_OK (self):
        message = "INFO: %s publishes SuspendedJobs '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingServicePreLRMSWaitingJobs_OK (self):
        message = "INFO: %s publishes PreLRMSWaitingJobs '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

#------------------------------------- GLUE2ComputingEndpoint ---------------------------------------

    def test_GLUE2ComputingEndpointQualityLevel_OK (self):
        message = "INFO: %s should publish 'production' QualityLevel instead of '%s'" % (self.dn, self.value[0])
        self.assertTrue( self.value[0] == 'production', message )

    def test_GLUE2EndpointHealthState_OK (self):
        message = "INFO: %s should publish a 'OK' HealthState instead of '%s'" % (self.dn, self.value[0])
        self.assertTrue( self.value[0] == 'ok', message )

    def test_GLUE2ComputingEndpointServingState_OK (self):
        message = "INFO: %s should publish 'production' ServingState instead of '%s'" % (self.dn, self.value[0])
        self.assertTrue( self.value[0] == 'production', message )

    def test_GLUE2EndpointStartTime_OK (self):
        try:
            creationtime = datetime.datetime.strptime( self.value[0], "%Y-%m-%dT%H:%M:%SZ" )
            now = datetime.datetime.utcnow()
            twoyears = datetime.timedelta(days=730)
            if creationtime > now:
                message = "ERROR: %s has a Start time '%s' in the future!" % (self.dn, self.value[0])
                status = False
            elif creationtime < (now - twoyears):
                message = "WARNING: %s has a Start time '%s' of more than two years ago" % (self.dn, self.value[0])
                status = False
            else:
                message = ""
                status = True
        except ValueError:
            message = ("WARNING: %s publishes StartTime '%s' that does not follow the type " 
                       "Datetime_t") % (self.dn, self.value[0])
            status = False
        self.assertTrue(status, message)

    def test_GLUE2EndpointIssuerCA_OK (self):
        message = "INFO: %s publishes 'unknown' for the IssuerCA" % self.dn
        self.assertTrue( self.value[0] != 'unknown', message )

    def test_GLUE2EndpointTrustedCA_OK (self):
        message = "INFO: %s publishes 'unknown' for the TrustedCA" % self.dn
        self.assertTrue( self.value[0] != 'unknown', message )

    def test_GLUE2EndpointDowntimeAnnounce_OK (self):
        try:
            creationtime = datetime.datetime.strptime( self.value[0], "%Y-%m-%dT%H:%M:%SZ" )
            now = datetime.datetime.utcnow()
            year = datetime.timedelta(days=365)
            if creationtime > now:
                message = "ERROR: %s has a Downtime announce '%s' in the future!" % (self.dn, self.value[0])
                status = False
            elif creationtime < (now - year):
                message = "WARNING: %s has a Downtime announce '%s' of more than one year ago" % (self.dn, self.value[0])
                status = False
            else:
                message = ""
                status = True
        except ValueError:
            message = ("WARNING: %s publishes DowntimeAnnounce '%s' that does not follow the type "
                       "Datetime_t") % (self.dn, self.value[0])
            status = False
        self.assertTrue(status, message)

    def test_GLUE2EndpointDowntimeAnnounce_checkStart (self):
       if 'GLUE2EndpointDowntimeStart' not in self.entry:
           message = "WARNING: %s publishes a Downtime announce with no Downtime start published" % (self.dn)
           status = False
           self.assertTrue(status, message)

    def test_GLUE2EndpointDowntimeStart_OK (self):
        try:
            status = True
            message = ""
            starttime = datetime.datetime.strptime( self.value[0], "%Y-%m-%dT%H:%M:%SZ" )
            now = datetime.datetime.utcnow()
            year = datetime.timedelta(days=365)
            if 'GLUE2EndpointDowntimeEnd' in self.entry:
                endtime = datetime.datetime.strptime( self.entry['GLUE2EndpointDowntimeEnd'][0], "%Y-%m-%dT%H:%M:%SZ" )
                if starttime > endtime:
                    message = "ERROR: %s publishes Downtime start time '%s' later than Downtime end time '%s'" % \
                              (self.dn, self.value[0], self.entry['GLUE2EndpointDowntimeEnd'][0])
                    status = False
            elif starttime > (now + year):
                message = "WARNING: %s publishes a Downtime start time '%s' in more than one year !" % \
                          (self.dn, self.value[0])
                status = False
            elif starttime < (now - year):
                message = "WARNING: %s publishes a Downtime start time '%s' of more than one year ago !" % \
                          (self.dn, self.value[0])
                status = False
        except ValueError:
            message = "WARNING: %s publishes DowntimeStart '%s' that does not follow the type Datetime_t" % \
                      (self.dn, self.value[0])
            status = False
        self.assertTrue(status, message)

    def test_GLUE2EndpointDowntimeEnd_OK (self):
        try:
            status = True
            message = ""
            endtime = datetime.datetime.strptime( self.value[0], "%Y-%m-%dT%H:%M:%SZ" )
            now = datetime.datetime.utcnow()
            year = datetime.timedelta(days=365)
            week = datetime.timedelta(days=7)
            if 'GLUE2EndpointDowntimeStart' not in self.entry:
                message = "ERROR: %s publishes Downtime end time with no Downtime start time" % (self.dn)
                status = False
            elif endtime > (now + year):
                message = "WARNING: %s publishes a Downtime end time '%s' in more than one year !" % (self.dn, self.value[0])
                status = False
            elif endtime < (now - week):
                message = "WARNING: %s publishes a Downtime end time '%s' of more than one week ago !" % \
                          (self.dn, self.value[0])
                status = False
        except ValueError:
            message = "WARNING: %s publishes DowntimeEnd '%s' that does not follow the type Datetime_t" % \
                      (self.dn, self.value[0])
            status = False
        self.assertTrue(status, message)

    def test_GLUE2ComputingEndpointTotalJobs_OK (self):
        total = 0
        for job in ['GLUE2ComputingEndpointRunningJobs',
                    'GLUE2ComputingEndpointWaitingJobs',
                    'GLUE2ComputingEndpointStagingJobs',
                    'GLUE2ComputingEndpointSuspendedJobs',
                    'GLUE2ComputingEndpointPreLRMSWaitingJobs']:
            if job in self.entry:
                total = total + int(self.entry[job][0])
        message = ("WARNING: %s is publishing a wrong number of total jobs '%s', that does not sum up "
                   "RunningJobs=%s, WaitingJobs=%s, StagingJobs=%s, SuspendedJobs=%s and PreLRMSWaitingJobs=%s")\
                   % (self.dn, self.value[0], self.entry['GLUE2ComputingEndpointRunningJobs'][0], \
                      self.entry['GLUE2ComputingEndpointWaitingJobs'][0], \
                      self.entry['GLUE2ComputingEndpointStagingJobs'][0], \
                      self.entry['GLUE2ComputingEndpointSuspendedJobs'][0], \
                      self.entry['GLUE2ComputingEndpointPreLRMSWaitingJobs'][0])
        self.assertTrue( total == int(self.value[0]), message )

    def test_GLUE2ComputingEndpointRunningJobs_OK (self):
        message = "INFO: %s publishes Running Jobs '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingEndpointWaitingJobs_OK (self):
        message = "INFO: %s publishes WaitingJobs '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingEndpointStagingJobs_OK (self):
        message = "INFO: %s publishes StagingJob '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingEndpointSuspendedJobs_OK (self):
        message = "INFO: %s publishes SuspendedJobs '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingEndpointPreLRMSWaitingJobs_OK (self):
        message = "INFO: %s publishes PreLRMSWaitingJobs '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

#------------------------------------- GLUE2ComputingShare ---------------------------------------

    def test_GLUE2ComputingShareMaxWallTime_OK (self):
        message = "INFO: %s publishes the default maximum wall time 999999999" % self.dn
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMaxMultiSlotWallTime_OK (self):
        message = "INFO: %s publishes the default multi slot maximum wall time 999999999" % self.dn
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareDefaultWallTime_OK (self):
        message = "INFO: %s publishes the default value for default wall time 999999999" % self.dn
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMinWallTime_OK (self):
        if 'GLUE2ComputingShareMaxWallTime' in self.entry:
            message = "WARNING: %s publishes MinWallTime '%s' > MaxWallTime '%s'" % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxWallTime'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxWallTime'][0]), message )

    def test_GLUE2ComputingShareDefaultWallTime_MaxRange (self):
        if 'GLUE2ComputingShareMaxWallTime' in self.entry:
            message = "WARNING: %s publishes DefaultWallTime '%s' out of MaxWallTime range '%s' !" % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxWallTime'][0])   
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxWallTime'][0]), message )  
            
    def test_GLUE2ComputingShareDefaultWallTime_MinRange (self):
        if 'GLUE2ComputingShareMinWallTime' in self.entry:
            message = "WARNING: %s publishes DefaultWallTime '%s' out of MinWallTime range '%s' !" % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMinWallTime'][0])
            self.assertTrue ( int(self.value[0]) >= int(self.entry['GLUE2ComputingShareMinWallTime'][0]), message )

    def test_GLUE2ComputingShareMaxCPUTime_OK (self):
        message = "INFO: %s publishes the default maximum CPU time 999999999" % self.dn
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMaxTotalCPUTime_OK (self):
        message = "INFO: %s publishes the default multi slot total CPU time 999999999" % self.dn
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareDefaultCPUTime_OK (self):
        message = "INFO: %s publishes the default value for default CPU time 999999999" % self.dn
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMinCPUTime_OK (self):
        if 'GLUE2ComputingShareMaxCPUTime' in self.entry:
            message = "WARNING: %s publishes MinCPUTime '%s' > MaxCPUTime '%s'" % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxCPUTime'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxCPUTime'][0]), message )

    def test_GLUE2ComputingShareDefaultCPUTime_MaxRange (self):
        if 'GLUE2ComputingShareMaxCPUTime' in self.entry:
            message = "WARNING: %s publishes DefaultCPUTime '%s' out of MaxCPUTime range '%s'!" % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxCPUTime'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxCPUTime'][0]), message )

    def test_GLUE2ComputingShareDefaultCPUTime_MinRange (self):
        if 'GLUE2ComputingShareMinCPUTime' in self.entry:
            message = "WARNING: %s publishes DefaultCPUTime '%s' out of MinCPUTime range '%s' !" % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMinCPUTime'][0])
            self.assertTrue ( int(self.value[0]) >= int(self.entry['GLUE2ComputingShareMinCPUTime'][0]), message )

    def test_GLUE2ComputingShareMaxTotalJobs_default (self):
        message = "INFO: %s publishes the default value for max total jobs 999999999" % self.dn
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMaxTotalJobs_zero (self):
        message = "WARNING: %s publishes zero for max total jobs" % self.dn
        self.assertTrue ( int(self.value[0]) != 0, message )

    def test_GLUE2ComputingShareMaxTotalJobs_OK (self):
        running = True
        waiting = True
        message = "WARNING: %s publishes MaxTotalJobs '%s' smaller than MaxRunningJobs or MaxWaitingJobs" % \
                  (self.dn, self.value[0]) 
        if 'GLUE2ComputingShareMaxRunningJobs' in self.entry:
            running = int(self.value[0]) >= int(self.entry['GLUE2ComputingShareMaxRunningJobs'][0])
        if 'GLUE2ComputingShareMaxWaitingJobs' in self.entry:
            waiting = int(self.value[0]) >= int(self.entry['GLUE2ComputingShareMaxWaitingJobs'][0])
        self.assertTrue ( running or waiting, message )

    def test_GLUE2ComputingShareMaxUserRunningJobs_zero (self):
        message = "WARNING: %s publishes zero for maximum user running jobs" % self.dn
        self.assertTrue ( int(self.value[0]) != 0, message )

    def test_GLUE2ComputingShareMaxUserRunningJobs_OK (self):
        if 'GLUE2ComputingShareMaxRunningJobs' in self.entry:
           message = "%s publishes maximum user running jobs '%s' greater than maximum running jobs '%s'" % \
                      (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxRunningJobs'][0])
           self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxRunningJobs'][0]), message )

    def test_GLUE2ComputingShareMaxRunningJobs_OK (self):
        message = "INFO: %s publishes the default value for max running jobs 999999999" % self.dn
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMaxWaitingJobs_OK (self):
        message = "INFO: %s publishes the default value for max waiting jobs 999999999" % self.dn
        self.assertTrue ( int(self.value[0]) != 999999999, message )

    def test_GLUE2ComputingShareMaxSlotsPerJob_zero (self):
        message = "WARNING: %s publishes zero for maximum slots per job" % self.dn
        self.assertTrue ( int(self.value[0]) != 0, message )

    def test_GLUE2ComputingShareTotalJobs_OK (self):
        total = 0
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
        message = ("WARNING: %s is publishing a wrong number of total jobs '%s', that does not sum up "
                   "RunningJobs=%s, LocalRunningJobs=%s, WaitingJobs=%s, LocalWaitingJobs=%s, StagingJobs=%s, "
                   "SuspendedJobs=%s, LocalSuspendedJobs=%s and PreLRMSWaitingJobs=%s")\
                   % (self.dn, self.value[0], self.entry['GLUE2ComputingShareRunningJobs'][0], \
                      self.entry['GLUE2ComputingShareLocalRunningJobs'][0], \
                      self.entry['GLUE2ComputingShareWaitingJobs'][0], \
                      self.entry['GLUE2ComputingShareLocalWaitingJobs'][0], \
                      self.entry['GLUE2ComputingShareStagingJobs'][0], \
                      self.entry['GLUE2ComputingShareSuspendedJobs'][0], \
                      self.entry['GLUE2ComputingShareLocalSuspendedJobs'][0], \
                      self.entry['GLUE2ComputingSharePreLRMSWaitingJobs'][0])
        self.assertTrue( total == int(self.value[0]), message )

    def test_GLUE2ComputingShareRunningJobs_OK (self):
        message = "INFO: %s publishes Running Jobs '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareLocalRunningJobs_OK (self):
        message = "INFO: %s publishes Local Running Jobs '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareWaitingJobs_OK (self):
        message = "INFO: %s publishes WaitingJobs '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareLocalWaitingJobs_OK (self):
        message = "INFO: %s publishes Local WaitingJobs '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareSuspendedJobs_OK (self):
        message = "INFO: %s publishes SuspendedJobs '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareLocalSuspendedJobs_OK (self):
        message = "INFO: %s publishes Local SuspendedJobs '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareStagingJobs_OK (self):
        message = "INFO: %s publishes StagingJob '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingSharePreLRMSWaitingJobs_OK (self):
        message = "INFO: %s publishes PreLRMSWaitingJobs '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareMaxMainMemory_MinRange (self):
        message = "WARNING: %s publishes MaxMainMemory '%s', lower than 100 MB!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) >= 100, message )
   
    def test_GLUE2ComputingShareMaxMainMemory_MaxRange (self):
        message = "INFO: %s publishes MaxMainMemory '%s', greater than 100,000 MB!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 100000, message )

    def test_GLUE2ComputingShareGuaranteedMainMemory_MinRange (self):
        if 'GLUE2ComputingShareMaxMainMemory' in self.entry:
            message = "WARNING: %s publishes GuaranteedMainMemory '%s' greater than MaxMainMemory '%s'!" % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxMainMemory'][0])
            self.assertTrue( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxMainMemory'][0]), message )

    def test_GLUE2ComputingShareGuaranteedMainMemory_MaxRange (self):
        message = "INFO: %s publishes GuaranteedMainMemory '%s', greater than 100,000 MB!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 100000, message )

    def test_GLUE2ComputingShareMaxVirtualMemory_MinRange (self):
        if 'GLUE2ComputingShareMaxMainMemory' in self.entry:
            message = "WARNING: %s publishes MaxVirtualMemory '%s' lower than MaxMainMemory %s!" % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxMainMemory'][0])
            self.assertTrue( int(self.value[0]) >= int(self.entry['GLUE2ComputingShareMaxMainMemory'][0]), message )

    def test_GLUE2ComputingShareMaxVirtualMemory_MaxRange (self):
        message = "INFO: %s publishes MaxVirtualMemory '%s', greater than 100,000 MB!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 100000, message )

    def test_GLUE2ComputingShareGuaranteedVirtualMemory_MinRange (self):
        if 'GLUE2ComputingShareMaxVirtualMemory' in self.entry:
            message = "WARNING: %s publishes GuaranteedVirtualMemory '%s' greater than MaxVirtualMemory '%s'!" % \
                       (self.dn, self.value[0], self.entry['GLUE2ComputingShareMaxVirtualMemory'][0])
            self.assertTrue( int(self.value[0]) <= int(self.entry['GLUE2ComputingShareMaxVirtualMemory'][0]), message )

    def test_GLUE2ComputingShareGuaranteedVirtualMemory_MaxRange (self):
        message = "INFO: %s publishes GuaranteedVirtualMemory '%s', greater than 100,000 MB!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 100000, message )

    def test_GLUE2ComputingShareServingState_OK (self):
        message = "INFO: %s publishes ServingState %s other than 'production'" % (self.dn, self.value[0])
        self.assertTrue( self.value[0] == "production" , message )

    def test_GLUE2ComputingShareEstimatedAverageWaitingTime_OK (self):
        message = "INFO: %s publishes EstimatedAverageWaitingTime '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareEstimatedWorstWaitingTime_OK (self):
        message = "INFO: %s publishes EstimatedWorstWaitingTime '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareFreeSlots_OK (self):
        message = "INFO: %s publishes FreeSlots '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareUsedSlots_OK (self):
        message = "INFO: %s publishes UsedSlots '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingShareRequestedSlots_OK (self):
        message = "INFO: %s publishes FreeSlots '%s', higher than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

#------------------------------------- GLUE2ComputingManager ---------------------------------------

    def test_GLUE2ComputingManagerTotalLogicalCPUs_MinRange (self):
        message = "INFO: %s publishes TotalLogicalCPUs '%s' lower than 10" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) >= 10, message )

    def test_GLUE2ComputingManagerTotalLogicalCPUs_MaxRange (self):
        message = "INFO: %s publishes TotalLogicalCPUs '%s' greater than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )
        
    def test_GLUE2ComputingManagerTotalPhysicalCPUs_OK (self):
        if 'GLUE2ComputingManagerTotalLogicalCPUs' in self.entry:
            message = "%s publishes TotalPhysicalCPUs '%s' greater than TotalLogicalCPUs %s" % \
                      (self.dn, self.value[0], self.entry['GLUE2ComputingManagerTotalLogicalCPUs'][0])
            self.assertTrue( int(self.value[0]) <= int(self.entry['GLUE2ComputingManagerTotalLogicalCPUs'][0]) , message) 

    def test_GLUE2ComputingManagerTotalPhysicalCPUs_MinRange (self):
        message = "INFO: %s publishes TotalPhysicalCPUs '%s' lower than 10" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) >= 10, message )

    def test_GLUE2ComputingManagerTotalPhysicalCPUs_MaxRange (self):
        message = "INFO: %s publishes TotalPhysicalCPUs '%s' greater than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerTotalSlots_OK (self):
        if 'GLUE2ComputingManagerTotalLogicalCPUs' in self.entry:
            message = "%s publishes TotalSlots '%s' greater than twice TotalLogicalCPUs '%s'" % \
                      (self.dn, self.value[0], self.entry['GLUE2ComputingManagerTotalLogicalCPUs'][0])
            self.assertTrue( int(self.value[0]) <= int(self.entry['GLUE2ComputingManagerTotalLogicalCPUs'][0])*2 , message)

    def test_GLUE2ComputingManagerTotalSlots_MinRange (self):
        message = "INFO: %s publishes TotalSlots '%s' lower than 10" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) >= 10, message )

    def test_GLUE2ComputingManagerTotalSlots_MaxRange (self):
        message = "INFO: %s publishes TotalSlots '%s' greater than 1 million!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerSlotsUsedByLocalJobs_OK (self):
        if 'GLUE2ComputingManagerTotalSlots' in self.entry:
            message = "INFO: %s publishes SlotsUsedByLocalJobs '%s' greater than TotalSlots '%s'!" % \
                       (self.dn, self.value[0],self.entry['GLUE2ComputingManagerTotalSlots'][0])
            self.assertTrue( int(self.value[0]) < int(self.entry['GLUE2ComputingManagerTotalSlots']), message )

    def test_GLUE2ComputingManagerSlotsUsedByGridJobs_OK (self):
        if 'GLUE2ComputingManagerTotalSlots' in self.entry:
            message = "INFO: %s publishes SlotsUsedByGridJobs '%s' greater than TotalSlots '%s'!" % \
                       (self.dn, self.value[0],self.entry['GLUE2ComputingManagerTotalSlots'][0])
            self.assertTrue( int(self.value[0]) < int(self.entry['GLUE2ComputingManagerTotalSlots']), message )

    def test_GLUE2ComputingManagerWorkingAreaTotal_OK (self):
        message = "INFO: %s publishes WorkingAreaTotal '%s' GB greater than 1 million GB!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerWorkingAreaFree_OK (self):
        message = "INFO: %s publishes WorkingAreaFree '%s' GB greater than 1 million GB!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerWorkingAreaMultiSlotTotal_OK (self):
        message = "INFO: %s publishes WorkingAreaMultiSlotTotal '%s' GB greater than 1 million GB!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerWorkingAreaMultiSlotFree_OK (self):
        message = "INFO: %s publishes WorkingAreaMultiSlotFree '%s' GB greater than 1 million GB!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerCacheTotal_OK (self):
        message = "INFO: %s publishes CacheTotal '%s' GB greater than 1 million GB!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ComputingManagerCacheFree_OK (self):
        message = "INFO: %s publishes CacheFree '%s' GB greater than 1 million GB!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

#------------------------------------- GLUE2ExecutionEnvironment ---------------------------------------

    def test_GLUE2ExecutionEnvironmentTotalInstances_MinRange (self):
        message = "INFO: %s publishes TotalInstances '%s' less than 10 !" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) > 10, message )

    def test_GLUE2ExecutionEnvironmentTotalInstances_MaxRange (self):
        message = "INFO: %s publishes TotalInstances '%s' greater than 1 million !" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ExecutionEnvironmentUsedInstances_OK (self):
        if 'GLUE2ExecutionEnvironmentTotalInstances' in self.entry:
            message = "INFO: %s publishes UsedInstances '%s' greater than TotalInstances %s !" % \
                       (self.dn, self.value[0], self.entry['GLUE2ExecutionEnvironmentTotalInstances'][0])
            self.assertTrue( int(self.value[0]) < int(self.entry['GLUE2ExecutionEnvironmentTotalInstances'][0]), message )

    def test_GLUE2ExecutionEnvironmentUnavailableInstances_OK (self):
        if 'GLUE2ExecutionEnvironmentTotalInstances' in self.entry:
            message = "INFO: %s publishes UnavailableInstances '%s' greater than TotalInstances %s !" % \
                       (self.dn, self.value[0], self.entry['GLUE2ExecutionEnvironmentTotalInstances'][0])
            self.assertTrue( int(self.value[0]) < int(self.entry['GLUE2ExecutionEnvironmentTotalInstances'][0]), message )

    def test_GLUE2ExecutionEnvironmentPhysicalCPUs_MaxRange (self):
        message = "INFO: %s publishes PhysicalCPUs '%s' greater than 10 !" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) <= 10, message )

    def test_GLUE2ExecutionEnvironmentLogicalCPUs_MaxRange (self):
        message = "INFO: %s publishes LogicalCPUs '%s' greater than 1000 !" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000, message )

    def test_GLUE2ExecutionEnvironmentCPUClockSpeed_MaxRange (self):
        message = "INFO: %s publishes CPUClockSpeed '%s' greater than 10000 !" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) <= 10000, message )

    def test_GLUE2ExecutionEnvironmentCPUClockSpeed_MinRange (self):
        message = "INFO: %s publishes CPUClockSpeed '%s' less than 100 !" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) >= 100, message )

    def test_GLUE2ExecutionEnvironmentCPUTimeScalingFactor_MaxRange (self):
        message = "WARNING: %s publishes CPUTimeScalingFactor '%s' greater than 1 !" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) <= 1, message )

    def test_GLUE2ExecutionEnvironmentCPUTimeScalingFactor_MinRange (self):
        message = "INFO: %s publishes CPUTimeScalingFactor '%s' less than 0.1 !" % (self.dn, self.value[0])
        self.assertTrue( float(self.value[0]) > 0.1, message )

    def test_GLUE2ExecutionEnvironmentWallTimeScalingFactor_MaxRange (self):
        message = "INFO: %s publishes WallTimeScalingFactor '%s' greater than 1 !" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) <= 1, message )

    def test_GLUE2ExecutionEnvironmentWallTimeScalingFactor_MinRange (self):
        message = "INFO: %s publishes WallTimeScalingFactor '%s' less than 0.1 !" % (self.dn, self.value[0])
        self.assertTrue( float(self.value[0]) > 0.1, message )

    def test_GLUE2ExecutionEnvironmentMainMemorySize_MaxRange (self):
        message = "INFO: %s publishes MainMemorySize '%s' MB greater than 1 million MB!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ExecutionEnvironmentMainMemorySize_MinRange (self):
        message = "INFO: %s publishes MainMemorySize '%s' MB less than 100 MB!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) >= 100, message )

    def test_GLUE2ExecutionEnvironmentVirtualMemorySize_MaxRange (self):
        message = "INFO: %s publishes VirtualMemorySize '%s' MB greater than 1 million MB!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) < 1000000, message )

    def test_GLUE2ExecutionEnvironmentVirtualMemorySize_MinRange (self):
        message = "INFO: %s publishes VirtualMemorySize '%s' MB less than 100 MB!" % (self.dn, self.value[0])
        self.assertTrue( int(self.value[0]) >= 100, message )

#------------------------------------- GLUE2ApplicationEnvironment ---------------------------------------

    def test_GLUE2ApplicationEnvironmentRemovalDate_OK (self):
        try:
           removaldate = datetime.datetime.strptime( self.value[0], "%Y-%m-%dT%H:%M:%SZ" )
           now = datetime.datetime.utcnow()
           message = "INFO: % publishes a removal date '%s' in the past !" % (self.dn, self.value[0])
        except ValueError:
            message = "WARNING: %s publishes RemovalDate '%s' that does not follow the type Datetime_t" % (self.dn, self.value[0])
            status = False
        self.asserTrue ( removaldate < now , message )

    def test_GLUE2ApplicationEnvironmentMaxSlots_OK (self):
        message = "INFO: %s publishes zero MaxSlots" % (self.dn)
        self.assertTrue ( int(self.value[0]) != 0, message )

    def test_GLUE2ApplicationEnvironmentMaxJobs_OK (self):
        message = "INFO: %s publishes zero MaxJobs" % (self.dn)
        self.assertTrue ( int(self.value[0]) != 0, message )
 
    def test_GLUE2ApplicationEnvironmentMaxUserSeats_OK (self):
        message = "INFO: %s publishes zero MaxUserSeats" % (self.dn)
        self.assertTrue ( int(self.value[0]) != 0, message )

    def test_GLUE2ApplicationEnvironmentFreeSlots_OK (self):
        if 'GLUE2ApplicationEnvironmentMaxSlots' in self.entry:
            message = "INFO: %s publishes FreeSlots '%s' greater than MaxSlots '%s'" % \
                       (self.dn, self.value[0], self.entry['GLUE2ApplicationEnvironmentMaxSlots'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ApplicationEnvironmentMaxSlots'][0]), message )

    def test_GLUE2ApplicationEnvironmentFreeJobs_OK (self):
        if 'GLUE2ApplicationEnvironmentMaxJobs' in self.entry:
            message = "INFO: %s publishes FreeJobs '%s' greater than MaxJobs '%s'" % \
                       (self.dn, self.value[0], self.entry['GLUE2ApplicationEnvironmentMaxJobs'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ApplicationEnvironmentMaxJobs'][0]), message )

    def test_GLUE2ApplicationEnvironmentFreeUserSeats_OK (self):
        if 'GLUE2ApplicationEnvironmentMaxUserSeats' in self.entry:
            message = "INFO: %s publishes FreeUserSeats '%s' greater than MaxUserSeats '%s'" % \
                       (self.dn, self.value[0], self.entry['GLUE2ApplicationEnvironmentMaxUserSeats'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2ApplicationEnvironmentMaxUserSeats'][0]), message )

#------------------------------------- GLUE2StorageServiceCapacity ---------------------------------------

    def test_GLUE2StorageServiceCapacityTotalSize_OK (self):
        total = 0
        for cap in ['GLUE2StorageServiceCapacityFreeSize',
                    'GLUE2StorageServiceCapacityUsedSize',
                    'GLUE2StorageServiceCapacityReservedSize']:
            if cap in self.entry:
                total = total + int(self.entry[cap][0])
        message = ("ERROR: %s is publishing a wrong number of total size for storage capacity '%s', "
                   "that does not sum up FreeSize=%s, UsedSize=%s and ReservedSize=%s") % \
                   (self.dn, self.value[0], self.entry['GLUE2StorageServiceCapacityFreeSize'][0], \
                    self.entry['GLUE2StorageServiceCapacityUsedSize'][0], \
                    self.entry['GLUE2StorageServiceCapacityReservedSize'][0])
        self.assertTrue( total == int(self.value[0]), message )

    def test_GLUE2StorageServiceCapacityTotalSize_MinRange (self):
        if 'GLUE2StorageServiceCapacityType' in self.entry:
            if self.entry['GLUE2StorageServiceCapacityType'][0] == 'online' or \
               self.entry['GLUE2StorageServiceCapacityType'][0] == 'nearline':
                   message = "INFO: %s publishes TotalSize storage capacity '%s' less than 1000" % \
                              (self.dn, self.value[0])
                   self.assertTrue ( int(self.value[0]) >= 1000 , message ) 

    def test_GLUE2StorageServiceCapacityTotalSize_MaxRange (self):
        if 'GLUE2StorageServiceCapacityType' in self.entry:
            if self.entry['GLUE2StorageServiceCapacityType'][0] == 'online' or \
               self.entry['GLUE2StorageServiceCapacityType'][0] == 'nearline':
                   message = "INFO: %s publishes TotalSize storage capacity '%s' greater than 1 million" % \
                              (self.dn, self.value[0])
                   self.assertTrue ( int(self.value[0]) <= 1000000 , message )

    def test_GLUE2StorageServiceCapacityFreeSize_OK (self):
        if 'GLUE2StorageServiceCapacityTotalSize' in self.entry:
            message = "ERROR: %s publishes FreeSize %s greater than TotalSize %s" % \
                       (self.dn, self.value[0], self.entry['GLUE2StorageServiceCapacityTotalSize'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2StorageServiceCapacityTotalSize'][0]), message )

    def test_GLUE2StorageServiceCapacityUsedSize_OK (self):
        if 'GLUE2StorageServiceCapacityUsedSize' in self.entry:
            message = "ERROR: %s publishes UsedSize '%s' greater than TotalSize '%s'" % \
                       (self.dn, self.value[0], self.entry['GLUE2StorageServiceCapacityUsedSize'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2StorageServiceCapacityUsedSize'][0]), message )

    def test_GLUE2StorageServiceCapacityReservedSize_OK (self):
        if 'GLUE2StorageServiceCapacityReservedSize' in self.entry:
            message = "ERROR: %s publishes ReservedSize '%s' greater than TotalSize '%s'" % \
                       (self.dn, self.value[0], self.entry['GLUE2StorageServiceCapacityReservedSize'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2StorageServiceCapacityReservedSize'][0]), message )

#------------------------------------- GLUE2StorageShare ---------------------------------------

    def test_GLUE2StorageShareServingState_OK (self):
        message = "INFO: %s should publish 'production' ServingState instead of '%s'" % (self.dn, self.value[0])
        self.assertTrue( self.value[0] == 'production', message )

    def test_GLUE2StorageShareAccessLatency_OK (self):
        message = "INFO: %s publishes 'offline' for AccessLatency" % (self.dn)
        self.assertTrue ( self.value[0] != 'offline', message )

    def test_GLUE2StorageShareRetentionPolicy_OK (self):
        message = "INFO: %s publishes RetentionPolicy '%s'" % (self.dn, self.value[0])
        self.assertTrue ( self.value[0] == 'custodial' or self.value[0] == 'replica', message )

    def test_GLUE2StorageShareExpirationMode_OK (self):
        message = "INFO: %s publishes ExpirationMode '%s'" % (self.dn, self.value[0])
        self.assertTrue ( self.value[0] == 'neverexpire', message )

    def test_GLUE2StorageShareDefaultLifeTime_OK (self):
        message = "INFO: %s publishes DefaultLifeTime '%s' less than 100000 seconds" % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) >= 100000 , message )

    def test_GLUE2StorageShareMaximumLifeTime_OK (self):
        message = "INFO: %s publishes MaximumLifeTime '%s' less than 100000 seconds" % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) >= 100000 , message )

#------------------------------------- GLUE2StorageShareCapacity ---------------------------------------

    def test_GLUE2StorageShareCapacityTotalSize_OK (self):
        total = 0
        for share in ['GLUE2StorageShareCapacityFreeSize', 'GLUE2StorageShareCapacityUsedSize']:
            if share in self.entry:
                total = total + int(self.entry[share][0])
        message = ("ERROR: %s is publishing a wrong number of total size for storage share capacity '%s', "
                   "that does not sum up FreeSize=%s and UsedSize=%s") % \
                   (self.dn, self.value[0], self.entry['GLUE2StorageShareCapacityFreeSize'][0], \
                    self.entry['GLUE2StorageShareCapacityUsedSize'][0])
        self.assertTrue( total <= int(self.value[0]), message )

    def test_GLUE2StorageShareCapacityTotalSize_MinRange (self):
        message = "INFO: %s publishes TotalSize share capacity '%s' less than 1000" % \
                   (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) >= 1000, message )

    def test_GLUE2StorageShareCapacityTotalSize_MaxRange (self):
        message = "INFO: %s publishes TotalSize share capacity '%s' greater than 1 million" % \
                   (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) <= 1000000, message )

    def test_GLUE2StorageShareCapacityFreeSize_OK (self):
        if 'GLUE2StorageShareCapacityTotalSize' in self.entry:
            message = "ERROR: %s publishes FreeSize '%s' greater than TotalSize '%s'" % \
                       (self.dn, self.value[0], self.entry['GLUE2StorageShareCapacityTotalSize'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2StorageShareCapacityTotalSize'][0]), message )

    def test_GLUE2StorageShareCapacityUsedSize_OK (self):
        if 'GLUE2StorageShareCapacityUsedSize' in self.entry:
            message = "ERROR: %s publishes UsedSize '%s' greater than TotalSize '%s'" % \
                       (self.dn, self.value[0], self.entry['GLUE2StorageShareCapacityUsedSize'][0])
            self.assertTrue ( int(self.value[0]) <= int(self.entry['GLUE2StorageShareCapacityUsedSize'][0]), message )

#------------------------------------- GLUE2ToComputingService ---------------------------------------

    def test_GLUE2ToComputingServiceBandwidth_MinRange (self):
        message = "INFO: %s publishes a bandwith '%s' less than 100" % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) >= 100 , message )

    def test_GLUE2ToComputingServiceBandwidth_MaxRange (self):
        message = "INFO: %s publishes a bandwith '%s' greater than 100000" % (self.dn, self.value[0])
        self.assertTrue ( int(self.value[0]) <= 100000 , message )


