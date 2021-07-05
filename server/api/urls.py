from django.urls import path, include
from . import views

urlpatterns = [
    # path(r'image/', views.selectedImage),
    # path(r'image/box_info/', views.selectedImageBox)
    path('signup/',views.signup),
    #path('start-task/', views.startTask),
    path('log/', views.recordLog),
    path('check-user/', views.checkUser),
    path('consent-agreed/', views.recordconsentAgreed),
    path('instr-done/', views.startTask),
    path('get-doctypes/', views.getDocTypes),
    path('get-cats/',views.getCats),
    path('add-cat/', views.addCat),
    path('add-subcat/', views.addSubcat),
    path('revise-cat/', views.reviseCat),
    path('revise-subcat/', views.reviseSubcat),
    path('get-image-id/', views.getImageID),
    path('get-annotations/',views.getAnnotations),
    path('get-def-annotations/',views.getDefAnnotations),
    path('save-annotation/', views.saveAnnotation),
    path('save-def-annotation/', views.saveDefAnnotation),
    path('save-as-regular/', views.saveAsRegular),
    path('delete-annotation/', views.deleteAnnotation),
    path('delete-def-annotation/', views.deleteDefAnnotation),
    path('update-status/', views.updateStatus),
    path('get-status/', views.getStatus),
    path('submit/', views.submit),
    path(r'image/<image_id>/', views.getImage, name='image_id'),
    path(r'upload_image/', views.uploadImage),
    path(r'json/<json_id>/', views.getJson, name='json_id'),
    path(r'upload_json/', views.uploadJson),
]