from django.contrib import admin
from newspost.models import NewsPost, Comment, Tag

admin.site.register(Tag)
admin.site.register(NewsPost)
admin.site.register(Comment)
