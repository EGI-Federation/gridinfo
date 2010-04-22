from django.shortcuts import render_to_response
from core.utils import *
import urllib, urllib2
import libxml2, csv, os
#from sets import Set
from django.db import connection
from datetime import datetime

monthName = ['', 'January', 'February', 'March', 'April',
             'May', 'June', 'July', 'August', 'September',
             'October', 'November', 'December']

def index(request):
    data = getData()
    data['c5report_active'] = 1
    return render_to_response('c5report.html', data)


def viewText(request):
    data = getData()
    response = render_to_response('c5report.txt', data)
    response['Content-Type'] = 'text/plain'
    response['Content-Description'] = 'C5 Report generated by GStat 2.0'
    return response


def viewXml(request):
    data = getData()
    response = render_to_response('c5report.xml', data)
    response['Content-Type'] = 'application/xml'
    response['Content-Description'] = 'C5 Report generated by GStat 2.0'
    return response


def prettyPrintNumber(number):
    len_number = len(number)
    key = 9; value = 'B';
    if len_number > key:
        return number[0:len_number-key] + '.' + number[len_number-key:len_number-key+1] + value
    key = 6; value = 'M';
    if len_number > key:
        return number[0:len_number-key] + '.' + number[len_number-key:len_number-key+1] + value
    key = 3; value = 'K';
    if len_number > key:
        return number[0:len_number-key] + '.' + number[len_number-key:len_number-key+1] + value
    return number


def getJobsPerMonth(startMonth, startYear, endMonth, endYear):
    urlquery = 'http://www3.egee.cesga.es/gridsite/accounting/CESGA/csv_export_extend.php'
    params = {'startYear'   : startYear,
              'startMonth'  : startMonth,
              'endYear'     : endYear,
              'endMonth'    : endMonth,
              'yrange'      : 'REGION',
              'xrange'      : 'VO',
              'option'      : 'REGION',
              'optval'      : '',
              'type'        : 'Production',
              'dteamVO'     : '0',
              'query'       : 'njobs',
              'voGroup'     : 'lhc',
              'dataGroup'   : 'Production',
              'newCateg'    : '0',
              'isextend'    : '0'}
    response = urllib2.urlopen(urlquery, urllib.urlencode(params)).read()
    rows = csv.reader(response.split(os.linesep), delimiter=',', quoting=False)

    # Skip initial comments
    for i in range(0,5):
        rows.next()

    # Get the total number of jobs
    for row in rows:
        if row[0] == 'Total':
            return row[5]

    return False


