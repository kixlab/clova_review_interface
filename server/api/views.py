from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import User, Log, Label

import json

@csrf_exempt
def checkUser(request):
    if request.method == 'GET':
        mturk_id = request.GET['mturk_id']
        user, created = User.objects.get_or_create(mturk_id=mturk_id)
        task_done = len(list(User.objects.filter(instrEnded = True))) > 15
        response = {
            'consent_agreed': user.consentAgreed,
            'step': user.step,
            'task_done': task_done
        }
        return JsonResponse(response)

@csrf_exempt
def recordconsentAgreed(request):
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

        if (user.instrEnded == False):
            valid_usrs = len(list(User.objects.filter(instrEnded = True)))
            user.startTask(valid_usrs)

        return HttpResponse('')


@csrf_exempt
def recordLog(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        print(query_json)
        mturk_id = query_json['mturk_id']
        behavior_type = query_json['type']
        box_ids = query_json['box_ids']
        image_id = query_json['image_id']
        label = query_json['label']

        user = User.objects.get(mturk_id=mturk_id)

        Log.objects.create(
            user = user,
            behavior = behavior_type,
            boxIDs = box_ids,
            imageID = image_id,
            label = label
        )

        return HttpResponse("")

@csrf_exempt
def getImageID(request):
    if request.method == 'GET':
        mturk_id = request.GET['mturk_id']
        user = User.objects.get(mturk_id=mturk_id)
        
        response = {
            'consent_agreed': user.consentAgreed,
            'start_image_id': user.start_image_id,
            'step': user.step,
        }
        return JsonResponse(response)

@csrf_exempt
def submit(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        mturk_id = query_json['mturk_id']
        image_id = query_json['image_id']
        annotation_data = query_json['annotationData']
 
        user = User.objects.get(mturk_id=mturk_id)
        user.step_up()

        for group in annotation_data:
            box_ids = group['boxes']
            label = group['label']
            group_id = group['group_id']

            Label.objects.create(
                user = user,
                imageID = image_id,
                groupID = group_id,
                label = label,
                boxIDs = box_ids
            )

        Log.objects.create(
            user = user,
            imageID = image_id,
            behavior = 'SU'
        )

        response = {
            'start_image_id': user.start_image_id,
            'step': user.step,
        }
        return JsonResponse(response)