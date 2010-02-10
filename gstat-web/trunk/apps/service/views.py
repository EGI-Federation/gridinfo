from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import html
from django.utils import simplejson as json
from core.utils import *
import gsutils
import socket
import sys

def main(request, type, output=None):

    if (output == 'json'):
        data = []
        nagios_status = get_nagios_status_dict()        
        qs = get_groups(type=type)

        already_done = {}
        for bdii in qs:
            alias = get_hostname(bdii.uniqueid)
            hosts = get_hosts_from_alias(alias)
            for host in hosts:
                if ( not already_done.has_key(host) ):
                    already_done[host]=None
                    status = get_nagios_status(nagios_status, 'check-bdii-freshness', host)
                    freshness = status['current_state']
                    if (type == 'bdii_top'):
                        status = get_nagios_status(nagios_status, 'check-bdii-sites', host)
                        state = status['current_state']
                    else:
                        status = get_nagios_status(nagios_status, 'check-bdii-services', host)
                        state = status['current_state']
                    
                    row = [ alias, host, len(hosts), freshness, state ]
                    data.append(row)


        content = '{ "aaData": %s }' % (json.dumps(data))
        return HttpResponse(content, mimetype='application/json')  
    else:
        if (type == 'bdii_top'):
            title = "Top BDII View"
            breadcrumbs_list = [{'name': 'Home',
                                 'url':  '/gstat/'},
                                {'name':'Site BDII View',
                                 'url':'/gstat/service/bdii_site/'}]
            thead=["Alias", "Hostname", "Instances", "Freshness", "Sites"]
        else:
            title = "Site BDII View"
            breadcrumbs_list = [{'name': 'Home',
                                 'url':  '/gstat/'},
                                {'name':'Top BDII View',
                                 'url':'/gstat/service/bdii_top/'}]
            thead=["Alias", "Hostname", "Instances", "Freshness", "Services"]

        return render_to_response('single_table_service.html',
                                  {'service_active': 1,
                                   'breadcrumbs_list': breadcrumbs_list,
                                   'title' : title,
                                   'type' : type,
                                   'thead': thead})

def status(request, type_name, host_name, check_name):
    # Get testing results from TOP BDII    
    nagios_status = get_nagios_status_dict()   
    
    status_list = []
    if check_name == 'all':
        # all checks of single BDII (probably multiple instances)
        hostname_list_all = get_hosts_from_alias(host_name)
        for hostname in hostname_list_all:
            for check in get_check_list(nagios_status, hostname):
                status_list.append( get_nagios_status(nagios_status, check, hostname) )
    else:
        # single check of single BDII (probably multiple instances)
        hostname_list_all = get_hosts_from_alias(host_name)
        for hostname in hostname_list_all:
            status_list.append( get_nagios_status(nagios_status, check_name, hostname) )
    
    # Sort status list
    unsorted_list = status_list
    sorted_list = [(dict['hostname'], dict) for dict in unsorted_list]
    sorted_list.sort()
    result_list = [dict for (hostname, dict) in sorted_list]
    status_list = result_list   

    return render_to_response('status.html', {'status_list' : status_list})


def treeview(request, type, uniqueid):

    # decide expanded tree node
    collapse = {}
    # type: bdii_top, bdii_site, subcluster_cpu, se_online, se_nearline, vo_job, vo_online, vo_nearline
    collapse[type] = "expanded"

    # Get subtree of TOP BDIIs and associated Nagios check names for testing results
    # ["top bdii hostname", ["check list"]]
    nagios_status = get_nagios_status_dict()   
    
    topbdii_list = get_groups(type='bdii_top')
    tree_topbdii = []
    if type == 'bdii_top' and topbdii_list:
        hostnames_topbdii = [topbdii.hostname for topbdii in topbdii_list]
        hostnames_all_topbdii = get_hosts_from_aliases(hostnames_topbdii)        
        for hostname in hostnames_all_topbdii:
            tree_topbdii.append( ( hostname, tuple(get_check_list(nagios_status, hostname)) ) )
        # decide expanded tree node
        if type == "bdii_top":
            hostnames_expand = get_hosts_from_alias(uniqueid)
            for hostname_expand in hostnames_expand:
                collapse[hostname_expand] = "expanded"
        
    # Get subtree of Site BDIIs and associated Nagios check names for testing results
    # ["site bdii hostname", ["check list"]]
    sitebdii_list = get_groups(type='bdii_site')
    tree_sitebdii = []
    if type == 'bdii_site' and sitebdii_list:
        hostnames_sitebdii = [sitebdii.hostname for sitebdii in sitebdii_list]
        hostnames_all_sitebdii = get_hosts_from_aliases(hostnames_sitebdii)   
        for hostname in hostnames_all_sitebdii:
            tree_sitebdii.append( ( hostname, tuple(get_check_list(nagios_status, hostname)) ) )
        # decide expanded tree node
        if type == "bdii_site":
            hostnames_expand = get_hosts_from_alias(uniqueid)
            print hostnames_expand
            for hostname_expand in hostnames_expand:
                collapse[hostname_expand] = "expanded"


        
    # decide the default viewing content in iframe of treeview page
    url = ""
    if type == "bdii_top":
        # e.g. /gstat/service/bdii_top/bdii118.cern.ch/all/
        url = "/".join(["", "gstat", "service", type, uniqueid, "all"])
    elif type == "bdii_site":
        # e.g. /gstat/service/bdii_site/bdii116.cern.ch/all/
        url = "/".join(["", "gstat", "service", type, uniqueid, "all"])

    return render_to_response('treeview_service.html', {'service_active':   1,
                                                        'collapse':         collapse,
                                                        'tree_topbdii':     tree_topbdii,
                                                        'tree_sitebdii':    tree_sitebdii,
                                                        'url':              url})