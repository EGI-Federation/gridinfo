#!/usr/bin/python
#
# Script to monitor GLUE 1 and GLUE 2 Storage deployment
# for DPM, dCache, StoRM, Castor and EOS
#
###############################################################

import subprocess
import os, sys
import datetime
from cStringIO import StringIO
import fileinput

path_to_output = "/afs/cern.ch/user/m/malandes/www/web/ssb/general/glue-per-se"
path_to_url = "http://malandes.web.cern.ch/malandes/ssb/general/glue-per-se" 
dt=datetime.datetime.now()
today=datetime.date.today()

test_list = [ 'glue1_storage_online', 'glue1_storage_nearline', 'glue2_storage_online', 'glue2_storage_nearline', \
              'glue2_storage_endpoints', \
              'glue1_storage_instances', 'glue2_storage_instances', 'glue1_storage_sites', 'glue2_storage_sites' ]

se_list = [ 'DPM', 'StoRM', 'dCache', 'castor', 'eos' ]

storage_manager_dict = {
'DPM'    : 'DPM',
'StoRM'  : 'storm-backend-server',
'dCache' : 'dCache',
'castor' : 'castor',
'eos'    : 'eos' 
}

glue2_storage_endpoints = {
'DPM'    : 'ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
           \'(&(objectClass=GLUE2Endpoint)(|(GLUE2EndpointImplementationName=DPM)(!(GLUE2EndpointImplementationName=*))))\' \
           dn | grep dn: | wc -l',
'StoRM'  : 'ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
            \'(&(objectClass=GLUE2Endpoint)(GLUE2EndpointImplementationName=StoRM))\' \
            dn | grep dn: | wc -l', 
'dCache' : 'ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
            \'(&(objectClass=GLUE2Endpoint)(GLUE2EndpointImplementationName=dCache))\' \
            dn | grep dn: | wc -l',
'castor' : 'ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
            \'(&(objectClass=GLUE2Endpoint)(GLUE2EndpointImplementationName=castor))\' \
            dn | grep dn: | wc -l',
'eos'    : 'ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
            \'(&(objectClass=GLUE2Endpoint)(GLUE2EndpointImplementationName=eos))\' \
            dn | grep dn: | wc -l'
}

glue2_storage_capacity_dict = {
'DPM_online'    : 'for i in `ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
                  \'(&(objectClass=GLUE2Service)(|(GLUE2ServiceType=DPM)(GLUE2ServiceType=Storage)))\' \
                  GLUE2ServiceID | grep GLUE2ServiceID: | cut -d":" -f2`; \
                  do ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
                  "(&(objectClass=GLUE2StorageServiceCapacity)(GLUE2StorageServiceCapacityStorageServiceForeignKey=$i))" \
                  GLUE2StorageServiceCapacityTotalSize | grep GLUE2StorageServiceCapacityTotalSize: | cut -d":" -f2; done | \
                  awk \'{sum+=$1} END {print sum/1000000}\'',
'DPM_nearline'  : "NA",
'StoRM_online'  :  'for i in `ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
                    \'(&(objectClass=GLUE2Service)(GLUE2ServiceType=SRM))\' \
                    GLUE2ServiceID | grep GLUE2ServiceID: | cut -d":" -f2-`;  \
                    do ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
                    "(&(objectClass=GLUE2StorageServiceCapacity)(GLUE2StorageServiceCapacityType=online)\
                    (GLUE2StorageServiceCapacityStorageServiceForeignKey=$i*))" \
                    GLUE2StorageServiceCapacityTotalSize | grep GLUE2StorageServiceCapacityTotalSize: | cut -d":" -f2; \
                    done | awk \'{sum+=$1} END {print sum/1000000}\'',
'StoRM_nearline':  'for i in `ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
                    \'(&(objectClass=GLUE2Service)(GLUE2ServiceType=SRM))\' \
                    GLUE2ServiceID | grep GLUE2ServiceID: | cut -d":" -f2-`;  \
                    do ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
                    "(&(objectClass=GLUE2StorageServiceCapacity)(GLUE2StorageServiceCapacityType=nearline)\
                    (GLUE2StorageServiceCapacityStorageServiceForeignKey=$i*))" \
                    GLUE2StorageServiceCapacityTotalSize | grep GLUE2StorageServiceCapacityTotalSize: | cut -d":" -f2; \
                    done | awk \'{sum+=$1} END {print sum/1000000}\'',
'dCache_online' :  'for i in `ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
                    \'(&(objectClass=GLUE2Service)(GLUE2ServiceType=org.dcache.storage))\' \
                    GLUE2ServiceID | grep GLUE2ServiceID: | cut -d":" -f2-`; \
                    do ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
                    "(&(objectClass=GLUE2StorageServiceCapacity)(GLUE2StorageServiceCapacityType=online)\
                    (GLUE2StorageServiceCapacityStorageServiceForeignKey=$i))" \
                    GLUE2StorageServiceCapacityTotalSize | grep GLUE2StorageServiceCapacityTotalSize: | cut -d":" -f2; \
                    done | awk \'{sum+=$1} END {print sum/1000000}\'',
'dCache_nearline':  'for i in `ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
                    \'(&(objectClass=GLUE2Service)(GLUE2ServiceType=org.dcache.storage))\' \
                    GLUE2ServiceID | grep GLUE2ServiceID: | cut -d":" -f2-`; \
                    do ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
                    "(&(objectClass=GLUE2StorageServiceCapacity)(GLUE2StorageServiceCapacityType=nearline)\
                    (GLUE2StorageServiceCapacityStorageServiceForeignKey=$i))" \
                    GLUE2StorageServiceCapacityTotalSize | grep GLUE2StorageServiceCapacityTotalSize: | cut -d":" -f2; \
                    done | awk \'{sum+=$1} END {print sum/1000000}\'',
'castor_online'  : 'echo "NA"',
'castor_nearline': 'for i in `ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
                    \'(&(objectClass=GLUE2Service)(GLUE2ServiceType=castor))\' \
                    GLUE2ServiceID | grep GLUE2ServiceID: | cut -d":" -f2-`; \
                    do ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
                    "(&(objectClass=GLUE2StorageServiceCapacity)(GLUE2StorageServiceCapacityType=nearline)\
                    (GLUE2StorageServiceCapacityStorageServiceForeignKey=$i))" \
                    GLUE2StorageServiceCapacityTotalSize | grep GLUE2StorageServiceCapacityTotalSize: | cut -d":" -f2; \
                    done | awk \'{sum+=$1} END {print sum/1000000}\'',
'eos_online'     : 'for i in `ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
                    \'(&(objectClass=GLUE2Service)(GLUE2ServiceType=eos))\' \
                    GLUE2ServiceID | grep GLUE2ServiceID: | cut -d":" -f2-`; \
                    do ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
                    "(&(objectClass=GLUE2StorageServiceCapacity)(GLUE2StorageServiceCapacityType=online)\
                    (GLUE2StorageServiceCapacityStorageServiceForeignKey=$i))" \
                    GLUE2StorageServiceCapacityTotalSize | grep GLUE2StorageServiceCapacityTotalSize: | cut -d":" -f2; \
                    done | awk \'{sum+=$1} END {print sum/1000000}\'',
'eos_nearline'   : 'echo "NA"'
}

