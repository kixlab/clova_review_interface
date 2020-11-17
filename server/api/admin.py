from django.contrib import admin

from .models import User, Log, Label

admin.site.register(User)
admin.site.register(Log)
admin.site.register(Label)