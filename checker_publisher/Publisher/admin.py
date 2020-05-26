from django.contrib import admin
from .models import Project, User, Channel, Sended
# Register your models here.
admin.site.register(User)
admin.site.register(Project)
admin.site.register(Channel)
admin.site.register(Sended)