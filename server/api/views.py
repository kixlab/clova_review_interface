from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import *

import json
from datetime import datetime, timedelta
from django.db.models import Max


@csrf_exempt
@api_view(['POST','GET'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data['username']
    password = username
    if len(User.objects.filter(username=username))==0:
        new_user=User(username=username, password=password)
        new_user.save()
        login(request, new_user)
#        print('logged in?', new_user.is_authenticated)
        
        response = {
            'status': 'new',
            'doctype': 'receipt'
        }
    else: # if already signed up 
        user=User.objects.get(username=username)
        profile=Profile.objects.get(user=user)
        login(request, user)
        if profile.consent_agreed:
            response = {
                'status': 'annotation',
                'doctype':profile.doctype.doctype
            }
        else:
            response = {
                'status':'consent',
                'doctype':profile.doctype.doctype
            }
    return JsonResponse(response)

@csrf_exempt
def startTask(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        username = query_json['mturk_id']
        user = User.objects.get(username=username)
        profile=Profile.objects.get(user=user)
        profile.instr_read = True

        # assign task by assigning start image number 
        ## get smallest available user_order 
        # check if there is a user order taken but not completed
        dropouts=Profile.objects.filter(instr_read=True, doctype=profile.doctype, done=False, starttime__lte=(datetime.now()-timedelta(hours=1, minutes=50)), dropout=False)
        if(len(dropouts)==0):
            # assign new order
            active_profiles=Profile.objects.filter(instr_read=True,doctype=profile.doctype, dropout=False)
            if(len(active_profiles)==0):
                order=0
            else:
                last_order= actice_profiles.order_by('-user_order')[0].user_order  #aggregate(Max('user_order'))
                print(last_order)
                order=last_order+1 
        else:
            # reassign the first dropout order to this user 
            dropout=dropouts[0]
            dropout.dropout=True
            dropout.save()

            order=dropout.user_order
        profile.starttime=datetime.now()
        profile.user_order=order        
        profile.save()

        # assign documents 
        documents=Document.objects.filter(doctype=profile.doctype).order_by('doc_no')[order*21:((order+1)*21)]

        # initialize status 
        for document in documents:
            Status(user=user, document=document, status=False).save()

        response={
            'user_order': order,
            'doctype': profile.doctype.doctype
        }
        return JsonResponse(response)

@csrf_exempt
def checkUser(request):
    if request.method =='GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        
        #user=request.user 
        #print('user', user)
        #print('request', request)
        if(user == None):
            response={
                'login_status': False
            }
        else:
            response={
                'login_status': True,
                'username': user.username
            }
        return JsonResponse(response)

        
""" @csrf_exempt
def checkUser(request):
    if request.method == 'GET':
        username = request.GET['mturk_id']
        print(User.objects)
        if(len(User.objects.filter(username=username))==0):
            user=User(username=username)
            user.save()
            # initialize status 
            for document in Document.objects.all():
                Status(user=user, document=document, status=False).save()
            # initialize usercats
            for initcat in InitCat.objects.all():
                usercat=UserCat(user=user, doctype=initcat.doctype, cat_text=initcat.cat_text)
                usercat.save()
            # add N/A category 
            for doctype in DocType.objects.all():
                UserCat(user=user, doctype=doctype, cat_text="N/A").save()
            # initialize usersubcats 
            for initsubcat in InitSubCat.objects.all():
                usercat=UserCat.objects.get(user=user, doctype=initsubcat.initcat.doctype, cat_text=initsubcat.initcat.cat_text)
                UserSubcat(usercat=usercat, subcat_text=initsubcat.subcat_text, subcat_description=initsubcat.subcat_description).save()   
            # add N/A subcategory to each category 
            for usercat in UserCat.objects.filter(user=user):
                UserSubcat(usercat=usercat, subcat_text="N/A", subcat_description="Not applicable or does not exist").save()
        else: 
            user=User.objects.get(username=username)
        user, created = User.objects.get_or_create(username=username)
        response = {
            'consent_agreed': user.consentAgreed,
            'step': 1
        }
        return JsonResponse(response) """

@csrf_exempt
def recordconsentAgreed(request):
    if request.method == 'GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        #user=request.user
        profile=Profile.objects.get(user=user)
        profile.consent_agreed=True
        profile.save()
        return HttpResponse('')

""" @csrf_exempt
def recordInstrDone(request):
    if request.method == 'GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        #user=request.user
        profile=Profile.objects.get(user=user)
        profile.instr_read=True
        profile.starttime=datetime.now()




        if (user.instrEnded == False):
            valid_usrs = len(list(User.objects.filter(instrEnded = True)))
            user.startTask(valid_usrs)

        return HttpResponse('') """

@csrf_exempt
def getDocTypes(request):
    if request.method == 'GET':
        doctypes=[doctype.doctype for doctype in DocType.objects.all()]
        return JsonResponse({'doctypes':doctypes})


@csrf_exempt
def recordLog(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
#        user=request.user
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
#        user=request.user
        username = request.GET['mturk_id']        
        user = User.objects.get(username=username)
        profile=Profile.objects.get(user=user)

        #get least unannotated document
        undonedocs=Status.objects.filter(user=user, document__doctype=profile.doctype, status=False)
        if(len(undonedocs)==0):
            startdoc=Status.objects.filter(user=user, document__doctype=profile.doctype, status=True).last()
        else:
            startdoc=undonedocs[0]
        startno=startdoc.document.doc_no
        response = {
            'start_image_id': startno
        }
        return JsonResponse(response)

@csrf_exempt
def getCats(request):
    if request.method == 'GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        profile=Profile.objects.get(user=user)
        initcats=InitCat.objects.filter(doctype=profile.doctype)
        subcats=[]
        cats=[]
        for cat in initcats:
            cats.append({'cat': cat.cat_text, 'pk': cat.pk})
            for subcat in InitSubCat.objects.filter(initcat=cat):
                subcats.append({'cat': subcat.initcat.cat_text, 'subcat':subcat.subcat_text, 'description':subcat.subcat_description, 'pk':subcat.pk, 'catpk':subcat.initcat.pk})
        response = {
            'cats': cats,
            'subcats': subcats
        }
        return JsonResponse(response)

@csrf_exempt
def getAnnotations(request):
    if request.method=='GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        #user=request.user
        doctypetext=request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        image_id =request.GET['image_id']
        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))
        annots=Annotation.objects.filter(user=user, document=document,is_alive=True)
        print(annots)

        annotations=[]
        for annot in annots: 
            annotations.append({'group_id':annot.pk, 'boxes_id': annot.boxes_id, 'cat': annot.label.usercat.cat_text, 'subcat': annot.label.subcat_text, 'subcatpk': annot.label.pk, 'catpk':annot.label.usercat.pk})
        
        response={
            'annotations':annotations
        }
        return JsonResponse(response)

@csrf_exempt
def getDefAnnotations(request):
    if request.method=='GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        #user=request.user
        doctypetext=request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        image_id =request.GET['image_id']
        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))
        annots=DefAnnotation.objects.filter(user=user, document=document,is_alive=True)
        print(annots)

        annotations=[]
        for annot in annots: 
            if(annot.subcat==None):
                annotations.append({'group_id':annot.pk, 'boxes_id': annot.boxes_id, 'cat': annot.cat.cat_text, 'subcat':None, 'subcatpk': None, 'catpk':annot.cat.pk, 'confidence': None })
            else:
                if(annot.subcat.subcat_text=="N/A"):
                    annotations.append({'group_id':annot.pk, 'boxes_id': annot.boxes_id, 'cat': annot.cat.cat_text, 'subcat':annot.subcat.subcat_text, 'subcatpk':annot.subcat.pk, 'catpk':annot.cat.pk, 'confidence': None})
                else:
                    annotations.append({'group_id':annot.pk, 'boxes_id': annot.boxes_id, 'cat': annot.cat.cat_text, 'subcat':annot.subcat.subcat_text, 'subcatpk':annot.subcat.pk, 'catpk':annot.cat.pk, 'confidence': annot.confidence})
        response={
            'annotations':annotations
        }
        return JsonResponse(response)

