#!/usr/bin/python
#
# Script to compare WLCG accounting results with the BDII numbers
#
###############################################################

import subprocess
import os, sys
import datetime
from cStringIO import StringIO
import simplejson as json
import urllib2


t1_bdiis = {
'CERN-PROD'         : "prod-bdii.cern.ch:2170",
'BNL-ATLAS'         : "is.grid.iu.edu:2180",
'FZK-LCG2'          : "giis-fzk.gridka.de:2170",
'IN2P3-CC'          : "cclcgip03.in2p3.fr:2170",
'INFN-T1'           : "sg01-lcg.cr.cnaf.infn.it:2170",
'KR-KISTI-GSDC-01'  : "sbdii-gsdc1.sdfarm.kr:2170",
'NDGF-T1'           : "bdii.ndgf.org:2170", 
'NIKHEF-ELPROD'     : "siteinfo03.nikhef.nl:2170",
'pic'               : "site-bdii.pic.es:2170",
'RAL-LCG2'          : "site-bdii.gridpp.rl.ac.uk:2170",
'SARA-MATRIX'       : "sitebdii.grid.sara.nl:2170",
'Taiwan-LCG2'       : "w-bdii.grid.sinica.edu.tw:2170",
'TRIUMF-LCG2'       : "site-bdii.triumf.ca:2170",  
'USCMS-FNAL-WC1'    : "is.grid.iu.edu:2180"
}

t1_sites = {
'CERN'             : ['CERN-PROD'],
'BNL'              : ['BNL-ATLAS'],
'KIT'              : ['FZK-LCG2'],
'CC-IN2P3'         : ['IN2P3-CC'],
'CNAF'             : ['INFN-T1'],
'KR-KISTI-GSDC'    : ['KR-KISTI-GSDC-01'],
'NDGF'             : ['NDGF-T1'],
'NL-T1'            : ['NIKHEF-ELPROD','SARA-MATRIX'], 
'pic'              : ['pic'],
'RAL'              : ['RAL-LCG2'],
'ASGC'             : ['Taiwan-LCG2'],
'TRIUMF'           : ['TRIUMF-LCG2'],
'FNAL'             : ['USCMS-FNAL-WC1']
}

t1_pledges = {
'CERN'       : {
'cpu'        : {'Feb' : 356000},
'disk'       : {'Feb' : 29100},
'tape'       : {'Feb' : 67400}
},
'BNL'        : { 
'cpu'        : {'Feb' : 74000},
'disk'       : {'Feb' : 11300},
'tape'       : {'Feb' : 10000}
},
'KIT'        : {
'cpu'        : {'Feb' : 106585},
'disk'       : {'Feb' : 11000},
'tape'       : {'Feb' : 14400}
},
'CC-IN2P3'   : {
'cpu'        : {'Feb' : 67350},
'disk'       : {'Feb' : 7000},
'tape'       : {'Feb' : 11025}
},
'CNAF'       : {
'cpu'        : {'Feb' : 88050},
'disk'       : {'Feb' : 10252},
'tape'       : {'Feb' : 15800}
},
'KR-KISTI-GSDC'        : {
'cpu'        : {'Feb' : 14500},
'disk'       : {'Feb' : 990},
'tape'       : {'Feb' : 1040}
},
'NDGF'       : {
'cpu'        : {'Feb' : 30900},
'disk'       : {'Feb' : 5129},
'tape'       : {'Feb' : 5464}
},
'NL-T1'      : {
'cpu'        : {'Feb' : 47296},
'disk'       : {'Feb' : 5362},
'tape'       : {'Feb' : 5593}
},
'pic'        : {
'cpu'        : {'Feb' : 31143},
'disk'       : {'Feb' : 3850},
'tape'       : {'Feb' : 5887}
},
'RAL'        : {
'cpu'        : {'Feb' : 90246},
'disk'       : {'Feb' : 9667},
'tape'       : {'Feb' : 12122}
},
'ASGC'       : {
'cpu'        : {'Feb' : 36165},
'disk'       : {'Feb' : 4275},
'tape'       : {'Feb' : 4000}
},
'TRIUMF'     : {
'cpu'        : {'Feb' : 70226},
'disk'       : {'Feb' : 6420},
'tape'       : {'Feb' : 5300}
},
'FNAL'       : {
'cpu'        : {'Feb' : 58000},
'disk'       : {'Feb' : 11000},
'tape'       : {'Feb' : 22000}
}
}

