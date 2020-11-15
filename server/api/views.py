from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import User

import json

@csrf_exempt
def checkUser(request):
    print(request)
    if request.method == 'GET':
        mturk_id = request.GET['mturk_id']
        user, created = User.objects.get_or_create(mturk_id=mturk_id)
        response = {
            'consentAgreed': user.consentAgreed,
            'step': user.step,
        }
        return JsonResponse(response)

@csrf_exempt
def consentAgreed(request):
    if request.method == 'GET':
        mturk_id = request.GET['mturk_id']
        user = User.objects.get(mturk_id=mturk_id)
        user.consentEnd()
        return HttpResponse('')

@csrf_exempt
def recordInstrDone(request):
    if request.method == 'GET':
        mturk_id = request.GET['mturk_id']
        user = User.objects.get(mturk_id=mturk_id)
        user.instrEnd()
        return HttpResponse('')

@csrf_exempt
def recordLog(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        if query_json['test'] == 'testText':
            return HttpResponse("RECEIVED")
        return HttpResponseBadRequest('Wrong test input received.')