@csrf_exempt
def saveAnnotation(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        user = User.objects.get(username=username)
        #user=request.user
        doctypetext=query_json['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        image_id =query_json['image_id']
        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))
        boxes = query_json['boxes_id']
        labelpk = query_json['labelpk']
        thisLabel = UserSubcat.objects.get(pk=labelpk)
        newAnnot=Annotation(user=user, document=document, boxes_id = boxes, cat=thisLabe.usercat, subcat=thisLabel, is_alive=True)
        newAnnot.save()
        response={
            'annot_pk': newAnnot.pk
        }
        return JsonResponse(response)

@csrf_exempt
def saveDefAnnotation(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        user = User.objects.get(username=username)
        #user=request.user
        doctypetext=query_json['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        image_id =query_json['image_id']
        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))
        boxes = query_json['boxes_id']
        subcatpk = query_json['subcatpk']
        catpk = query_json['catpk']
        confidence=query_json['confidence']
        thisSubcat=UserSubcat.objects.get(pk=subcatpk)
        thisCat=UserCat.objects.get(pk=catpk)
        if(thisSubcat.subcat_text=='N/A'):
            newDefAnnot=DefAnnotation(user=user, document=document, boxes_id = boxes, cat=thisCat, subcat=thisSubcat, confidence=False, is_alive=True)
        else:
            newDefAnnot=DefAnnotation(user=user, document=document, boxes_id = boxes, cat=thisCat, subcat=thisSubcat, confidence=confidence, is_alive=True)
        newDefAnnot.save()
        response={
            'annot_pk': newDefAnnot.pk
        }
        return JsonResponse(response)


