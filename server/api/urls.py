from django.urls import path, include
from . import views

urlpatterns = [
    path(r'image/<num>/', views.selectedImage, name='num'),
    path(r'image/box_info/<num>', views.selectedImageBox, name='num')
]