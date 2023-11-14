from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(File)
admin.site.register(Temp_File_Path)
admin.site.register(User)
admin.site.register(Post)