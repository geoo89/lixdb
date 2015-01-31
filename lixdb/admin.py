from django.contrib import admin

from lixdb.models import Directory, Level, Replay

admin.site.register(Directory)
admin.site.register(Level)
admin.site.register(Replay)

# class PageAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'url')