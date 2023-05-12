from django.shortcuts import redirect, render
from django.db.models import Count
from newspost.models import NewsPostModel, CommentModel, TagModel
from newspost.forms import NewsPostForm
from datetime import date, datetime


def main_view(request):
    
    if request.method == 'GET':
        
        news_latest = NewsPostModel.objects.order_by('-date')[0:1].get()
        news_latest_comments = CommentModel.objects.filter(post=news_latest).count()
        
        news = NewsPostModel.objects.order_by('-date')[1:6]
        news = news.annotate(num=Count('comment'))
        
        bus_news1 = NewsPostModel.objects.filter(tag__name='Business')[0:3]
        bus_news1 = bus_news1.annotate(com=Count('comment'))
        
        bus_news2 = NewsPostModel.objects.filter(tag__name='Business')[3:6]
        bus_news2 = bus_news2.annotate(com=Count('comment'))
        
        pop_news = NewsPostModel.objects.order_by('-views')[0:6]
        pop_news = pop_news.annotate(com=Count('comment'))
        
        new_com = CommentModel.objects.order_by('-date')[0:8]
        
        comp_news = NewsPostModel.objects.filter(tag__name='Company')[0:4]
        comp_news = comp_news.annotate(com=Count('comment'))
        
        job_news = NewsPostModel.objects.filter(tag__name='Job')[0:4]
        job_news = job_news.annotate(com=Count('comment'))
        
        ex_news = NewsPostModel.objects.filter(tag__name='Excursion')[0:4]
        ex_news = ex_news.annotate(com=Count('comment'))
        
        rec_news = NewsPostModel.objects.order_by('-date')[0:2]
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


def single_view(request, id):
    
    if request.method == 'GET':
    
        singlepost = NewsPostModel.objects.get(id=id)
        post_com = singlepost.comment.count()
        coms = CommentModel.objects.filter(post=singlepost)
        singlepost.views += 1
        singlepost.save()
                
        pop_news = NewsPostModel.objects.order_by('-views')[0:6]
        pop_news = pop_news.annotate(com=Count('comment'))
        
        new_com = CommentModel.objects.order_by('-date')[0:8]
        
        rec_news = NewsPostModel.objects.order_by('-date')[0:2]
        rec_news = rec_news.annotate(com=Count('comment'))
    
        return render(request, 'singlepost.html', context={
            'time': datetime.now().strftime("%H:%M"),
            'date': date.today().strftime("%B %d, %Y"),
            'post': singlepost,
            'post_com': post_com,
            'coms': coms,
            
            'pop_news': pop_news,
            
            'new_com': new_com,
            
            'rec_news': rec_news,
        })
        

def post_create_view(request):
    
    pop_news = NewsPostModel.objects.order_by('-views')[0:6]
    pop_news = pop_news.annotate(com=Count('comment'))
        
    new_com = CommentModel.objects.order_by('-date')[0:8]
        
    rec_news = NewsPostModel.objects.order_by('-date')[0:2]
    rec_news = rec_news.annotate(com=Count('comment'))
    
    if request.method == 'GET':
        
        form = NewsPostForm
        
        return render(request, 'singlepostform.html', context={
            'time': datetime.now().strftime("%H:%M"),
            'date': date.today().strftime("%B %d, %Y"),
            'form':form,
            
            'pop_news': pop_news,
            
            'new_com': new_com,
            
            'rec_news': rec_news,
            })

    
    if request.method == 'POST':
        
        form = NewsPostForm(request.POST, request.FILES)

        if form.is_valid():
            print(form.cleaned_data)
            NewsPostModel.objects.create(
                creator=request.user,
                title=form.cleaned_data.get('title'),
                paragraph1=form.cleaned_data.get('paragraph1'),
                paragraph2=form.cleaned_data.get('paragraph2'),
                photo=form.cleaned_data.get('photo'),
                tag=form.cleaned_data.get('tag'),
            )

            return redirect('/')
        
        
        return render(request, 'singlepostform.html', context={
            'time': datetime.now().strftime("%H:%M"),
            'date': date.today().strftime("%B %d, %Y"),
            'form':form,
            
            'pop_news': pop_news,
            
            'new_com': new_com,
            
            'rec_news': rec_news,
            })
    
    