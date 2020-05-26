from django.contrib import admin 
from django.urls import path, include
from .views import dashboard, save_user, check_user, search_project, check_task, send_image, save_channel, check_channel

urlpatterns = [ 
   path('dashboard', dashboard),
   path('dashboard/submit_user', save_user),
   path('dashboard/check_user', check_user),
   path('dashboard/search_project', search_project),
   path('dashboard/check_task', check_task),
   path('dashboard/send_image', send_image),
   path('dashboard/save_channel', save_channel),
   path('dashboard/check_channel', check_channel),
]