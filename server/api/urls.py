from django.urls import path, include
from . import views

urlpatterns = [
    # path(r'image/', views.selectedImage),
    # path(r'image/box_info/', views.selectedImageBox)
    path('log/', views.recordLog),
    path('check-user/', views.checkUser),
    path('consent-agreed/', views.consentAgreed),
]