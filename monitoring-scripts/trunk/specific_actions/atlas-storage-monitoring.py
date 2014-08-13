#!/usr/bin/python
#
# Script to monitor Storage Capacity (BDII vs SRM) for ATLAS sites
#
###############################################################

import subprocess
import os, sys
import datetime
from cStringIO import StringIO
import simplejson as json
import urllib2
import urllib
import sites
from xml.dom import minidom
from pprint import pprint



path_to_output = "/afs/cern.ch/user/m/malandes/www/web/ssb/atlas/storage"
path_to_url = "http://malandes.web.cern.ch/malandes/ssb/atlas/storage"
base_xml_url = "http://bourricot.cern.ch/SLS/data"

log_file = "%s/atlas_storage_log.txt" % (path_to_output)
results_free = "%s/atlas_storage_free.txt" % (path_to_output) 
results_total = "%s/atlas_storage_total.txt" % (path_to_output) 
log_fd = os.open(log_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
free_fd = os.open(results_free, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
total_fd = os.open(results_total, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)

srm_dict = {}
bdii_dict = {}
token_dict = {}

t1_list = [ 'CERN-PROD', 'BNL-ATLAS', 'FZK-LCG2', 'IN2P3-CC', 'INFN-T1', 'KR-KISTI-GSDC-01', 'NDGF-T1', 'NIKHEF-ELPROD',
            'pic', 'RAL-LCG2', 'SARA-MATRIX', 'Taiwan-LCG2', 'TRIUMF-LCG2', 'USCMS-FNAL-WC1' ]

# Parsing the DDM endpoint json file to store token - ddmendpoint relationships
def site_token_ddmendpoint_to_dict ():

    url = "http://atlas-agis-api.cern.ch/request/ddmendpoint/query/list/?json"
    json_file = urllib2.urlopen(url).read()
    ddmendpoints = json.loads(json_file)
    for ddmendpoint in ddmendpoints:
        if ddmendpoint["rc_site"] not in token_dict:
            token_dict[ddmendpoint["rc_site"]] = { "ATLASDATADISK" : [],
                                                   "ATLASPRODDISK" : [], 
                                                   "ATLASSCRATCHDISK" : [], 
                                                   "ATLASLOCALGROUPDISK" : [], 
                                                   "ATLASGROUPDISK" : [], 
                                                   "ATLASHOTDISK" : [], 
                                                   "ATLASDATATAPE" : [], 
                                                   "ATLASMCTAPE" : [] 
                                                 }
        if ddmendpoint["token"] in token_dict[ddmendpoint["rc_site"]]:
            token_dict[ddmendpoint["rc_site"]][ddmendpoint["token"]].append(ddmendpoint["name"])
    #pprint (token_dict)         

# Parsing the SRM information from the XML files provided by ATLAS DDM endpoints
def site_srm_storage_xml_to_dict ():

    for site in sorted(token_dict.keys()):
        srm_dict[site] = { "ATLASDATADISK" : { "Total" : 0, "Free" : 0, "color" : "" },
                           "ATLASPRODDISK" : { "Total" : 0, "Free" : 0, "color" : "" },
                           "ATLASSCRATCHDISK" : { "Total" : 0, "Free" : 0, "color" : "" },
                           "ATLASLOCALGROUPDISK" : { "Total" : 0, "Free" : 0, "color" : "" },
                           "ATLASGROUPDISK" : { "Total" : 0, "Free" : 0, "color" : "" },
                           "ATLASHOTDISK" : { "Total" : 0, "Free" : 0, "color" : "" },
                           "ATLASDATATAPE" : { "Total" : 0, "Free" : 0, "color" : "" },
                           "ATLASMCTAPE" : { "Total" : 0, "Free" : 0, "color" : "" }
                         }
        for token in ["ATLASDATADISK", "ATLASPRODDISK", "ATLASSCRATCHDISK", "ATLASLOCALGROUPDISK", "ATLASGROUPDISK", \
                      "ATLASHOTDISK", "ATLASDATATAPE", "ATLASMCTAPE" ]:
            if token_dict[site][token]: 
                for ddmendpoint in token_dict[site][token]:
                    #print "%s/%s.xml" % (base_xml_url,ddmendpoint)
                    xml_file_name = "%s/%s.xml" % (base_xml_url,ddmendpoint)
                    try:
                        xml_file = urllib2.urlopen(xml_file_name)
                        tree = minidom.parse(xml_file)
                        for subelement in tree.getElementsByTagName('numericvalue'):
                            if (subelement.attributes['name'].value == "Total space"):
                                srm_dict[site][token]["Total"] = srm_dict[site][token]["Total"] + \
                                                                 int(float(subelement.firstChild.nodeValue))
                            elif (subelement.attributes['name'].value == "Free space"):
                                srm_dict[site][token]["Free"] = srm_dict[site][token]["Free"] + \
                                                                int(float(subelement.firstChild.nodeValue))
                        srm_dict[site][token]['color'] = "green"
                    except urllib2.HTTPError:
                        output = "Error to open %s\n" % (xml_file_name)
                        os.write(log_fd,output)    
            else:
                srm_dict[site][token]['color'] = "pink"
                srm_dict[site][token]["Total"] = "No_such_token"
                srm_dict[site][token]["Free"] = "No_such_token"


# get storage capacities from BDII
def site_bdii_storage_to_dict ():

    for site in sorted(srm_dict.keys()):
        if site in sites.atlas_site_bdiis: 
            bdii_dict[site] = { "ATLASDATADISK" : { "Total" : 0, "Free" : 0, "color" : "" },
                                "ATLASPRODDISK" : { "Total" : 0, "Free" : 0, "color" : "" },
                                "ATLASSCRATCHDISK" : { "Total" : 0, "Free" : 0, "color" : "" },
                                "ATLASLOCALGROUPDISK" : { "Total" : 0, "Free" : 0, "color" : "" },
                                "ATLASGROUPDISK" : { "Total" : 0, "Free" : 0, "color" : "" },
                                "ATLASHOTDISK" : { "Total" : 0, "Free" : 0, "color" : "" },
                                "ATLASDATATAPE" : { "Total" : 0, "Free" : 0, "color" : "" },
                                "ATLASMCTAPE" : { "Total" : 0, "Free" : 0, "color" : "" }
                              }
            for token in ["ATLASDATADISK", "ATLASPRODDISK", "ATLASSCRATCHDISK", "ATLASLOCALGROUPDISK", "ATLASGROUPDISK", \
                          "ATLASHOTDISK", "ATLASDATATAPE", "ATLASMCTAPE" ]:
                
                if token.find("DISK") > -1:
                    query_dict = { 'Total' : "ldapsearch -LLL -x -h %s -b mds-vo-name=%s,o=grid -o nettimeout=10\
                                              '(&(objectClass=GlueSA)(|(GlueSALocalID=%s*)(GlueSALocalID=atlas:%s*)))' \
                                              GlueSATotalOnlineSize | grep GlueSATotalOnlineSize: | cut -d\":\" -f2" \
                                              % (sites.atlas_site_bdiis[site],site,token,token),
                                   'Free'  : "ldapsearch -LLL -x -h %s -b mds-vo-name=%s,o=grid -o nettimeout=10\
                                              '(&(objectClass=GlueSA)(|(GlueSALocalID=%s*)(GlueSALocalID=atlas:%s*)))' \
                                              GlueSAFreeOnlineSize | grep GlueSAFreeOnlineSize: | cut -d\":\" -f2" \
                                              %(sites.atlas_site_bdiis[site],site,token,token)
                              }
                if token.find("TAPE") > -1:
                    if site in t1_list:
                        query_dict = { 'Total' : "ldapsearch -LLL -x -h %s -b mds-vo-name=%s,o=grid -o nettimeout=10\
                                                  '(&(objectClass=GlueSA)(|(GlueSALocalID=%s*)(GlueSALocalID=atlas:%s*)))' \
                                                  GlueSATotalNearlineSize | grep GlueSATotalNearlineSize: \
                                                  | cut -d\":\" -f2" \
                                                  % (sites.atlas_site_bdiis[site],site,token,token),
                                       'Free'  : "ldapsearch -LLL -x -h %s -b mds-vo-name=%s,o=grid -o nettimeout=10\
                                                  '(&(objectClass=GlueSA)(|(GlueSALocalID=%s*)(GlueSALocalID=atlas:%s*)))' \
                                                  GlueSAFreeNearlineSize | grep GlueSAFreeNearlineSize: | cut -d\":\" -f2" \
                                                  %(sites.atlas_site_bdiis[site],site,token,token)
                                     }
                    else:
                        query_dict = {}

                for query in query_dict.keys():
                    #print "%s executing query %s for %s" % (site,query,token)
                    p = subprocess.Popen(query_dict[query], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    results = p.communicate()
                    full_text=results[0].strip()
                    index1=full_text.find("Error:")
                    index2=full_text.find("UNKNOWN:")
                    index3=full_text.find("Can't contact")   
                    index4=full_text.find("No such object")   
                    if (index1 > -1) or (index2 > -1) or (index3 > -1) or (index4 > -1):  
                        bdii_dict[site][token]['color'] = "grey"
                        bdii_dict[site][token][query] = "Unreachable"
                    elif ( full_text == ""):
                        bdii_dict[site][token]['color'] = "pink"
                        bdii_dict[site][token][query] = "No_such_token"
                    else: 
                        bdii_dict[site][token]['color'] = "yellow"
                        if full_text.find("\n") > -1:
                            output = "%s: Token %s exists in more than one SE\n" % (site,token)
                            os.write(log_fd,output) 
                            values=full_text.split("\n")
                            total = 0 
                            for value in values:  
                                total = total + int(value) 
                            full_text = total   
                        bdii_dict[site][token][query] = int(full_text)/1000

        else:
            output = "%s not in BDII list\n" % (site)
            os.write(log_fd,output)                 

site_token_ddmendpoint_to_dict()
site_srm_storage_xml_to_dict()
site_bdii_storage_to_dict()

dt=datetime.datetime.now()

for site in sorted(srm_dict.keys()):
    for token in ["ATLASDATADISK", "ATLASPRODDISK", "ATLASSCRATCHDISK", "ATLASLOCALGROUPDISK", "ATLASGROUPDISK", \
                  "ATLASHOTDISK", "ATLASDATATAPE", "ATLASMCTAPE" ]:
        if site in bdii_dict:
            if ( bdii_dict[site][token]['color'] == "yellow" ) and ( srm_dict[site][token]['color'] == "green" ):
                if ( bdii_dict[site][token]["Total"] == srm_dict[site][token]["Total"] ):
                    output = "OK=>BDII:%s==>SRM=%s" % (bdii_dict[site][token]["Total"],srm_dict[site][token]["Total"])
                    result_string="%s %s_%s %s %s %s\n" % (dt,site,token,output,"green","None")
                    print "%s_%s: %s" % (site,token,output)  
                else:
                    output = "ERROR=>BDII:%s==>SRM=%s" % (bdii_dict[site][token]["Total"],srm_dict[site][token]["Total"])
                    result_string="%s %s_%s %s %s %s\n" % (dt,site,token,output,"red","None")
                    print "%s_%s: %s" % (site,token,output)
                os.write(total_fd,result_string)
                if ( bdii_dict[site][token]["Free"] == srm_dict[site][token]["Free"] ):
                    output = "OK=>BDII:%s==>SRM=%s" % (bdii_dict[site][token]["Free"],srm_dict[site][token]["Free"])
                    result_string="%s %s_%s %s %s %s\n" % (dt,site,token,output,"green","None")
                    print "%s_%s: %s" % (site,token,output)
                else:
                    output = "ERROR=>BDII:%s==>SRM=%s" % (bdii_dict[site][token]["Free"],srm_dict[site][token]["Free"])
                    result_string="%s %s_%s %s %s %s\n" % (dt,site,token,output,"red","None")
                    print "%s_%s: %s" % (site,token,output)
                os.write(free_fd,result_string)
            else:
                if ( bdii_dict[site][token]['color'] == "grey" ):
                    output = "BDII_unavailable"
                    result_string="%s %s_%s %s %s %s\n" % (dt,site,token,output,"grey","None")
                    #print "%s_%s: %s" % (site,token,output)
                    os.write(total_fd,result_string)
                    os.write(free_fd,result_string)
                #if ( srm_dict[site][token]['color'] == "pink" ):
                #   print "%s : No such token %s defined in SRM" % (site, token)
                #if ( bdii_dict[site][token]['color'] == "pink" ):
                #   output = "BDII_no_such_token"
                #   result_string="%s %s_%s %s %s %s\n" % (dt,site,token,output,"pink","None")
                #   print "%s_%s: %s" % (site,token,output)
        else:
            output = "%s : BDII not defined\n" % (site)
            os.write(log_fd,output)
 

os.close(log_fd)
os.close(free_fd)
os.close(total_fd)

