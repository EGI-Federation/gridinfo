from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
import os 
    
def graph_png(request, type, uniqueid, attribute):

    if ( type == 'BDII' ):
        rrd_dir = '/var/lib/pnp4nagios'
        ds = 2
    if ( type == 'CE' ):
        rrd_dir='/var/cache/gstat/rrd/CE'
        ds=attribute
    if ( type == 'SE' ):
        rrd_dir='/var/cache/gstat/rrd/SE'
        ds=attribute

    rrd_file = '%s/%s/%s.rrd' %(rrd_dir, uniqueid, attribute)
    graph_cmd ='rrdtool graph "-" ' + \
        'DEF:mytitle=%s:%s:AVERAGE LINE2:2#FF0000 ' %(rrd_file,attribute)

    image = os.popen(graph_cmd, 'rb').read()
    response = HttpResponse(mimetype="image/png")
    response.write(image)
    response['Content-Length'] = len(image)
    return response
