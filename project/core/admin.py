from django.contrib import admin
from .models import *
# Register your models here.
from precise_bbcode.models import BBCodeTag, SmileyTag


admin.site.register(Post)