@csrf_exempt
def saveAsRegular(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
#        user=request.user
        username=query_json['mturk_id']
        user = User.objects.get(username=username)
        doctypetext=query_json['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)

        confDefAnnots=DefAnnotation.objects.filter(user=user, confidence=True, is_alive=True)
        for annot in confDefAnnots:
            newAnnot=Annotation(user=user, document=annot.document, boxes_id=annot.boxes_id, cat=annot.cat, subcat=annot.subcat, is_alive=True)
            newAnnot.save()
        response={
            'annot_pk': newAnnot.pk
        }
        return JsonResponse(response)


@csrf_exempt
def deleteAnnotation(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
#        user=request.user
        username=query_json['mturk_id']
        user = User.objects.get(username=username)
        doctypetext=query_json['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        image_id =query_json['image_id']
        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))
        annot_pk = query_json['annot_pk']
        thisAnnot=Annotation.objects.get(user=user, pk=annot_pk)
        thisAnnot.is_alive=False
        thisAnnot.save()
        response={
            'annot_pk': annot_pk
        }
        return JsonResponse(response)
@csrf_exempt
def deleteDefAnnotation(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        username=query_json['mturk_id']
        user = User.objects.get(username=username)
        #user=request.user
        doctypetext=query_json['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        image_id =query_json['image_id']
        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))
        annot_pk = query_json['annot_pk']
        thisAnnot=DefAnnotation.objects.get(user=user, pk=annot_pk)
        thisAnnot.is_alive=False
        thisAnnot.save()
        response={
            'annot_pk': annot_pk
        }
        return JsonResponse(response)

@csrf_exempt
def submit(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        user=request.user
#        username = query_json['mturk_id']
        doctypetext=query_json['doctype']
        image_id = query_json['image_id']
        annotation_data = query_json['annotationData']

        doctype=DocType.objects.get(doctype=doctypetext)

        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))
 #       user = User.objects.get(username=username)
        Status.objects.filter(user=user, document=document).update(status=True)

        #delete old labels --> this to be changed to record all the logs later
        Annotation.objects.filter(user=user, document=document).delete()

        for group in annotation_data:
            box_ids = group['boxes']
            label = group['label']
            group_id = group['group_id']

            for box_id in box_ids:
                Annotation(user=user, document=document, group_id=group_id, box_id=box_id,
                status=True, label=label).save()

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

        yetdocs=Status.objects.filter(user=user, document__doctype=doctype, status=False)
        if(len(yetdocs)>0):
            startno=yetdocs[0].document.doc_no
        else:
            startno=99

        donedocs=Status.objects.filter(user=user, document__doctype=doctype, status=True)

        response = {
            'next_img': startno,
            'step': len(donedocs)
        }
        return JsonResponse(response)


@csrf_exempt
def updateStatus(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        #user=request.user
        username = query_json['mturk_id']
        doctypetext=query_json['doctype']
        image_id = query_json['image_id']
        status= query_json['status']
        doctype=DocType.objects.get(doctype=doctypetext)

        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))
        user = User.objects.get(username=username)
        if(status):
            Status.objects.filter(user=user, document=document).update(status=True)
        else:
            Status.objects.filter(user=user, document=document).update(status=False)
        return HttpResponse('')



