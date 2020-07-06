# from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from .models import Image

@csrf_exempt
def selectedImage(request):
    if request.method == 'GET':
        print(Image.objects.get(pk=1))
        item = Image.objects.get(pk=1)
        print(item.image.url)
        return JsonResponse(item.image.url, safe=False) 
