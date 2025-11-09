from django.urls import path
from . import views

app_name = 'predictor'

urlpatterns = [
    path('', views.index, name='index'),           # Home
    path('upload/', views.upload_page, name='upload_page'),  # Upload page
    path('camera/', views.camera_page, name='camera_page'),  # Camera page
    path('predict/upload/', views.predict_upload, name='predict_upload'),
    path('predict/camera/', views.predict_camera, name='predict_camera'),
]
