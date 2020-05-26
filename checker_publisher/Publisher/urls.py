from django.contrib import admin 
from django.urls import path, include
from .views import channels, save_user, check_user, search_project, check_task, send_image

urlpatterns = [ 
   path('dashboard', channels),
   path('dashboard/submit_user', save_user),
   path('dashboard/check_user', check_user),
   path('dashboard/search_project', search_project),
   path('dashboard/check_task', check_task),
   path('dashboard/send_image', send_image),
]