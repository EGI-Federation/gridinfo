from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from topology.models import Entity
from glue.models import gluesite
from django.utils import html
from django.shortcuts import render_to_response, get_object_or_404
import gsutils
import socket

def bdii(request, bdii_type):
    if bdii_type == "bdii_top":
        title="Top BDII View"
    elif bdii_type == "bdii_site":
        title="Site BDII View"

    table=[]
    nagios_status = gsutils.get_nagios_status()
    
    qs = Entity.objects.filter(type=bdii_type)  
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
        service = "N/A"
        site =  "N/A"
        for host in alias[hostname]:
            if ( nagios_status.has_key(host)):
                services = nagios_status[host]['check-bdii-services']['current_state']

                if bdii_type == "bdii_top":
                    sites = nagios_status[host]['check-bdii-sites']['current_state']
                elif bdii_type == "bdii_site":
                    sanity = nagios_status[host]['check-sanity']['current_state']

        if bdii_type == "bdii_top":
            row = [ hostname, instances, services, sites ]
        elif bdii_type == "bdii_site":
            row = [ hostname, instances, services, sanity ]
        table.append(row)
    return render_to_response('summary.html', {'title':title,'table': table})

