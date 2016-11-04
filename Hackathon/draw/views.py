from django.shortcuts import render
from django.http import HttpResponse
from draw.models import DrawData, Data
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import datetime
import json
import time


@csrf_exempt
def line_refactor(request):
    response = ""
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            json_data = json.loads(body_unicode)
            latLonList = json_data['coordinates']
            latLonStart = latLonList[0]
            latLonEnd = latLonList[1]
            bbox = json_data['bbox']
            currentObj = DrawData.objects.create(usid=json_data['id'],
                                    user=json_data['nick'],
                                    latStart=latLonStart['lat'],
                                    longStart=latLonStart['lon'],
                                    latEnd=latLonEnd['lat'],
                                    longEnd=latLonEnd['lon'],
                                    thickness=json_data['thickness'],
                                    color=json_data['color'])
            time = currentObj.timestamp - datetime.timedelta(seconds=1)
            response = serializers.serialize("json", DrawData.objects.filter(timestamp__gt=time), fields=(
                'timestamp',
                'color',
                'thickness',
                'latStart',
                'longStart',
                'latEnd',
                'longEnd',
            ))
            return HttpResponse("{\"result\":" + response + "}")
        except Exception as err:
            response += "Json failure"
            print(err)
    else:
        response += 'No valid request method!'
    return HttpResponse(response)


@csrf_exempt
def line(request):
    body_unicode = request.body.decode('utf-8')
    json_data = json.loads(body_unicode)
    latLonList = json_data['coordinates']
    latLonStart = latLonList[0]
    latLonEnd = latLonList[1]
    currentObj = Data.objects.create(usid=json_data['id'],
                                         user=json_data['nick'],
                                         latstart=latLonStart['lat'],
                                         lonstart=latLonStart['lon'],
                                         latend=latLonEnd['lat'],
                                         lonend=latLonEnd['lon'],
                                         thickness=json_data['thickness'],
                                         color=json_data['color'])
    time_delta = currentObj.timestamp - 5
    response_objects = Data.objects.filter(timestamp__gt=time_delta).exclude(user=currentObj.user)
    response = serializers.serialize("json", response_objects, fields=(
        'user',
        'timestamp',
        'color',
        'thickness',
        'latstart',
        'lonstart',
        'latend',
        'lonend',
    ))
    print(response)
    print(HttpResponse("{\"result\":" + response + "}", content_type="application/json"))
    return HttpResponse("{\"result\":" + response + "}", content_type="application/json")
