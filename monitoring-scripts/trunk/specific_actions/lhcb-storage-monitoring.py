#!/usr/bin/python
#
# Script to monitor Tier 1 Storage Capacity for LHCb sites
#
###############################################################

import subprocess
import urllib
import os, sys
import datetime
from cStringIO import StringIO
from xml.dom import minidom
import ggus_monitor

site_bdiis = {
"CERN-PROD"  : "prod-bdii.cern.ch",
"CERN-EOS"   : "prod-bdii.cern.ch",
"FZK-LCG2"   : "giis-fzk.gridka.de",
"IN2P3-CC"   : "cclcgip03.in2p3.fr",
"INFN-T1"    : "sg01-lcg.cr.cnaf.infn.it",
"RAL-LCG2"   : "site-bdii.gridpp.rl.ac.uk",
"SARA-MATRIX": "sitebdii.grid.sara.nl",
"pic"        : "site-bdii.pic.es"
}

schema_version = {
"CERN-PROD"  : "1",
"CERN-EOS"   : "1",
"FZK-LCG2"   : "2",
"IN2P3-CC"   : "1",
"INFN-T1"    : "1",
"RAL-LCG2"   : "1",
"SARA-MATRIX": "1",
"pic"        : "2"
}

storage_dict = {
"Disk" : {
"CERN-PROD"   : { "BDII" :   { "Total" : 0,  "Used" : 0 }, 
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"CERN-EOS"    : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"FZK-LCG2"    : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"IN2P3-CC"    : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"INFN-T1"     : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"RAL-LCG2"    : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"SARA-MATRIX" : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"pic"         : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
},
"Tape" : {
"CERN-PROD"   : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"CERN-EOS"    : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"FZK-LCG2"    : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"IN2P3-CC"    : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"INFN-T1"     : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"RAL-LCG2"    : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"SARA-MATRIX" : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"pic"         : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
},
"USER" : {
"CERN-PROD"   : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"CERN-EOS"    : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"FZK-LCG2"    : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"IN2P3-CC"    : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"INFN-T1"     : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"RAL-LCG2"    : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"SARA-MATRIX" : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
"pic"         : { "BDII" :   { "Total" : 0,  "Used" : 0 },
                  "SRM"  :   { "Total" : 0,  "Used" : 0 },
                  "Result" : { "Total" : "", "Used" : ""}},
}
}

id_dict = {
"CERN-PROD": { "Disk" : "CASTORLHCBLHCBDISK", "Tape" : "CASTORLHCBLHCBTAPE", "USER" : "CASTORLHCBLHCBUSER" }, 
"CERN-EOS" : { "Disk" : "LHCbEOS", "Tape" : "None", "USER" : "None" },
"FZK-LCG2": { "Disk" : "LHCb-Disk", "Tape" : "LHCb-Tape", "USER" : "LHCb_USER" },
"IN2P3-CC": { "Disk" : "lhcb:LHCb-Disk", "Tape" : "lhcb:LHCb-Tape", "USER" : "lhcb:LHCb_USER" },
"INFN-T1": { "Disk" : "lhcb_disk:replica:online", "Tape" : "lhcb_tape:custodial:nearline", 
             "USER" : "lhcb_user:replica:online" },
"RAL-LCG2": { "Disk" : "lhcbRawRdst", "Tape" : "lhcbDst", "USER" : "lhcbUser" },
"SARA-MATRIX": { "Disk" : "lhcb:LHCb-Disk", "Tape" : "lhcb:LHCb-Tape", "USER" : "lhcb:LHCb_USER" },
"pic": { "Disk" : "LHCb-Disk", "Tape" : "LHCb-Tape", "USER" : "LHCb_USER" }
}

color_code = {
"red" : "ERROR",
"green" : "OK",
"grey" : "Unreachable",
"pink" : "Missing_LHCb_shares",
"yellow" : "Unable_to_use_BDII_data"
}

lhcb_names_dict = {
"CERN-PROD": "CERN",
"CERN-EOS" : "CERN-EOS",
"FZK-LCG2": "GRIDKA",
"IN2P3-CC": "IN2P3",
"INFN-T1": "CNAF",
"RAL-LCG2": "RAL",
"SARA-MATRIX": "SARA",
"pic": "PIC"
}

storage_type_dict = {
"Disk" : "LHCb-Disk",
"Tape" : "LHCb-Tape",
"USER" : "LHCb_USER"
}

base_xml_url = "http://lhcb-web-dirac.cern.ch/sls/storage_space/"

path_to_output = "/afs/cern.ch/user/m/malandes/www/web/ssb/lhcb/storage"
results_disk_total = "%s/lhcb_storage_disk-total.txt" % (path_to_output)
results_disk_used = "%s/lhcb_storage_disk-used.txt" % (path_to_output)
results_tape_total = "%s/lhcb_storage_tape-total.txt" % (path_to_output)
results_tape_used = "%s/lhcb_storage_tape-used.txt" % (path_to_output)
results_user_total = "%s/lhcb_storage_user-total.txt" % (path_to_output)
results_user_used = "%s/lhcb_storage_user-used.txt" % (path_to_output)
fh_disk_total=os.open(results_disk_total, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
fh_disk_used=os.open(results_disk_used, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
fh_tape_total=os.open(results_tape_total, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
fh_tape_used=os.open(results_tape_used, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
fh_user_total=os.open(results_user_total, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
fh_user_used=os.open(results_user_used, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)

results_dict = {
"Disk" : { "Total" : fh_disk_total, "Used" : fh_disk_used },
"Tape" : { "Total" : fh_tape_total, "Used" : fh_tape_used },
"USER" : { "Total" : fh_user_total, "Used" : fh_user_used },
}


# Parsing the SRM information from the XML files provided by LHCb

for site_name in lhcb_names_dict.keys():

    for storage_type in storage_type_dict.keys():
        if (site_name == "CERN-EOS") and (storage_type == "Disk"):
            xml_file_name = "%sCERN_LHCb-EOS.xml" % (base_xml_url)
        else:
            xml_file_name = "%s%s_%s.xml" % (base_xml_url,lhcb_names_dict[site_name],storage_type_dict[storage_type])
        tree = minidom.parse(urllib.urlopen(xml_file_name))
        for subelement in tree.getElementsByTagName('numericvalue'):
            if (subelement.attributes['name'].value == "Total space"):
                storage_dict[storage_type][site_name]["SRM"]["Total"]=int(float(subelement.firstChild.nodeValue))
            elif (subelement.attributes['name'].value == "Occupied space"):
                storage_dict[storage_type][site_name]["SRM"]["Used"]=int(float(subelement.firstChild.nodeValue))

# Getting the BDII information querying the site BDII

for site_name in sorted(site_bdiis.keys()):

    #print ("%s ------>") % (site_name)
    site_name_query = site_name
    if (site_name == "CERN-EOS"):
        site_name_query = "CERN-PROD"

    dt=datetime.datetime.now()

    for storage_type in storage_type_dict.keys():
        #print ("%s ------>") % (storage_type)
        glue2_query = "ldapsearch -LLL -x -h %s -p 2170 -b GLUE2DomainID=%s,o=glue \
                       '(&(objectClass=GLUE2StorageShareCapacity)\
                          (GLUE2StorageShareCapacityStorageShareForeignKey=*%s*))'\
                           GLUE2StorageShareCapacityTotalSize GLUE2StorageShareCapacityUsedSize\
                       | perl -p00e 's/\r?\n //g' | grep -v dn:" % \
                       (site_bdiis[site_name], site_name_query, id_dict[site_name][storage_type])
        glue1_query = "ldapsearch -LLL -x -h %s -p 2170 -b mds-vo-name=%s,o=grid \
                       '(&(objectClass=GlueSA)(GlueSALocalID=%s))'\
                          GlueSATotalNearlineSize GlueSAUsedNearlineSize \
                          GlueSATotalOnlineSize GlueSAUsedOnlineSize\
                       | perl -p00e 's/\r?\n //g' | grep -v dn:" % \
                       (site_bdiis[site_name], site_name_query, id_dict[site_name][storage_type])     
        if (schema_version[site_name] == "1"):
            p = subprocess.Popen(glue1_query, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            p = subprocess.Popen(glue2_query, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        results = p.communicate()
        full_text=results[0].strip()
        index1=full_text.find("Error:")
        index2=full_text.find("UNKNOWN:")
        index3=full_text.find("error")    # Internal (implementation specific) error (80). See GGUS 101259. 
        if (index1 > -1) or (index2 > -1) or (index3 > -1):
             # Redirect this to StorageT1-storage_type-i.txt
             result_string="%s %s %s %s %s\n" % (dt,lhcb_names_dict[site_name],color_code["grey"],"grey","None") 
             os.write(results_dict[storage_type]["Total"],result_string)
             os.write(results_dict[storage_type]["Used"],result_string)
        elif (results[0] == ""):
             # Redirect this to StorageT1-storage_type-i.txt
             result_string="%s %s %s %s %s\n" % (dt,lhcb_names_dict[site_name],color_code["pink"],"pink","None")
             os.write(results_dict[storage_type]["Total"],result_string)
             os.write(results_dict[storage_type]["Used"],result_string)
        else:
            #print ("--------------------------")
            #print ("%s") % (full_text)
            #print ("--------------------------")
            if (schema_version[site_name] == "1"):
                try:
                    line1,line2,line3,line4=full_text.split("\n")
                    aux_dict={}
                    key1,value1=line1.split(":")
                    aux_dict[key1]=value1 
                    key2,value2=line2.split(":")
                    aux_dict[key2]=value2
                    key3,value3=line3.split(":")
                    aux_dict[key3]=value3
                    key4,value4=line4.split(":")
                    aux_dict[key4]=value4
                    for j in [key1,key2,key3,key4]:
                        if (j.find("Total") > -1) and (aux_dict[j] != 0):
	    	            storage_dict[storage_type][site_name]["BDII"]["Total"]=int(aux_dict[j])/1000		
                        elif (j.find("Used") > -1) and (aux_dict[j] != 0):
                            storage_dict[storage_type][site_name]["BDII"]["Used"]=int(aux_dict[j])/1000
                except ValueError:
                    # Redirect this to StorageT1-storage_type-i.txt
                    result_string="%s %s %s %s %s\n" % (dt,lhcb_names_dict[site_name],color_code["yellow"],"yellow","None")
                    os.write(results_dict[storage_type]["Total"],result_string)
                    os.write(results_dict[storage_type]["Used"],result_string)
            else:
                if ( full_text.count("\n") > 1 ):        # This is for pic case
                    line1,rest=full_text.split("\n",1)
                    line2,_=rest.split("\n",1)
                else:
                    line1,line2=full_text.split("\n") 
                key1,value1=line1.split(":")    
                key2,value2=line2.split(":")    
                if (key1 == "GLUE2StorageShareCapacityTotalSize"):
                    storage_dict[storage_type][site_name]["BDII"]["Total"]=int(value1)/1000
                    storage_dict[storage_type][site_name]["BDII"]["Used"]=int(value2)/1000
                else:
                    storage_dict[storage_type][site_name]["BDII"]["Total"]=int(value2)/1000
                    storage_dict[storage_type][site_name]["BDII"]["Used"]=int(value1)/1000
            for i in ["Total","Used"]:
                extra=""
                if (storage_dict[storage_type][site_name]["BDII"][i] == storage_dict[storage_type][site_name]["SRM"][i]):
                    storage_dict[storage_type][site_name]["Result"][i] = "green"
                else:
                    storage_dict[storage_type][site_name]["Result"][i] = "red"
                extra="=>BDII:%s==>SRM:%s" % (storage_dict[storage_type][site_name]["BDII"][i],\
                                              storage_dict[storage_type][site_name]["SRM"][i])

                # Prepare detailed output information  
                file_name = "%s-%s-%s" % (site_name,storage_type,i)
                file_path = "%s/%s" % (path_to_output,file_name)
                output = os.open (file_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)
                file_url = "http://malandes.web.cern.ch/malandes/ssb/lhcb/storage/%s" % (file_name)
                os.write(output,"BDII numbers:\n") 
                os.write(output,full_text)
                os.close(output)
                # Redirect this to StorageT1-storage_type-i.txt
                result_string="%s %s %s%s %s %s\n" % \
                (dt,lhcb_names_dict[site_name],color_code[storage_dict[storage_type][site_name]["Result"][i]],extra,\
                 storage_dict[storage_type][site_name]["Result"][i],file_url)
                os.write(results_dict[storage_type][i],result_string)
                

os.close(fh_tape_total)
os.close(fh_tape_used)
os.close(fh_disk_total)
os.close(fh_disk_used)
os.close(fh_user_total)
os.close(fh_user_used)

#######################################
# Interacting with GGUS
#######################################

ggus_file_name = "%s/ggus_lhcb_storage.txt" % (path_to_output)
ggus_output = os.open (ggus_file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600)

for site_name in sorted(site_bdiis.keys()):

    site_name_query = site_name
    if (site_name == "CERN-EOS"):
        site_name_query = "CERN-PROD"

    extra_condition = False
    ggus_details = ""
    for storage_type in storage_type_dict.keys():    
        if ( storage_dict[storage_type][site_name]["Result"]["Total"] == "red" ):
            ggus_details = ggus_details + "\nAffected Storage Share: %s \nBDII Total:%s vs SRM Total:%s" % \
                           (id_dict[site_name][storage_type], storage_dict[storage_type][site_name]["BDII"]["Total"],\
                            storage_dict[storage_type][site_name]["SRM"]["Total"])
            extra_condition = True    
        if (storage_dict[storage_type][site_name]["Result"]["Used"] == "red"):
            ggus_details = ggus_details + "\nAffected Storage Share: %s \nBDII Used:%s vs SRM Used:%s" % \
                           (id_dict[site_name][storage_type], storage_dict[storage_type][site_name]["BDII"]["Used"],\
                            storage_dict[storage_type][site_name]["SRM"]["Used"])
            extra_condition = True

    ggus_color, ggus_result, ggus_file_url = ggus_monitor.ggus_monitor(site_name_query, "lhcb-storage", \
                                             ggus_details, extra_condition)
    os.write(ggus_output,"%s %s %s %s %s\n" % (dt,lhcb_names_dict[site_name],ggus_result,ggus_color,ggus_file_url))

os.close(ggus_output)


