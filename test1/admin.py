from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *


admin.site.register(ToDoItem)
admin.site.register(Test)
admin.site.register(Test2)
