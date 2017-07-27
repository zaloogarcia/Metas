from django.contrib import admin
from .models import Task, SubTask, Category, Comment, File

# Register your models here.
admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(File)
