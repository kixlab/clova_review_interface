from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
import json

from .models import Image

@csrf_exempt
def selectedImage(request):
    if request.method == 'GET':
        item = Image.objects.filter(is_done=False)[0]
        return HttpResponse(item.image.url)

    elif request.method == 'POST':
        query_json = json.loads(request.body)
        if query_json['test'] == 'testText':
            return HttpResponse("RECEIVED")
        return HttpResponseBadRequest('Wrong test input received.')

def selectedImageBox(request):
    if request.method == 'GET':
        item = Image.objects.filter(is_done=False)[0]
        return HttpResponse(item.box_info)