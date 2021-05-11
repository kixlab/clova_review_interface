from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import *

import json

@csrf_exempt
def checkUser(request):
    if request.method == 'GET':
        username = request.GET['mturk_id']
        if(len(User.objects.filter(username=username))==0):
            user=User(username=username)
            user.save()
            # initialize status 
            for document in Document.objects.all():
                Status(user=user, document=document, status=False).save()
            # initialize usercats
            for initcat in InitCat.objects.all():
                UserCat(user=user, doctype=initcat.doctype, cat_no=initcat.cat_no, cat_text=initcat.cat_text).save()
            # initialize usersubcats 
            for initsubcat in InitSubCat.objects.all():
                usercat=UserCat.objects.get(user=user, doctype=initsubcat.initcat.doctype, cat_no=initsubcat.initcat.cat_no)
                UserSubcat(usercat=usercat,subcat_no=initsubcat.subcat_no, subcat_text=initsubcat.subcat_text, subcat_description=initsubcat.subcat_description).save()
        else: 
            user=User.objects.get(username=username)
        user, created = User.objects.get_or_create(username=username)
        task_done = len(list(User.objects.filter(instrEnded = True))) > 15
        response = {
            'consent_agreed': user.consentAgreed,
            'step': 1,
            'task_done': task_done
        }
        return JsonResponse(response)

@csrf_exempt
def recordconsentAgreed(request):
    if request.method == 'GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        user.consentEnd()
        return HttpResponse('')

@csrf_exempt
def recordInstrDone(request):
    if request.method == 'GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)

        if (user.instrEnded == False):
            valid_usrs = len(list(User.objects.filter(instrEnded = True)))
            user.startTask(valid_usrs)

        return HttpResponse('')

@csrf_exempt
def getDocTypes(request):
    if request.method == 'GET':
        doctypes=[doctype.doctype for doctype in DocType.objects.all()]
        return JsonResponse({'doctypes':doctypes})


@csrf_exempt
def recordLog(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        print("Hi", query_json)
        username = query_json['mturk_id']
        behavior_type = query_json['type']
        box_ids = query_json['box_ids']
        image_id = query_json['image_id']
        label = query_json['label']

        user = User.objects.get(username=username)

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
        username = request.GET['mturk_id']
        doctypetext=request.GET['doctype']
        user = User.objects.get(username=username)
        doctype=DocType.objects.get(doctype=doctypetext)
        #get least unannotated document
        startdoc=Status.objects.filter(user=user, document__doctype=doctype, status=False)[0]
        startno=startdoc.document.doc_no
        response = {
            'consent_agreed': user.consentAgreed,
            'start_image_id': startno
        }
        return JsonResponse(response)

@csrf_exempt
def getCats(request):
    if request.method == 'GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        doctypetext=request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        usercats=UserCat.objects.filter(user=user, doctype=doctype)
        subcats=[]
        for usercat in usercats:
            subcats.append(UserSubcat.objects.filter(usercat=usercat))
        
        response = {
            'cats': [usercat.cat_text for usercat in usercats],
            'subcats': [{'label': subcat.usercat.cat_text, 'sublabel':subcat.subcat_text, 'description':subcat.subcat_description} for subcat in subcats]
        }
        return JsonResponse(response)



@csrf_exempt
def submit(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        username = query_json['mturk_id']
        image_id = query_json['image_id']
        annotation_data = query_json['annotationData']
 
        user = User.objects.get(username=username)
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