from django.contrib import admin
from .models import Project, User
# Register your models here.
admin.site.register(User)
admin.site.register(Project)