from django.shortcuts import render
from django.db.models import Count
from newspost.models import NewsPost, Tag, Comment
from datetime import date, datetime


def main_view(request):
    
    if request.method == 'GET':
        
        news_latest = NewsPost.objects.order_by('-date')[0:1].get()
        news_latest_comments = Comment.objects.filter(post=news_latest).count()
        
        news = NewsPost.objects.order_by('-date')[1:6]
        news = news.annotate(num=Count('comment'))
        
        bus_news1 = NewsPost.objects.filter(tag__name='Business')[0:3]
        bus_news1 = bus_news1.annotate(com=Count('comment'))
        
        bus_news2 = NewsPost.objects.filter(tag__name='Business')[3:6]
        bus_news2 = bus_news2.annotate(com=Count('comment'))
        
        pop_news = NewsPost.objects.order_by('-views')[0:6]
        pop_news = pop_news.annotate(com=Count('comment'))
        
        new_com = Comment.objects.order_by('-date')[0:8]
        
        comp_news = NewsPost.objects.filter(tag__name='Company')[0:4]
        comp_news = comp_news.annotate(com=Count('comment'))
        
        job_news = NewsPost.objects.filter(tag__name='Job')[0:4]
        job_news = job_news.annotate(com=Count('comment'))
        
        ex_news = NewsPost.objects.filter(tag__name='Excursion')[0:4]
        ex_news = ex_news.annotate(com=Count('comment'))
        
        rec_news = NewsPost.objects.order_by('-date')[0:2]
        rec_news = rec_news.annotate(com=Count('comment'))
        
        return render(request, 'main.html', context={
            'time': datetime.now().strftime("%H:%M"),
            'date': date.today().strftime("%B %d, %Y"),
            
            'news_latest': news_latest,
            'news_latest_comments': news_latest_comments,
            
            'news': news,
            
            'bus_news1': bus_news1,
            'bus_news2': bus_news2,
            
            'pop_news': pop_news,
            
            'new_com': new_com,
            
            'comp_news': comp_news,
            
            'job_news': job_news,
            
            'ex_news': ex_news,
            
            'rec_news': rec_news,
        })


def post_view(request, id):
    
    if request.method == 'GET':
    
        post = NewsPost.objects.get(id=id)
        post_com = post.comment.count()
        coms = Comment.objects.filter(post=post)
        post.views += 1
        post.save()
                
        pop_news = NewsPost.objects.order_by('-views')[0:6]
        pop_news = pop_news.annotate(com=Count('comment'))
        
        new_com = Comment.objects.order_by('-date')[0:8]
        
        rec_news = NewsPost.objects.order_by('-date')[0:2]
        rec_news = rec_news.annotate(com=Count('comment'))
    
        return render(request, 'singlepost.html', context={
            'time': datetime.now().strftime("%H:%M"),
            'date': date.today().strftime("%B %d, %Y"),
            'post': post,
            'post_com': post_com,
            'coms': coms,
            
            'pop_news': pop_news,
            
            'new_com': new_com,
            
            'rec_news': rec_news,
        })