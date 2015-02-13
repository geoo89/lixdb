from django.contrib import admin

from lixdb.models import Directory, Level, Replay, UserProfile

admin.site.register(Directory)
admin.site.register(Level)
admin.site.register(Replay)
admin.site.register(UserProfile)

# class PageAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'url')