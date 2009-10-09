from django.shortcuts import render_to_response
from django.views.generic.list_detail import object_list

from newserializers.responses import JsonResponse
from glue.models import gluesite

def json(request, object_id=None):

    if object_id != None:
        f = GlueSite.objects.get(pk=object_id)
        return JsonResponse((f,),method='deep')
    else:
        return JsonResponse(GlueSite.objects.all(),method='deep')