def getData():
    # Initialization
    cursor = connection.cursor()
    # SAM DB API
    urlquery = 'http://lcg-sam.cern.ch:8080/reports/lcg_deployment_C5.xsql'
    response = urllib2.urlopen(urlquery).read()
    doc = libxml2.parseDoc(response)
    # Summary OSes
    #urlquery2 = 'http://horat.web.cern.ch/horat/summary-oses.xml'
    #response2 = urllib2.urlopen(urlquery2).read()
    #doc2 = libxml2.parseDoc(response2)
    # Sites in GStat 2.0
    site_list = get_sites('GRID', 'ALL')
    # Month names for easy access. E.g.: monthName[1] == 'January'
    monthName = ['', 'January', 'February', 'March', 'April', 
                 'May', 'June', 'July', 'August', 
                 'September', 'October', 'November', 'December']

    # 1.a Total number of Sites
    # Extracted from GStat 2.0 or SAM API
    # GStat 2.0 way: total_number_sites = len(site_list)
    total_number_sites = doc.xpathEval("/LCG_DEPLOYMENT/TOTAL_NUM_EGEE_SITES_CERT_PROD/VALUE/TOTAL_SITES")[0].content

    # 1.b Status (ok, degraded, down, maintenance, not available)
    # Extracted from SAM API
    # http://lcg-sam.cern.ch:8080/reports/lcg_deployment_C5.xsql
    sites_ok = doc.xpathEval("/LCG_DEPLOYMENT/TOTAL_EGEE_SITES_STATUS_CERT_PROD/VALUE[NAME='ok']/TOTAL")[0].content
    sites_degraded = doc.xpathEval("/LCG_DEPLOYMENT/TOTAL_EGEE_SITES_STATUS_CERT_PROD/VALUE[NAME='degraded']/TOTAL")[0].content
    sites_degraded += doc.xpathEval("/LCG_DEPLOYMENT/TOTAL_EGEE_SITES_STATUS_CERT_PROD/VALUE[NAME='degrated80']/TOTAL")[0].content
    sites_down = doc.xpathEval("/LCG_DEPLOYMENT/TOTAL_EGEE_SITES_STATUS_CERT_PROD/VALUE[NAME='down']/TOTAL")[0].content
    sites_maint = doc.xpathEval("/LCG_DEPLOYMENT/TOTAL_EGEE_SITES_STATUS_CERT_PROD/VALUE[NAME='maint']/TOTAL")[0].content
    sites_na = doc.xpathEval("/LCG_DEPLOYMENT/TOTAL_EGEE_SITES_STATUS_CERT_PROD/VALUE[NAME='na']/TOTAL")[0].content

    # 2. Numer of sites per software (glite 3.2 and glite 3.1)
    # Extracted from SAM API
    # http://lcg-sam.cern.ch:8080/reports/lcg_deployment_C5.xsql
    sites_glite32 = doc.xpathEval("/LCG_DEPLOYMENT/GLITE_VERSION_IN_SITES/VALUES[VERSION='3.2.0']/NUMBER_OF_SITES")[0].content
    sites_glite31 = doc.xpathEval("/LCG_DEPLOYMENT/GLITE_VERSION_IN_SITES/VALUES[VERSION='3.1.0']/NUMBER_OF_SITES")[0].content

    # 3.a Number of jobs executed last month
    # 3.b Number of jobs executed since the beginning of this month
    # Extracted from accounting portal: http://www3.egee.cesga.es/
    now = datetime.now()
    thisYear = now.year
    thisMonth = now.month
    jobs_this_month = getJobsPerMonth(thisMonth, thisYear, thisMonth, thisYear)
    jobs_this_month = prettyPrintNumber(jobs_this_month)
    jobs_this_month_monthName = monthName[thisMonth]
    jobs_this_month_monthNumber = thisMonth
    jobs_this_month_yearNumber = thisYear
    
    if thisMonth == 1:
        lastYear = thisYear - 1
        lastMonth = 12
    else:
        lastYear = thisYear
        lastMonth = thisMonth - 1
    jobs_last_month = getJobsPerMonth(lastMonth, lastYear, lastMonth, lastYear)
    jobs_last_month = prettyPrintNumber(jobs_last_month)
    jobs_last_month_monthName = monthName[lastMonth]
    jobs_last_month_monthNumber = lastMonth
    jobs_last_month_yearNumber = lastYear

    # 4. Number of CREAM CEs unique hosts deployed
    cursor.execute("SELECT count(DISTINCT ce.hostname) FROM glue_gluece ce WHERE ce.implementationname = 'CREAM';")
    creamces_unique_hosts = int(cursor.fetchall()[0][0])

    # 5. Number of LCG-CEs unique hosts deployed
    cursor.execute("SELECT count(DISTINCT ce.hostname) FROM glue_gluece ce WHERE ce.implementationname = 'LCG-CE';")
    lcgces_unique_hosts = int(cursor.fetchall()[0][0])

    # 6. - Number of sites supporting CREAM CEs
    cursor.execute("SELECT COUNT(DISTINCT cluster.gluesite_fk) FROM glue_gluece ce, glue_gluecluster cluster, glue_gluesite site WHERE ce.implementationname='CREAM' and ce.gluecluster_fk = cluster.uniqueid and cluster.gluesite_fk = site.uniqueid;")
    sites_creamces = int(cursor.fetchall()[0][0])

    # 7. - Number of sites supporting LCG-CEs
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(DISTINCT cluster.gluesite_fk) FROM glue_gluece ce, glue_gluecluster cluster, glue_gluesite site WHERE ce.implementationname='LCG-CE' and ce.gluecluster_fk = cluster.uniqueid and cluster.gluesite_fk = site.uniqueid;")
    sites_lcgces = int(cursor.fetchall()[0][0])

    # 8 Number of sites supporting MPI
    # Before, extracted from SAM API:
    # http://lcg-sam.cern.ch:8080/reports/lcg_deployment_C5.xsql
    #ces_mpi = doc.xpathEval("/LCG_DEPLOYMENT/LCG_CEs_and_CREAM_CEs_SUPPORTING_MPI/VALUE/TOTAL_CES")[0].content
    # Extracted from GStat 2.0
    cursor.execute("SELECT COUNT(*) FROM glue_gluemultivalued mv, glue_gluecluster cluster, glue_gluesite site WHERE mv.attribute = 'GlueHostApplicationSoftwareRunTimeEnvironment' and mv.value = 'MPI-START' and mv.uniqueid = cluster.uniqueid and cluster.gluesite_fk = site.uniqueid;")
    sites_mpi = int(cursor.fetchall()[0][0])

    # 9 Number of logical CPUs supporting MPI
    cursor.execute("SELECT SUM(subcluster.logicalcpus) FROM glue_gluemultivalued mv, glue_gluesubcluster subcluster WHERE mv.attribute = 'GlueHostApplicationSoftwareRunTimeEnvironment' and mv.value = 'MPI-START' and mv.uniqueid = subcluster.uniqueid;")
    logical_cpus_mpi = int(cursor.fetchall()[0][0])

    # 10. Installed Capacity per OS
    # Check with: ldapsearch -LLL -x -h lcg-bdii -p 2170 -b o=grid '(&(objectClass=GlueSubCluster)(GlueHostOperatingSystemName=*AIX*))'
    temp = {}
    cursor.execute("SELECT operatingsystemname, operatingsystemrelease, logicalcpus, benchmarksi00 FROM glue_gluesubcluster;")
    normalOS = ['AIX', 'Debian', 'Ubuntu', 'SUSE LINUX']
    rhelOS = ['Scientific Linux', 'Scientific Linux CERN', 'ScientificCERNSLC',
              'CentOS', 'ScientificSL', 'ScientificFermiLTS',
              'RedHatEnterpriseAS', 'RedHatEnterpriseWS', 'ScientificSLF']

    for row in cursor.fetchall():
        os = row[0]
        ver = row[1]
        if ver.find('.') != -1:
            ver = ver[0:ver.find('.')]
        logicalcpus = int(row[2])
        si2000 = logicalcpus * int(row[3])

        if os in normalOS:
            key = os + ' ' + ver
        elif os in rhelOS and ver != '':
            key = 'RHEL ' + ver + ' Compat'
        else:
            key = 'Unknown'

        if temp.has_key(key):
            tempkey = temp[key]
            tempkey[0] += 1
            tempkey[1] += logicalcpus
            tempkey[2] += si2000
        else:
            temp[key] = [1, logicalcpus, si2000]

    ic_per_os = []
    for key, value in temp.items():
        temp = [key]
        temp.extend(value)
        ic_per_os.append(temp)
    ic_per_os.sort(lambda x, y: cmp(x[0],y[0]))

    mySubClusters = 0
    myLogicalCPUs = 0
    mySI2000 = 0
    for temp in ic_per_os:
        mySubClusters += temp[1]
        myLogicalCPUs += temp[2]
        mySI2000 += temp[3]
    ic_per_os.append(['Total', mySubClusters, myLogicalCPUs, mySI2000])


    return {'date': datetime.utcnow().strftime("%Y-%m-%d %H:%MZ"),
            'total_number_sites': total_number_sites,
            'sites_ok': sites_ok,
            'sites_degraded': sites_degraded,
            'sites_down': sites_down,
            'sites_maint': sites_maint,
            'sites_na': sites_na,
            'sites_glite32': sites_glite32,
            'sites_glite31': sites_glite31,
            'jobs_this_month': jobs_this_month,
            'jobs_this_month_monthName': jobs_this_month_monthName,
            'jobs_this_month_monthNumber': jobs_this_month_monthNumber,
            'jobs_this_month_yearNumber': jobs_this_month_yearNumber,
            'jobs_last_month': jobs_last_month,
            'jobs_last_month_monthName': jobs_last_month_monthName,
            'jobs_last_month_monthNumber': jobs_last_month_monthNumber,
            'jobs_last_month_yearNumber': jobs_last_month_yearNumber,
            'creamces_unique_hosts': creamces_unique_hosts,
            'lcgces_unique_hosts': lcgces_unique_hosts,
            'sites_creamces': sites_creamces,
            'sites_lcgces': sites_lcgces,
            'sites_mpi': sites_mpi,
            'logical_cpus_mpi': logical_cpus_mpi,
            'ic_per_os': ic_per_os}