from django.contrib import admin

from myapp.models import Blog, User

# Register your models here.
admin.site.register(User)
admin.site.register(Blog)
