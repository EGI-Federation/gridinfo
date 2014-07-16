#!/usr/bin/python
#
# Script to monitor T1 Storage per VO
#
###############################################################

import subprocess
import os, sys
import datetime
from cStringIO import StringIO
import fileinput

path_to_output = "/afs/cern.ch/user/m/malandes/www/web/ssb/wlcg/t1-storage"
path_to_url = "http://malandes.web.cern.ch/malandes/ssb/wlcg/t1-storage" 
dt=datetime.datetime.now()
today=datetime.date.today()


test_list = [ 'vos', 'storage_version', 'storage_type' ]
 
t1_list = [ 'CERN-PROD', 'BNL-ATLAS', 'FZK-LCG2', 'IN2P3-CC', 'INFN-T1', 'KR-KISTI-GSDC-01', 'NDGF-T1', 'NIKHEF-ELPROD',
            'pic', 'RAL-LCG2', 'SARA-MATRIX', 'Taiwan-LCG2', 'TRIUMF-LCG2', 'USCMS-FNAL-WC1' ]

for test in test_list:

    output_file_name = "%s/%s.txt" % (path_to_output,test)
    output_fd = os.open (output_file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600) 

    for t1 in t1_list:
        #print t1

        se_list = "ldapsearch -x -LLL -h lcg-bdii:2170 -b mds-vo-name=%s,mds-vo-name=local,o=grid \
                   '(objectClass=GlueSE)' GlueSEUniqueID | grep GlueSEUniqueID: | cut -d\":\" -f2 \
                   | cut -d\"=\" -f2 | sort | uniq" % (t1)

        p =  subprocess.Popen(se_list, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        results = p.communicate()
        if ( results[0].find("Error") > -1 or results[0].find("UNKNOWN") > -1 or results[0].find("No such object") > -1 ):
            se_lhc = ""
            color = "grey"
            result = "Unreachable"
            result_string = "%s %s-%s %s %s %s\n" % (dt,t1,se_lhc,result,color,detail_url)
            os.write(output_fd,result_string)
        else:
            se_list = results[0].strip() 
            for se in se_list.split():
                
                if ( se != "BNL-ATLAS_classicSE") and ( se != "USCMS-FNAL-WC1_classicSE"):  
  
                    se_lhc_list = "ldapsearch -x -LLL -h lcg-bdii:2170 -b mds-vo-name=%s,mds-vo-name=local,o=grid \
                                   '(&(objectClass=GlueSA)(GlueChunkKey=GlueSEUniqueID=%s)\
                                   (|(GlueSAAccessControlBaseRule=*atlas*)(GlueSAAccessControlBaseRule=*cms*)\
                                   (GlueSAAccessControlBaseRule=*lhcb*)(GlueSAAccessControlBaseRule=*alice*)))' \
                                   GlueChunkKey | grep GlueChunkKey: | cut -d\":\" -f2 | cut -d\"=\" -f2 | sort | uniq" \
                                   % (t1,se)
               
                    p =  subprocess.Popen(se_lhc_list, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    results = p.communicate()
                    if ( results[0].find("Error") > -1 or results[0].find("UNKNOWN") > -1 or \
                         results[0].find("No such object") > -1):
                        se_lhc = ""
                        color = "grey"
                        result = "Unreachable"
                        result_string = "%s %s-%s %s %s %s\n" % (dt,t1,se_lhc,result,color,detail_url)
                        os.write(output_fd,result_string)
                    else:
                        se_lhc_list = results[0].strip()
                        for se_lhc in se_lhc_list.split():
                            vos = "ldapsearch -x -LLL -h lcg-bdii:2170 -b mds-vo-name=%s,mds-vo-name=local,o=grid \
                                   '(&(objectClass=GlueSA)(GlueChunkKey=GlueSEUniqueID=%s)\
                                   (|(GlueSAAccessControlBaseRule=*atlas*)(GlueSAAccessControlBaseRule=*cms*)\
                                   (GlueSAAccessControlBaseRule=*lhcb*)(GlueSAAccessControlBaseRule=*alice*)))' \
                                   GlueSAAccessControlBaseRule | grep GlueSAAccessControlBaseRule: | cut -d\":\" -f3 \
                                   | sort | uniq | grep 'atlas\|alice\|cms\|lhcb' | tr '\n' '-'" % (t1,se_lhc)            
                            storage_version = "ldapsearch -x -LLL -h lcg-bdii:2170 \
                                               -b mds-vo-name=%s,mds-vo-name=local,o=grid \
                                               \"(&(objectClass=GlueSE)(GlueSEUniqueID=%s))\" \
                                               GlueSEImplementationVersion | grep GlueSEImplementationVersion: \
                                               | cut -d\":\" -f2-" % (t1,se_lhc)
                            storage_type = "ldapsearch -x -LLL -h lcg-bdii:2170 -b mds-vo-name=%s,mds-vo-name=local,o=grid \
                                            \"(&(objectClass=GlueSE)(GlueSEUniqueID=%s))\" \
                                            GlueSEImplementationName | grep GlueSEImplementationName: | cut -d\":\" -f2" \
                                            % (t1,se_lhc)

                            test_dict = {
                            'vos'              : vos, 
                            'storage_version'  : storage_version,
                            'storage_type'     : storage_type
                            }

                            detail_file_name = "%s/%s/%s-%s.html" % (path_to_output,test,t1,se_lhc)
                            detail_url = "%s/%s/%s-%s.html#%s" % (path_to_url,test,t1,se_lhc,today)

                            p =  subprocess.Popen(test_dict[test] ,shell=True, stdout=subprocess.PIPE, \
                                 stderr=subprocess.STDOUT)
                            results = p.communicate()
                            if ( results[0].find("Error") > -1 or results[0].find("UNKNOWN") > -1 ):
                                color = "grey"
                                result = "Unreachable" 
                            else:
                                color = "green"
                                result = results[0].strip()
                                if ( test == "vos" ):
                                    result_aux = "" 
                                    if (result.find("atlas") > -1 ):
	                                result_aux = "atlas"
                                    if (result.find("alice") > -1 ):
                                        if ( result_aux == ""):
                                            result_aux="alice"
                                        else:
                                            result_aux = "%s-alice" % (result_aux)   
                                    if (result.find("cms") > -1 ):
                                        if ( result_aux == ""):
                                            result_aux="cms"
                                        else:
                                            result_aux = "%s-cms" % (result_aux)   
                                    if (result.find("lhcb") > -1 ):
                                        if ( result_aux == ""):
                                            result_aux="lhcb"
                                        else:
                                            result_aux = "%s-lhcb" % (result_aux)   
                                    result=result_aux 
                                elif ( test == "storage_version" ): 
                                    result_aux = result.replace (" ","_")
                                    result_aux2 = result_aux.replace (":","_") 
                                    result = result_aux2
    
                            #detail_result_string="<a name=\"%s\">%s: %s</a><br>\n</body></html>" % (today,today,result)
                            #for line in fileinput.input(detail_file_name, inplace=True): 
                            #    sys.stdout.write(line.replace('</body></html>', detail_result_string))
                            result_string = "%s %s-%s %s %s %s\n" % (dt,t1,se_lhc,result,color,detail_url)
                            os.write(output_fd,result_string)

    os.close(output_fd)
