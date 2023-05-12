from django.db import models
from django.contrib.auth.models import User


class TagModel(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name


class NewsPostModel(models.Model):
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=150)
    paragraph1 = models.TextField(null=False)
    paragraph2 = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)
    photo = models.ImageField(null=False, upload_to='')
    date = models.DateTimeField(auto_now=True)
    tag = models.ForeignKey(TagModel, on_delete=models.DO_NOTHING, related_name='tag', null=False)
    

class CommentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(NewsPostModel, on_delete=models.CASCADE, related_name='comment')
    text = models.TextField(null=False)    
    date = models.DateTimeField(auto_now=True)


    
    