t1_dict = {}
t1_bdii_dict = {}

# Change every month
month = "Feb"

cpu_acc = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/accounting/cpu_acc_%s.txt" % (month)
cpu_acc_fd=os.open(cpu_acc, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
cpu_rebus = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/accounting/cpu_rebus_%s.txt" % (month)
cpu_rebus_fd=os.open(cpu_rebus, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
cpu_bdii = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/accounting/cpu_bdii_%s.txt" % (month)
cpu_bdii_fd=os.open(cpu_bdii, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
disk_acc = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/accounting/disk_acc_%s.txt" % (month)
disk_acc_fd=os.open(disk_acc, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
disk_rebus = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/accounting/disk_rebus_%s.txt" % (month)
disk_rebus_fd=os.open(disk_rebus, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
disk_bdii = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/accounting/disk_bdii_%s.txt" % (month)
disk_bdii_fd=os.open(disk_bdii, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
tape_acc = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/accounting/tape_acc_%s.txt" % (month)
tape_acc_fd=os.open(tape_acc, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
tape_rebus = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/accounting/tape_rebus_%s.txt" % (month)
tape_rebus_fd=os.open(tape_rebus, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
tape_bdii = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/accounting/tape_bdii_%s.txt" % (month)
tape_bdii_fd=os.open(tape_bdii, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)


# get full site installed capacities from REBUS
def site_full_capacities_json_to_dict ():

    url = "http://rebus.cern.ch/apps/capacities/sites/ALL/2014/3/json"
    json_file = urllib2.urlopen(url).read()
    sites = json.loads(json_file)
    for site in sites:
       if site['Site'] in t1_bdiis.keys():
           t1_dict[site['Site']] = {'PhysicalCPUs' :     0,
                                    'TotalNearlineSize': 0,
                                    'LogicalCPUs':       0,
                                    'HEPSPEC06':         0,
                                    'TotalOnlineSize':   0 }
           t1_dict[site['Site']]['PhysicalCPUs'] = site['PhysicalCPUs']
           t1_dict[site['Site']]['LogicalCPUs'] = site['LogicalCPUs']
           t1_dict[site['Site']]['HEPSPEC06'] = site['HEPSPEC06']
           t1_dict[site['Site']]['TotalNearlineSize'] = site['TotalNearlineSize']
           t1_dict[site['Site']]['TotalOnlineSize'] = site['TotalOnlineSize']

# get WLCG VOs installed capacities from REBUS
def site_wlcg_capacities_json_to_dict ():

    url_dict = { 'atlas' : "http://rebus.cern.ch/apps/capacities/sites/ATLAS/2014/3/json",
                 'alice' : "http://rebus.cern.ch/apps/capacities/sites/ALICE/2014/3/json",
                 'cms'   : "http://rebus.cern.ch/apps/capacities/sites/CMS/2014/3/json",
                 'lhcb'  : "http://rebus.cern.ch/apps/capacities/sites/LHCB/2014/3/json" }

    for vo in url_dict.keys():
        json_file = urllib2.urlopen(url_dict[vo]).read()
        sites = json.loads(json_file)
        for site in sites:
            if site['Site'] in t1_bdiis.keys():
                if site['Site'] not in t1_dict: 
                    t1_dict[site['Site']] = {'PhysicalCPUs' :     0,
                                             'TotalNearlineSize': 0,
                                             'LogicalCPUs':       0,
                                             'HEPSPEC06':         0,
                                             'TotalOnlineSize':   0 }
                else:
                    t1_dict[site['Site']]['PhysicalCPUs'] = t1_dict[site['Site']]['PhysicalCPUs'] + site['PhysicalCPUs']
                    t1_dict[site['Site']]['LogicalCPUs'] = t1_dict[site['Site']]['LogicalCPUs'] + site['LogicalCPUs']
                    t1_dict[site['Site']]['HEPSPEC06'] = t1_dict[site['Site']]['HEPSPEC06'] + site['HEPSPEC06']
                    t1_dict[site['Site']]['TotalNearlineSize'] = t1_dict[site['Site']]['TotalNearlineSize'] + \
                                                                 site['TotalNearlineSize']
                    t1_dict[site['Site']]['TotalOnlineSize'] = t1_dict[site['Site']]['TotalOnlineSize'] + \
                                                               site['TotalOnlineSize']

def cpu_power (site):

    print "----------> %s" % (site)
    share_dict = { 'atlas' : 0, 'alice' : 0, 'cms' : 0, 'lhcb' : 0 }

    share = "ldapsearch -x -LLL -h %s -b mds-vo-name=%s,o=grid '(objectClass=GlueCE)' GlueCECapability \
             | grep Share | tr '[:upper:]' '[:lower:]' | grep -E 'atlas|alice|cms|lhcb' \
             | sort | uniq | cut -d\"=\" -f2" % (t1_bdiis[site],site)

    p = subprocess.Popen(share, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    results = p.communicate()
    full_text=results[0].strip()
    #print "Share %s %s" % (site,full_text)
    index1=full_text.find("Error:")
    index2=full_text.find("UNKNOWN:")
    index3=full_text.find("Can't contact")
    if (index1 > -1) or (index2 > -1) or (index3 > -1):
        t1_bdii_dict[site]['color']['cpu'] = "grey"
        t1_bdii_dict[site]['cpu'] = "Unreachable"
        return
    elif ( full_text == ""):
        total_share = 1
    else:
        shares = full_text.splitlines(True)
        for i in shares:
            vo,share=i.split(":")
            if vo not in share_dict:
                share_dict[vo] = int(share)
            else:
                if int(share) > share_dict[vo]:
                    share_dict[vo] = int(share)    
        total_share = share_dict ['atlas'] + share_dict ['alice'] + share_dict ['cms'] + share_dict ['lhcb']
        #print "Total Share Sum = %s" % (total_share)
        if total_share > 100:
            total_share = 1
        else:
            total_share = float(total_share) / 100
    print "Total Share = %.2f" % (total_share)

    subclusters = "ldapsearch -x -LLL -h %s -b mds-vo-name=%s,o=grid '(objectClass=GlueSubcluster)' \
                   GlueSubclusterUniqueID | grep GlueSubClusterUniqueID: | cut -d\":\" -f2" % (t1_bdiis[site],site)

    p = subprocess.Popen(subclusters, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    results = p.communicate()
    full_text=results[0].strip()
    index1=full_text.find("Error:")
    index2=full_text.find("UNKNOWN:")
    index3=full_text.find("Can't contact")
    if (index1 > -1) or (index2 > -1) or (index3 > -1):
        t1_bdii_dict[site]['color']['cpu'] = "grey"
        t1_bdii_dict[site]['cpu'] = "Unreachable"
        return
    elif ( full_text == ""):
        t1_bdii_dict[site]['color']['cpu'] = "pink"
        t1_bdii_dict[site]['cpu'] = "No_subclusters"
        return

    subclus = full_text.splitlines(True)
    wlcg_cpu_power = 0
    for i in subclus:
        logicalcpus = "ldapsearch -x -LLL -h %s -b mds-vo-name=%s,o=grid \
                       '(&(objectClass=GlueSubcluster)(GlueSubclusterUniqueID=%s))' \
                       GlueSubClusterLogicalCPUs | grep GlueSubClusterLogicalCPUs: | cut -d\":\" -f2" \
                       % (t1_bdiis[site],site,i.strip())

        p = subprocess.Popen(logicalcpus, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        results = p.communicate()
        full_text=results[0].strip()
        print "log cpus %s" % (full_text)
        index1=full_text.find("Error:")
        index2=full_text.find("UNKNOWN:")
        index3=full_text.find("Can't contact")
        if (index1 > -1) or (index2 > -1) or (index3 > -1):
            t1_bdii_dict[site]['color']['cpu'] = "grey"
            t1_bdii_dict[site]['cpu'] = "Unreachable"
            return
        elif ( full_text == ""):
            full_text = 0

        logcpus = int(full_text)

        if (logcpus != 0):
            hepspec = "ldapsearch -x -LLL -h %s -b mds-vo-name=%s,o=grid \
                       '(&(objectClass=GlueSubcluster)(GlueSubclusterUniqueID=%s))' \
                       GlueHostProcessorOtherDescription | grep GlueHostProcessorOtherDescription: \
                       | awk -F\"=\" '{ print $NF }' | cut -d\"-\" -f1" % (t1_bdiis[site],site,i.strip())    

            p = subprocess.Popen(hepspec, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            results = p.communicate()
            full_text=results[0].strip()
            print "hepspec %s" % (full_text)
            index1=full_text.find("Error:")
            index2=full_text.find("UNKNOWN:")
            index3=full_text.find("Can't contact")
            if (index1 > -1) or (index2 > -1) or (index3 > -1):
                t1_bdii_dict[site]['color']['cpu'] = "grey"
                t1_bdii_dict[site]['cpu'] = "Unreachable"
                return
            elif ( full_text == ""):
                full_text = 0

            benchmark = float(full_text)

            wlcg_cpu_power = wlcg_cpu_power + int(logcpus * benchmark * total_share)      

    print "CPU power: %s" % (wlcg_cpu_power)
    
    t1_bdii_dict[site]['color']['cpu'] = "yellow"
    t1_bdii_dict[site]['cpu'] = wlcg_cpu_power

# get WLCG VO installed capacities from BDII
def site_wlcg_capacities_bdii_to_dict ():

    for site in t1_bdiis.keys():
        query_dict = { 'disk' : "ldapsearch -LLL -x -h %s -b mds-vo-name=%s,o=grid \
                                 '(&(objectClass=GlueSA)(|(GlueSAAccessControlBaseRule=*atlas*)\
                                                          (GlueSAAccessControlBaseRule=*cms*)\
                                                          (GlueSAAccessControlBaseRule=*alice*)\
                                                          (GlueSAAccessControlBaseRule=*lhcb*)))' \
                                 GlueSATotalOnlineSize | grep GlueSATotalOnlineSize: | cut -d\":\" -f2 \
                                 | awk 'NF!=0 {print}' | awk '{sum+=$1} END {print sum}'" % (t1_bdiis[site],site),
                       'tape' : "ldapsearch -LLL -x -h %s -b mds-vo-name=%s,o=grid \
                                 '(&(objectClass=GlueSA)(|(GlueSAAccessControlBaseRule=*atlas*)\
                                                          (GlueSAAccessControlBaseRule=*cms*)\
                                                          (GlueSAAccessControlBaseRule=*alice*)\
                                                          (GlueSAAccessControlBaseRule=*lhcb*)))' \
                                 GlueSATotalNearlineSize | grep GlueSATotalNearlineSize: | cut -d\":\" -f2 \
                                 | awk 'NF!=0 {print}' | awk '{sum+=$1} END {print sum}'" % (t1_bdiis[site],site) }

        t1_bdii_dict[site] = { 'color' : { 'cpu' : "", 'disk' : "", 'tape' : "" },
                               'cpu'   : 0,
                               'disk'  : 0,
                               'tape'  : 0 }

        cpu_power(site)  

        for query in query_dict.keys():
            p = subprocess.Popen(query_dict[query], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            results = p.communicate()
            full_text=results[0].strip()
            index1=full_text.find("Error:")
            index2=full_text.find("UNKNOWN:")
            index3=full_text.find("Can't contact")   
            if (index1 > -1) or (index2 > -1) or (index3 > -1):  
                t1_bdii_dict[site]['color'][query] = "grey"
                t1_bdii_dict[site][query] = "Unreachable"
            elif ( full_text == ""):
                t1_bdii_dict[site]['color'][query] = "pink"
                t1_bdii_dict[site][query] = "No_LHC_shares"
            else: 
                t1_bdii_dict[site]['color'][query] = "yellow"
                t1_bdii_dict[site][query] = int(full_text)
                

#site_full_capacities_json_to_dict ()
site_wlcg_capacities_json_to_dict ()
site_wlcg_capacities_bdii_to_dict ()
for t1 in sorted(t1_sites.keys()):

    dt=datetime.datetime.now()
    #print ("%s ------>") % (site_name)
    rebus_cpu = 0
    rebus_disk = 0
    rebus_tape = 0
    for site_name in t1_sites[t1]:
        rebus_cpu = rebus_cpu + t1_dict[site_name]['HEPSPEC06']
        rebus_disk = rebus_disk + t1_dict[site_name]['TotalOnlineSize']
        rebus_tape = rebus_tape + t1_dict[site_name]['TotalNearlineSize']

    bdii_cpu = 0
    bdii_disk = 0
    bdii_tape = 0
    for site_name in t1_sites[t1]:
        if t1_bdii_dict[site_name]['color']['cpu'] == "yellow":
            bdii_cpu = bdii_cpu + t1_bdii_dict[site_name]['cpu']
        else:
             bdii_cpu = t1_bdii_dict[site_name]['cpu']
        if t1_bdii_dict[site_name]['color']['disk'] == "yellow":
            bdii_disk = bdii_disk + t1_bdii_dict[site_name]['disk']
        else: 
            bdii_disk = t1_bdii_dict[site_name]['disk']
        if t1_bdii_dict[site_name]['color']['tape'] == "yellow": 
            bdii_tape = bdii_tape + t1_bdii_dict[site_name]['tape']
        else: 
            bdii_tape = t1_bdii_dict[site_name]['tape'] 

    # WLCG accounting is in TB and REBUS/BDII is in GB
    rebus_disk=rebus_disk/1024
    rebus_tape=rebus_tape/1024    
    bdii_disk=bdii_disk/1024
    bdii_tape=bdii_tape/1024    

    result_string="%s %s %s %s %s\n" % (dt,t1,rebus_cpu,"orange","None") 
    os.write(cpu_rebus_fd,result_string)
    result_string="%s %s %s %s %s\n" % (dt,t1,bdii_cpu,t1_bdii_dict[site_name]['color']['cpu'],"None")
    os.write(cpu_bdii_fd,result_string)
    result_string="%s %s %s %s %s\n" % (dt,t1,t1_pledges[t1]["cpu"][month],"green","None")
    os.write(cpu_acc_fd,result_string)

    result_string="%s %s %s %s %s\n" % (dt,t1,rebus_disk,"orange","None")
    os.write(disk_rebus_fd,result_string)
    result_string="%s %s %s %s %s\n" % (dt,t1,bdii_disk,t1_bdii_dict[site_name]['color']['disk'],"None")
    os.write(disk_bdii_fd,result_string)
    result_string="%s %s %s %s %s\n" % (dt,t1,t1_pledges[t1]["disk"][month],"green","None")
    os.write(disk_acc_fd,result_string)

    result_string="%s %s %s %s %s\n" % (dt,t1,rebus_tape,"orange","None")
    os.write(tape_rebus_fd,result_string)
    result_string="%s %s %s %s %s\n" % (dt,t1,bdii_tape,t1_bdii_dict[site_name]['color']['tape'],"None")
    os.write(tape_bdii_fd,result_string)
    result_string="%s %s %s %s %s\n" % (dt,t1,t1_pledges[t1]["tape"][month],"green","None")
    os.write(tape_acc_fd,result_string)

os.close(cpu_rebus_fd)
os.close(cpu_bdii_fd)
os.close(cpu_acc_fd)
os.close(disk_rebus_fd)
os.close(disk_bdii_fd)
os.close(disk_acc_fd)
os.close(tape_rebus_fd)
os.close(tape_bdii_fd)
os.close(tape_acc_fd)

