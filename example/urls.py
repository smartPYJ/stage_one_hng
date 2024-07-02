from django.urls import path
from . import views

urlpatterns = [
    path('api/hello/',views.getData ),
    path('',views.getInfo ),
    
]