from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import os

def initial(request):
    file = 'firstRun'
    if (os.access(file, os.F_OK)):
        os.remove(file)
        #return HttpResponseRedirect('/gstat/register')
        return render_to_response('registerform.html')
    else:
        return HttpResponseRedirect("/gstat/geo/openlayers")

def about(request):
    return render_to_response('about.html')

def register(request):
    return render_to_response('registerform.html')