@csrf_exempt
def getStatus(request):
    if request.method=='GET':
        username = request.GET['mturk_id']
        user = User.objects.get(username=username)
        #user=request.user
        doctypetext=request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)

        documents=Document.objects.filter(doctype=doctype)
        status=Status.objects.filter(user=user).values_list('status', flat=True)
        return JsonResponse({'status': list(status)})

@csrf_exempt
def addCat(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username = query_json['mturk_id']
        doctypetext=query_json['doctype']
        image_id = query_json['image_id']
        cat= query_json['cat']
        doctype=DocType.objects.get(doctype=doctypetext)
        user = User.objects.get(username=username)
        #user=request.user
        newCat=UserCat(user=user, doctype=doctype, cat_text=cat, made_at=int(image_id))
        newCat.save()
        response = {
            'newcat_pk': newCat.pk,
        }
        return JsonResponse(response)


@csrf_exempt
def addSubcat(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username = query_json['mturk_id']
        doctypetext=query_json['doctype']
        image_id = query_json['image_id']
        cat= query_json['cat']
        subcat=query_json['subcat']
        desc=query_json['description']

        doctype=DocType.objects.get(doctype=doctypetext)
        user = User.objects.get(username=username)
        #user=request.user
        print(cat)
        cat = UserCat.objects.get(user=user, doctype=doctype, cat_text=cat)


        newSubcat=UserSubcat(usercat=cat, subcat_text=subcat, subcat_description=desc, made_at=int(image_id))
        newSubcat.save()
        response = {
            'newsubcat_pk': newSubcat.pk,
        }
        return JsonResponse(response)

@csrf_exempt
def reviseCat(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username = query_json['mturk_id']
        doctypetext=query_json['doctype']
        cat_pk= query_json['cat_pk']
        revcat=query_json['revcat']

        doctype=DocType.objects.get(doctype=doctypetext)
        user = User.objects.get(username=username)
        #user=request.user

        UserCat.objects.filter(user=user, doctype=doctype, pk=int(cat_pk)).update(cat_text=revcat)
        return HttpResponse('')


@csrf_exempt
def reviseSubcat(request):
    if request.method=='POST':
        query_json = json.loads(request.body)
        username = query_json['mturk_id']
        doctypetext=query_json['doctype']
        subcat_pk= query_json['subcat_pk']
        revsubcat=query_json['revsubcat']
        revdesc=query_json['revdesc']

        doctype=DocType.objects.get(doctype=doctypetext)
        user = User.objects.get(username=username)
#        user=request.user

        UserSubcat.objects.filter(pk=int(subcat_pk)).update(subcat_text=revsubcat, subcat_description=revdesc)
        return HttpResponse('')


@csrf_exempt
def getImage(request, image_id):
    if request.method == 'GET':
        item = Image.objects.get(image_id=image_id)
        # item = Image.objects.filter(is_done=True)[int(num)]
        return HttpResponse(item.image.url)

'''
@csrf_exempt
def getImageBoxInfo(request, image_id):
    if request.method == 'GET':
        item = Image.objects.get(image_id=image_id)
        return HttpResponse(item.box_info)
'''

@csrf_exempt
def uploadImage(request):
    if request.method == 'POST':
        file = request.FILES["image_file"]
        image_id = file.name.replace(".png", "")
        if len(Image.objects.filter(image_id=image_id)) != 0:
            return HttpResponseBadRequest("The image_id exists!")

        data = request.POST
        image = Image(image_id=file.name.replace(".png", ""), image=file, box_info=data["text"])
        image.save()
        return HttpResponse("Uploaded!")

@csrf_exempt
def getJson(request, json_id):
    if request.method == 'GET':
        item = Json.objects.get(json_id=json_id)
        # item = Image.objects.filter(is_done=True)[int(num)]
        return HttpResponse(item.json.url)


@csrf_exempt
def uploadJson(request):
    if request.method == 'POST':
        file = request.FILES["json_file"]
        json_id = file.name.replace(".json", "")
        if len(Image.objects.filter(json_id=json_id)) != 0:
            return HttpResponseBadRequest("The json_id exists!")

        data = request.POST
        json = Json(image_id=file.name.replace(".json", ""), image=file)
        json.save()
        return HttpResponse("Uploaded!")
