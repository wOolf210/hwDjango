from django.contrib import admin

from .models import *

class BbAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'content','price','published')
    list_display_links = ('title',)
    search_fields = ('title',)

admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric)
admin.site.register(Passport)
admin.site.register(Spare)
admin.site.register(Machine)
admin.site.register(Kit)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Note)
admin.site.register(Message)
admin.site.register(PrivateMessage)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone','website')

admin.site.register(UserProfile, UserProfileAdmin)
