from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import html
from topology.models import Entity
from topology.models import Entityrelationship
from django.utils import simplejson as json
from core.utils import *
import gsutils
import socket
import sys

def main(request, type, output=None):

    if (output == 'json'):
        data = []
        nagios_status = getNagiosStatusDict()
        if (type == 'topbdii'):  
            qs = Entity.objects.filter(type='bdii_top')
        else:
            qs = Entity.objects.filter(type='bdii_site')

        already_done = {}
        for bdii in qs:
            alias = get_hostname(bdii.uniqueid)
            hosts = get_hosts_from_alias(alias)
            for host in hosts:
                if ( not already_done.has_key(host) ):
                    already_done[host]=None
                    status = getNagiosStatus(nagios_status, 'check-bdii-freshness', host)
                    freshness = status['current_state']
                    if (type == 'topbdii'):
                        status = getNagiosStatus(nagios_status, 'check-bdii-sites', host)
                        state = status['current_state']
                    else:
                        status = getNagiosStatus(nagios_status, 'check-bdii-services', host)
                        state = status['current_state']
                    
                    row = [ alias, host, len(hosts), freshness, state ]
                    data.append(row)


        content = '{ "aaData": %s }' % (json.dumps(data))
#        return HttpResponse(content, mimetype='application/json')  
        return render_to_response('single_table_service.html')  
    else:
        if (type == 'topbdii'):
            title = "Top BDII View"
            breadcrumbs_list = [{'name':'Site BDII View',
                                 'url':'/gstat/service/sitebdii/'}]
            thead=["Alias", "Hostname", "Instances", "Freshness", "Sites"]
        else:
            title = "Site BDII View"
            breadcrumbs_list = [{'name':'Top BDII View',
                                 'url':'/gstat/service/topbdii/'}]
            thead=["Alias", "Hostname", "Instances", "Freshness", "Services"]

        return render_to_response('single_table_service.html',
                                  {'service_active': 1,
                                   'breadcrumbs_list': breadcrumbs_list,
                                   'title' : title,
                                   'type' : type,
                                   'thead': thead})

def service(request, type, uniqueid):

    hostname = get_hostname(uniqueid)
    
    hosts_from_alias = get_hosts_from_alias(hostname)
    
    hostname_list = []
    if ( len(hosts_from_alias) > 1 ):
        #This is and alias point to more than on reall hostname
        hostname_list = hosts_from_alias
    elif not ( hostname == hosts_from_alias[0]):
        #This is an alias for a single instance
        hostname_list = hosts_from_alias
    else:
        #The actual id given was a real host.
        hostname_list.append(hostname)
            
    nagios_status = getNagiosStatusDict()
    status_list = []
    for hostname in hostname_list:
        if type == 'topbdii':
            status_list.append( getNagiosStatus(nagios_status, 'check-bdii-freshness', hostname) )
            status_list.append( getNagiosStatus(nagios_status, 'check-bdii-sites', hostname) )
        elif type == 'sitebdii':
            status_list.append( getNagiosStatus(nagios_status, 'check-bdii-freshness', hostname) )
            status_list.append( getNagiosStatus(nagios_status, 'check-bdii-services', hostname) )
        elif type == 'ce':
            status_list.append( getNagiosStatus(nagios_status, 'check-ce', hostname) )
        elif type == 'se':
            status_list.append( getNagiosStatus(nagios_status, 'check-se', hostname) )
        elif type == 'service':
            status_list.append( getNagiosStatus(nagios_status, 'check-service', hostname) )
        elif type == 'site':
            status_list.append( getNagiosStatus(nagios_status, 'check-site', hostname) )

    if type in ['topbdii', 'sitebdii']:
        check_type = 'monitoring'
    else:
        check_type = 'validation'

    return render_to_response('status.html', {'status_list' : status_list,
                                              'check_type'  : check_type})
