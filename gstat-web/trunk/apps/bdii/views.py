from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import html
from topology.models import Entity
from topology.models import Entityrelationship
from django.utils import simplejson as json
from summary.utils import *
import gsutils
import socket

def main(request, type=None, output=None):

    data = []

    nagios_status = getNagiosStatusDict()
    if (type == None ):
        type = 'top'
    if (type == 'top'):  
        qs = Entity.objects.filter(type='bdii_top')
    else:
        qs = Entity.objects.filter(type='bdii_site')
    alias = {} 
    hosts = [] 

    for bdii in qs:
        hostname=bdii.uniqueid
        index=hostname.find(':')
        if (index > -1 ):
            hostname= hostname[index+3:]
        index=hostname.find(':')
        if (index > -1 ):
            hostname= hostname[:index]
        try:
            ips = socket.gethostbyname_ex(hostname)[2]
            for ip in ips:
                instance = socket.gethostbyaddr(ip)[0]
                if ( alias.has_key(hostname)):
                    alias[hostname].append(instance)
                else:
                    alias[hostname] = [ instance ]
        except Exception, e:
            continue

    for hostname in alias:
        instances = len(alias[hostname])
        freshness = "N/A"
        content =  "N/A"
        for host in alias[hostname]:
            if ( nagios_status.has_key(host)):
                current_state = nagios_status[host]['check-bdii-freshness']['current_state']
                has_been_checked = nagios_status[host]['check-bdii-freshness']['has_been_checked']
                freshness = getNagiosStatusStr(current_state, has_been_checked)
                if (type == 'top'):
                    try:
                        current_state = nagios_status[host]['check-bdii-sites']['current_state']
                        has_been_checked = nagios_status[host]['check-bdii-sites']['has_been_checked']
                        content = getNagiosStatusStr(current_state, has_been_checked)
                    except KeyError:
                        content ='N/A'
                else:
                    try:
                        current_state = nagios_status[host]['check-bdii-services']['current_state']
                        has_been_checked = nagios_status[host]['check-bdii-services']['has_been_checked']
                        content = getNagiosStatusStr(current_state, has_been_checked)
                    except KeyError:
                        content ='N/A'

        host_name = hostname
        instance_counts = instances
        freshness_status = freshness
        content_status = content
        
        row = [ host_name, instance_counts, freshness_status, content_status ]
        data.append(row)

    if (output == 'json'):
        content = '{ "aaData": %s }' % (json.dumps(data))
        return HttpResponse(content, mimetype='application/json')  
    else:
        if (type == 'top'):
            title = "Top BDII View"
            breadcrumbs_list = [{'name':'Site BDII View', 'url':'/gstat/bdii/site/'}]
            thead=["Hostname", "Instances", "Freshness", "Sites"]
        else:
            title = "Site BDII View"
            breadcrumbs_list = [{'name':'Top BDII View', 'url':'/gstat/bdii/top/'}]
            thead=["Hostname", "Instances", "Freshness", "Services"]
        return render_to_response('single_table.html', {'summary_active': 1,
                                                        'breadcrumbs_list': breadcrumbs_list,
                                                        'title' : title,
                                                        'thead': thead})

    
