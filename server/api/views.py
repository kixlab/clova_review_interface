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
        print(User.objects)
        if(len(User.objects.filter(username=username))==0):
            user=User(username=username)
            user.save()
            # initialize status 
            for document in Document.objects.all():
                Status(user=user, document=document, status=False).save()
            # initialize usercats
            for initcat in InitCat.objects.all():
                UserCat(user=user, doctype=initcat.doctype, cat_text=initcat.cat_text).save()
            # initialize usersubcats 
            for initsubcat in InitSubCat.objects.all():
                usercat=UserCat.objects.get(user=user, doctype=initsubcat.initcat.doctype, cat_text=initsubcat.initcat.cat_text)
                UserSubcat(usercat=usercat, subcat_text=initsubcat.subcat_text, subcat_description=initsubcat.subcat_description).save()
        else: 
            user=User.objects.get(username=username)
        user, created = User.objects.get_or_create(username=username)
        response = {
            'consent_agreed': user.consentAgreed,
            'step': 1
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
        cats=[]
        for usercat in usercats:
            cats.append({'cat': usercat.cat_text, 'pk': usercat.pk, 'usermade': (usercat.made_at!=9999), 'rev':False})
            for subcat in UserSubcat.objects.filter(usercat=usercat):
                subcats.append({'cat': subcat.usercat.cat_text, 'subcat':subcat.subcat_text, 'description':subcat.subcat_description, 'pk':subcat.pk, 'usermade': (subcat.made_at!=9999),'rev':False})
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
        doctypetext=request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        image_id =request.GET['image_id']
        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))
        annots=Annotation.objects.filter(user=user, document=document,is_alive=True)
        print(annots)

        annotations=[]
        for annot in annots: 
            annotations.append({'group_id':annot.pk, 'boxes_id': annot.boxes_id, 'label': annot.label})
        
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
        doctypetext=query_json['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)
        image_id =query_json['image_id']
        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))
        boxes = query_json['boxes_id']
        labelpk = query_json['labelpk']
        thisLabel = UserSubcat.objects.get(pk=labelpk)
        newAnnot=Annotation(user=user, document=document, boxes_id = boxes, label=thisLabel, is_alive=True)
        newAnnot.save()
        response={
            'annot_pk': newAnnot.pk
        }
        return JsonResponse(response)

@csrf_exempt
def deleteAnnotation(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
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
def submit(request):
    if request.method == 'POST':
        query_json = json.loads(request.body)
        username = query_json['mturk_id']
        doctypetext=query_json['doctype']
        image_id = query_json['image_id']
        annotation_data = query_json['annotationData']

        doctype=DocType.objects.get(doctype=doctypetext)

        document=Document.objects.get(doctype=doctype, doc_no=int(image_id))
        user = User.objects.get(username=username)
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
        doctypetext=request.GET['doctype']
        doctype=DocType.objects.get(doctype=doctypetext)

        documents=Document.objects.filter(doctype=doctype)
        status=[]
        for doc in documents:
            thisStat=Status.objects.get(document=doc, user=user)
            status.append(thisStat.status)

        return JsonResponse({'status': status})

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

        UserSubcat.objects.filter(pk=int(subcat_pk)).update(subcat_text=revsubcat, subcat_description=revdesc)
        return HttpResponse('')



