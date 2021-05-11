from django.urls import path, include
from . import views

urlpatterns = [
    # path(r'image/', views.selectedImage),
    # path(r'image/box_info/', views.selectedImageBox)
    path('log/', views.recordLog),
    path('check-user/', views.checkUser),
    path('consent-agreed/', views.recordconsentAgreed),
    path('instr-done/', views.recordInstrDone),
    path('get-doctypes/', views.getDocTypes),
    path('get-cats/',views.getCats),
    path('get-image-id/', views.getImageID),
    path('submit/', views.submit),
]