#!/usr/bin/python
#
# Script to monitor Storage Capacity (BDII vs SRM) for ATLAS sites
#
###############################################################

import subprocess
import os, sys
import datetime
import time
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
results_ddm = "%s/atlas_storage_ddm.txt" % (path_to_output) 
log_fd = os.open(log_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
free_fd = os.open(results_free, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
total_fd = os.open(results_total, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
ddm_fd = os.open(results_ddm, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)

srm_dict = {}
bdii_dict = {}
token_dict = {}

t1_list = [ 'CERN-PROD', 'BNL-ATLAS', 'FZK-LCG2', 'IN2P3-CC', 'INFN-T1', 'KR-KISTI-GSDC-01', 'NDGF-T1', 'NIKHEF-ELPROD',
            'pic', 'RAL-LCG2', 'SARA-MATRIX', 'Taiwan-LCG2', 'TRIUMF-LCG2', 'USCMS-FNAL-WC1' ]

dt=datetime.datetime.now()

# Parsing the DDM endpoint json file to store token - ddmendpoint relationships
def site_token_ddmendpoint_to_dict ():

    url = "http://atlas-agis-api.cern.ch/request/ddmendpoint/query/list/?json"
    json_file = urllib2.urlopen(url).read()
    ddmendpoints = json.loads(json_file)
    for ddmendpoint in ddmendpoints:
        if ddmendpoint["rc_site"] not in token_dict:
            token_dict[ddmendpoint["rc_site"]] = {}
        se_uniqueid = ddmendpoint["se"].split("/",2)[2].split(":",1)[0]
        token = ddmendpoint["token"]
        key = "%s_%s" % (token,se_uniqueid)
        if key in token_dict[ddmendpoint["rc_site"]]:
            token_dict[ddmendpoint["rc_site"]][key].append(ddmendpoint["name"])
        else:
            token_dict[ddmendpoint["rc_site"]][key] = [ddmendpoint["name"]] 
    #pprint (token_dict)         

# Parsing the SRM information from the XML files provided by ATLAS DDM endpoints
def site_srm_storage_xml_to_dict ():

    for site in sorted(token_dict.keys()):
        srm_dict[site] = {} 
        for key in token_dict[site]:
            srm_dict[site][key] = { "Total" : 0, "Free" : 0, "color" : "" }
            for ddmendpoint in token_dict[site][key]:
                #print "%s/%s.xml" % (base_xml_url,ddmendpoint)
                xml_file_name = "%s/%s.xml" % (base_xml_url,ddmendpoint)
                try:
                    xml_file = urllib2.urlopen(xml_file_name)
                    last_modified = datetime.datetime(*(time.strptime(xml_file.headers.dict['last-modified'],"%a, %d %b %Y %H:%M:%S GMT")[0:6])) 
                    margin = datetime.timedelta(days=2)
                    if last_modified.timetuple() < (dt - margin).timetuple():
                        output = "XML_older_than_2_days"
                        result_string="%s %s_%s %s %s %s\n" % (dt,site,key,output,"grey","None")
                        os.write(total_fd,result_string)
                        os.write(free_fd,result_string)
                    else: 
                        tree = minidom.parse(xml_file)
                        for subelement in tree.getElementsByTagName('numericvalue'):
                            if (subelement.attributes['name'].value == "Total space"):
                                srm_dict[site][key]["Total"] = int(float(subelement.firstChild.nodeValue))
                            elif (subelement.attributes['name'].value == "Free space"):
                                srm_dict[site][key]["Free"] = int(float(subelement.firstChild.nodeValue))
                        srm_dict[site][key]['color'] = "green"
                except urllib2.HTTPError:
                    output = "XML_does_not_exist" 
                    result_string="%s %s_%s %s %s %s\n" % (dt,site,key,output,"grey","None")
                    os.write(total_fd,result_string)    
                    os.write(free_fd,result_string)    
    #pprint (srm_dict)

# get storage capacities from BDII
def site_bdii_storage_to_dict ():

    for site in sorted(srm_dict.keys()):
        bdii_dict[site] = {}
        for key in srm_dict[site]:
            bdii_dict[site][key] = { "Total" : 0, "Free" : 0, "color" : "" }
            token,se_uniqueid = key.split("_",1) 
            if site in sites.atlas_site_bdiis:
                if token.find("DISK") > -1:
                    query_dict = { 'Total' : "ldapsearch -LLL -x -h %s -b mds-vo-name=%s,o=grid -o nettimeout=10 \
                                              '(&(objectClass=GlueSA)(GlueChunkKey=GlueSEUniqueID=%s) \
                                              (|(GlueSALocalID=%s)(GlueSALocalID=%s:*)(GlueSALocalID=atlas:%s)))' \
                                              GlueSATotalOnlineSize | grep GlueSATotalOnlineSize: | cut -d\":\" -f2" \
                                              % (sites.atlas_site_bdiis[site],site,se_uniqueid,token,token,token),
                                   'Free'  : "ldapsearch -LLL -x -h %s -b mds-vo-name=%s,o=grid -o nettimeout=10 \
                                              '(&(objectClass=GlueSA)(GlueChunkKey=GlueSEUniqueID=%s) \
                                              (|(GlueSALocalID=%s)(GlueSALocalID=%s:*)(GlueSALocalID=atlas:%s)))' \
                                              GlueSAFreeOnlineSize | grep GlueSAFreeOnlineSize: | cut -d\":\" -f2" \
                                              %(sites.atlas_site_bdiis[site],site,se_uniqueid,token,token,token)
                              }
                if token.find("TAPE") > -1:
                    if site in t1_list:
                        query_dict = { 'Total' : "ldapsearch -LLL -x -h %s -b mds-vo-name=%s,o=grid -o nettimeout=10 \
                                                  '(&(objectClass=GlueSA)(GlueChunkKey=GlueSEUniqueID=%s) \
                                                  (|(GlueSALocalID=%s)(GlueSALocalID=%s:*)(GlueSALocalID=atlas:%s)))' \
                                                  GlueSATotalNearlineSize GlueSATotalOnlineSize | grep GlueSATotal" \
                                                  % (sites.atlas_site_bdiis[site],site,se_uniqueid,token,token,token),
                                       'Free'  : "ldapsearch -LLL -x -h %s -b mds-vo-name=%s,o=grid -o nettimeout=10 \
                                                  '(&(objectClass=GlueSA)(GlueChunkKey=GlueSEUniqueID=%s) \
                                                  (|(GlueSALocalID=%s)(GlueSALocalID=%s:*)(GlueSALocalID=atlas:%s)))' \
                                                  GlueSAFreeNearlineSize GlueSAFreeOnlineSize | grep GlueSAFree" \
                                                  %(sites.atlas_site_bdiis[site],site,se_uniqueid,token,token,token)
                                     }
                    else:
                        query_dict = {}

                for query in query_dict.keys():
                    #print "%s executing query %s for %s" % (site,query,key)
                    p = subprocess.Popen(query_dict[query], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    results = p.communicate()
                    full_text=results[0].strip()
                    index1=full_text.find("Error:")
                    index2=full_text.find("UNKNOWN:")
                    index3=full_text.find("Can't contact")   
                    index4=full_text.find("No such object")   
                    if (index1 > -1) or (index2 > -1) or (index3 > -1) or (index4 > -1):  
                        bdii_dict[site][key]['color'] = "grey"
                        bdii_dict[site][key][query] = "Unreachable"
                    elif ( full_text == ""):
                        bdii_dict[site][key]['color'] = "pink"
                        bdii_dict[site][key][query] = "No_such_SE_token"
                    else:
                        bdii_dict[site][key]['color'] = "yellow"
                        if token.find("TAPE") > -1:
                            size1,size2 = full_text.split("\n")
                            size1_attr,size1_value = size1.split(":")
                            size2_attr,size2_value = size2.split(":") 
                            size1_value = size1_value.strip()
                            size2_value = size2_value.strip()
                            if size1_attr.find("NearlineSize") > -1: 
                                if size1_value == "0":
                                    bdii_dict[site][key][query] = int(size2_value)/1000
                                else:
                                    bdii_dict[site][key][query] = int(size1_value)/1000 
                            else:
                                if size2_value == "0":
                                    bdii_dict[site][key][query] = int(size1_value)/1000
                                else:
                                    bdii_dict[site][key][query] = int(size2_value)/1000
                        else: 
                            bdii_dict[site][key][query] = int(full_text)/1000

            else:
                bdii_dict[site][key]['color'] = "orange"
                bdii_dict[site][key]["Total"] = "No_BDII_defined" 
                bdii_dict[site][key]["Free"] = "No_BDII_defined" 

    #pprint (bdii_dict)

site_token_ddmendpoint_to_dict()
site_srm_storage_xml_to_dict()
site_bdii_storage_to_dict()

dt=datetime.datetime.now()

for site in sorted(srm_dict.keys()):
    for token in srm_dict[site]:
        if site in bdii_dict:
            if ( bdii_dict[site][token]['color'] == "yellow" ) and ( srm_dict[site][token]['color'] == "green" ):
                if ( abs ( bdii_dict[site][token]["Total"] - srm_dict[site][token]["Total"] ) <= 1 ):
                    output = "OK=>BDII:%s==>SRM=%s" % (bdii_dict[site][token]["Total"],srm_dict[site][token]["Total"])
                    result_string="%s %s_%s %s %s %s\n" % (dt,site,token,output,"green","None")
                    #print "%s_%s: %s" % (site,token,output)  
                else:
                    output = "ERROR=>BDII:%s==>SRM=%s" % (bdii_dict[site][token]["Total"],srm_dict[site][token]["Total"])
                    result_string="%s %s_%s %s %s %s\n" % (dt,site,token,output,"red","None")
                    #print "%s_%s: %s" % (site,token,output)
                os.write(total_fd,result_string)
                if ( abs ( bdii_dict[site][token]["Free"] - srm_dict[site][token]["Free"] ) <= 1 ):
                    output = "OK=>BDII:%s==>SRM=%s" % (bdii_dict[site][token]["Free"],srm_dict[site][token]["Free"])
                    result_string="%s %s_%s %s %s %s\n" % (dt,site,token,output,"green","None")
                    #print "%s_%s: %s" % (site,token,output)
                else:
                    output = "ERROR=>BDII:%s==>SRM=%s" % (bdii_dict[site][token]["Free"],srm_dict[site][token]["Free"])
                    result_string="%s %s_%s %s %s %s\n" % (dt,site,token,output,"red","None")
                    #print "%s_%s: %s" % (site,token,output)
                os.write(free_fd,result_string)
            else:
                if ( bdii_dict[site][token]['color'] == "grey" ):
                    output = "BDII_unavailable"
                    result_string="%s %s_%s %s %s %s\n" % (dt,site,token,output,"grey","None")
                    #print "%s_%s: %s" % (site,token,output)
                    os.write(total_fd,result_string)
                    os.write(free_fd,result_string)
                elif ( bdii_dict[site][token]['color'] == "pink" ):
                    output = "No_such_SE_token"
                    result_string="%s %s_%s %s %s %s\n" % (dt,site,token,output,"pink","None")
                    #print "%s_%s: %s" % (site,token,output)
                    os.write(total_fd,result_string)
                    os.write(free_fd,result_string)
                elif (bdii_dict[site][token]['color'] == "orange" ):
                    output = "No_BDII_defined"
                    result_string="%s %s_%s %s %s %s\n" % (dt,site,token,output,"orange","None")
                    #print "%s_%s: %s" % (site,token,output)
                    os.write(free_fd,result_string)
                    os.write(total_fd,result_string)

        list=""
        elems=len(token_dict[site][token])
        count=1 
        for ddmendpoint in token_dict[site][token]:
            site_string = "%s_" % (site)
            ddmendpoint_name = ddmendpoint.replace(site_string,"")
            if ( count == elems ):
                list += "%s" % (ddmendpoint_name)
            else:
                list += "%s," % (ddmendpoint_name)
            count += 1
        result_string="%s %s_%s %s %s %s\n" % (dt,site,token,list,"yellow","None") 
        os.write(ddm_fd,result_string)  

os.close(log_fd)
os.close(free_fd)
os.close(total_fd)
os.close(ddm_fd)