for test in test_list:
    output_file_name = "%s/%s.txt" % (path_to_output,test)
    output_fd = os.open (output_file_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0600) 

    for se in se_list:
        glue1_storage_online = "ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=grid \
                                 \"(&(objectClass=GlueSE)(GlueSEImplementationName=%s))\" GlueSETotalOnlineSize \
                                 | grep GlueSETotalOnlineSize: | cut -d\":\" -f2 \
                                 | awk '{sum+=$1} END {print sum/1000000}'" \
                                 % (se) 
        glue1_storage_nearline = "ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=grid \
                                  \"(&(objectClass=GlueSE)(GlueSEImplementationName=%s))\" GlueSETotalNearlineSize \
                                  | grep GlueSETotalNearlineSize: | cut -d\":\" -f2 \
                                  | awk '{sum+=$1} END {print sum/1000000}'" \
                                  % (se)
        glue1_storage_instances = "ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=grid \
                                   \'(&(objectClass=GlueSE)(GlueSEImplementationName=%s))\' \
                                   GlueSEImplementationName | grep GlueSEImplementationName: | wc -l" % (se)
        glue2_storage_instances = "ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
                                   \'(&(objectClass=GLUE2StorageManager)(GLUE2ManagerProductName=%s))\' \
                                   GLUE2ManagerProductName | grep GLUE2ManagerProductName: | wc -l" \
                                   % (storage_manager_dict[se])
        glue1_storage_sites = "ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=grid \
                               \'(&(objectClass=GlueSE)(GlueSEImplementationName=%s))\' \
                               GlueForeignKey | grep GlueForeignKey: | sort | uniq | wc -l" % (se)

        glue2_storage_sites = "ldapsearch -h lcg-bdii -p 2170 -x -LLL -b o=glue \
                               \'(&(objectClass=GLUE2StorageManager)(GLUE2ManagerProductName=%s))\' \
                               dn | perl -p00e \'s/\\r?\\n //g\'  | grep dn: | awk -F \"=\" \'{print $(NF-2) }\' \
                               | sort | uniq | wc -l" % (storage_manager_dict[se])

        se_online = "%s_online" % (se) 
        se_nearline = "%s_nearline" % (se) 

        test_dict = {
        'glue1_storage_online'           :  glue1_storage_online,
        'glue1_storage_nearline'         :  glue1_storage_nearline,
        'glue2_storage_online'           :  glue2_storage_capacity_dict[se_online],
        'glue2_storage_nearline'         :  glue2_storage_capacity_dict[se_nearline],
        'glue2_storage_endpoints'        :  glue2_storage_endpoints[se], 
        'glue1_storage_instances'        :  glue1_storage_instances,
        'glue2_storage_instances'        :  glue2_storage_instances,
        'glue1_storage_sites'            :  glue1_storage_sites,
        'glue2_storage_sites'            :  glue2_storage_sites
        }

        detail_file_name = "%s/%s/%s.html" % (path_to_output,test,se)
        detail_url = "%s/%s/%s.html#%s" % (path_to_url,test,se,today)

        if ( test == 'glue2_storage_capacity'):
           print test_dict[test]
        p = subprocess.Popen(test_dict[test] ,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        results = p.communicate()
        if ( results[0].find("Error") > -1 or results[0].find("UNKNOWN") > -1  or \
             results[0].find("Can't contact") > -1):
            color = "grey"
            result = "Unreachable"
        elif ( results[0].find("NA") > -1 ):
            color = "grey"
            result = "NA" 
        else:
            color = "green"
            if ( test == 'glue1_storage_online' or test == 'glue1_storage_nearline' or \
                 test == 'glue2_storage_online' or test == 'glue2_storage_nearline' ):
                result = round(float(results[0].strip()),2)
            else:
                result = results[0].strip()

        detail_result_string="<a name=\"%s\">%s: %s</a><br>\n</body></html>" % (today,today,result)
        for line in fileinput.input(detail_file_name, inplace=True): 
            sys.stdout.write(line.replace('</body></html>', detail_result_string))
        result_string = "%s %s %s %s %s\n" % (dt,se,result,color,detail_url)
        os.write(output_fd,result_string)

    os.close(output_fd)
