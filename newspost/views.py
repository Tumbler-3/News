from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count
from newspost.models import NewsPostModel, CommentModel, TagModel
from newspost.forms import NewsPostForm, CommentForm
from datetime import date, datetime
from News.settings import PAGINATION_LIMIT


def main_view(request):

    if request.method == 'GET':
        try:
            news_latest = NewsPostModel.objects.order_by('-date')[0:1].get()
            news_latest_comments = CommentModel.objects.filter(
                post=news_latest).count()
        except:
            news_latest = None
            news_latest_comments = None
            
        try:
            news = NewsPostModel.objects.order_by('-date')[1:6]
            news = news.annotate(num=Count('comment'))
        except:
            news = None
            
        try:
            bus_news1 = NewsPostModel.objects.filter(tag__name='Business')[0:3]
            bus_news1 = bus_news1.annotate(com=Count('comment'))

            bus_news2 = NewsPostModel.objects.filter(tag__name='Business')[3:6]
            bus_news2 = bus_news2.annotate(com=Count('comment'))
        except:
            bus_news1 = None
            bus_news2 = None
            
        try:
            pop_news = NewsPostModel.objects.order_by('-views')[0:6]
            pop_news = pop_news.annotate(com=Count('comment'))
        except:
            pop_news = None
            
        try:
            new_com = CommentModel.objects.order_by('-date')[0:8]
        except:
            new_com = None
            
        try:
            comp_news = NewsPostModel.objects.filter(tag__name='Company')[0:4]
            comp_news = comp_news.annotate(com=Count('comment'))
        except:
            comp_news = None
            
        try:
            job_news = NewsPostModel.objects.filter(tag__name='Job')[0:4]
            job_news = job_news.annotate(com=Count('comment'))
        except:
            job_news = None
            
        try:
            ex_news = NewsPostModel.objects.filter(tag__name='Excursion')[0:4]
            ex_news = ex_news.annotate(com=Count('comment'))
        except:
            ex_news = None
            
        try:
            rec_news = NewsPostModel.objects.order_by('-date')[0:2]
            rec_news = rec_news.annotate(com=Count('comment'))
        except:
            rec_news = None

        return render(request, 'main.html', context={
            'user': None if request.user.is_anonymous else request.user,
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

    commentform = CommentForm

    if request.method == 'GET':

        return render(request, 'singlepost.html', context={
            'user': None if request.user.is_anonymous else request.user,
            'time': datetime.now().strftime("%H:%M"),
            'date': date.today().strftime("%B %d, %Y"),
            'post': singlepost,
            'post_com': post_com,
            'coms': coms,

            'pop_news': pop_news,

            'new_com': new_com,

            'rec_news': rec_news,

            'commentform': commentform,
        })

    if request.method == 'POST':
        
        user = None if request.user.is_anonymous else request.user
        
        if user == None:
            return redirect('/login/')

        commentform = CommentForm(request.POST)

        if commentform.is_valid():

            CommentModel.objects.create(
                user=request.user,
                text=commentform.cleaned_data.get('text'),
                post=singlepost,
            )

            return redirect(f'/post{id}')


def post_create_view(request):
    
    user = None if request.user.is_anonymous else request.user
    
    if user.is_superuser == False or user == None:
        return redirect('/')

    pop_news = NewsPostModel.objects.order_by('-views')[0:6]
    pop_news = pop_news.annotate(com=Count('comment'))

    new_com = CommentModel.objects.order_by('-date')[0:8]

    rec_news = NewsPostModel.objects.order_by('-date')[0:2]
    rec_news = rec_news.annotate(com=Count('comment'))

    if request.method == 'GET':

        form = NewsPostForm

        return render(request, 'singlepostform.html', context={
            'user': user,
            'time': datetime.now().strftime("%H:%M"),
            'date': date.today().strftime("%B %d, %Y"),
            'form': form,

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
            'user': None if request.user.is_anonymous else request.user,
            'time': datetime.now().strftime("%H:%M"),
            'date': date.today().strftime("%B %d, %Y"),
            'form': form,

            'pop_news': pop_news,

            'new_com': new_com,

            'rec_news': rec_news,
        })


def post_tag_view(request, slug=None):
    
    page = int(request.GET.get('page', 1))
    tag = None
    posts = NewsPostModel.objects.order_by('-date')[0::] 
    posts = posts.annotate(com=Count('comment'))
    
    if slug:
        tag = get_object_or_404(TagModel, slug=slug)
        posts = posts.filter(tag=tag)
    
    
    max_page = posts.__len__() / PAGINATION_LIMIT
    if max_page > round(max_page):
        max_page = round(max_page) + 1
    else:
        max_page = round(max_page)
    posts = posts[PAGINATION_LIMIT*(page-1):PAGINATION_LIMIT*page]
    
    
    pages = range(1, max_page+1)
    print(pages)
    
    pop_news = NewsPostModel.objects.order_by('-views')[0:6]
    pop_news = pop_news.annotate(com=Count('comment'))
    
    new_com = CommentModel.objects.order_by('-date')[0:8]

    rec_news = NewsPostModel.objects.order_by('-date')[0:2]
    rec_news = rec_news.annotate(com=Count('comment'))
    
    return render(request, 'taglist.html', context={
        'user': None if request.user.is_anonymous else request.user,
        'time': datetime.now().strftime("%H:%M"),
        'date': date.today().strftime("%B %d, %Y"),
        
        'tag': '' if tag==None else tag,
        'posts': posts,
        'pages': pages,
        
        'pop_news': pop_news,
        'new_com': new_com,
        'rec_news': rec_news,
    })
