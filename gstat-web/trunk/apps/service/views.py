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

nagios_status = getNagiosStatusDict()

def main(request, type, output=None):

    if (output == 'json'):
        data = []
        nagios_status = getNagiosStatusDict()
        if (type == 'top'):  
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
                    status = getStatus('check-bdii-freshness', host)
                    freshness = status['current_state']
                    if (type == 'top'):
                        status = getStatus('check-bdii-sites', host)
                        state = status['current_state']
                    else:
                        status = getStatus('check-bdii-services', host)
                        state = status['current_state']
                    
                    row = [ alias, host, len(hosts), freshness, state ]
                    data.append(row)


        content = '{ "aaData": %s }' % (json.dumps(data))
        return HttpResponse(content, mimetype='application/json')  
    else:
        if (type == 'top'):
            title = "Top BDII View"
            breadcrumbs_list = [{'name':'Site BDII View',
                                 'url':'/gstat/service/site/'}]
            thead=["Alias", "Hostname", "Instances", "Freshness", "Sites"]
        else:
            title = "Site BDII View"
            breadcrumbs_list = [{'name':'Top BDII View',
                                 'url':'/gstat/service/top/'}]
            thead=["Alias", "Hostname", "Instances", "Freshness", "Services"]

        return render_to_response('single_table_service.html',
                                  {'service_active': 1,
                                   'breadcrumbs_list': breadcrumbs_list,
                                   'title' : title,
                                   'type' : type,
                                   'thead': thead})

def service(request, type, uniqueid):

    hostname = get_hostname(uniqueid)
    status_list = []
    if type == 'top':
        status_list.append( getStatus('check-bdii-freshness', hostname) )
        status_list.append( getStatus('check-bdii-sites', hostname) )
    elif type == 'site':
        status_list.append( getStatus('check-bdii-freshness', hostname) )
        status_list.append( getStatus('check-bdii-services', hostname) )
    elif type == 'ce':
        status_list.append( getStatus('check-ce', hostname) )
    elif type == 'se':
        status_list.append( getStatus('check-se', hostname) )
    elif type == 'service':
        status_list.append( getStatus('check-service', hostname) )

    elif type == 'site':
        status_list.append( getStatus('check-site', hostname) )

    if type in ['top', 'site']:
        check_type = 'monitoring'
    else:
        check_type = 'validation'

    return render_to_response('status.html', {'status_list' : status_list,
                                              'check_type'  : check_type})

def getStatus(check, hostname):

    status_dict = {'hostname': hostname,
                   'current_state': 'N/A'
                   }
    if ( nagios_status.has_key(hostname) ) :
        if ( nagios_status[hostname].has_key(check) ) :
            status_dict['check']              = check
            current_state                     = nagios_status[hostname][check]['current_state']
            has_been_checked                  = nagios_status[hostname][check]['has_been_checked']
            status_dict['current_state']      = getNagiosStatusStr(current_state, has_been_checked)
            status_dict['plugin_output']      = nagios_status[hostname][check]['plugin_output']
            status_dict['long_plugin_output'] = nagios_status[hostname][check]['long_plugin_output']
            status_dict['last_check']         = nagios_status[hostname][check]['last_check']

    return status_dict


def get_hostname(uniqueid):
    hostname=uniqueid
    index=hostname.rfind(':')
    if (index > -1 ):
        hostname = hostname[:index]
    index=hostname.find(':')
    if (index > -1 ):
        hostname = hostname[index+3:]


    return hostname

def get_hosts_from_alias(hostname):
    hosts = []
    try:
        ips = socket.gethostbyname_ex(hostname)[2]
        for ip in ips:
            instance = socket.gethostbyaddr(ip)[0]
            hosts.append(instance)
    except Exception, e:
        pass
    return hosts
    
