from django.contrib import admin

from post.models import Category, Job, Locality

# Register your models here.
admin.site.register(Category)
admin.site.register(Job)
admin.site.register(Locality)