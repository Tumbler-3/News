from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=150)


class NewsPost(models.Model):
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=150)
    paragraph1 = models.TextField(null=False)
    paragraph2 = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)
    photo = models.ImageField(null=False)
    date = models.DateTimeField(auto_now=True)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, related_name='tag')
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name='comment')
    text = models.TextField(null=False)    
    date = models.DateTimeField(auto_now=True)


    
    