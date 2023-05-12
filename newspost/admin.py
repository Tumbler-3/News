from django.contrib import admin
from newspost.models import NewsPostModel, CommentModel, TagModel

admin.site.register(TagModel)
admin.site.register(NewsPostModel)
admin.site.register(CommentModel)
