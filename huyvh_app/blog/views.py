from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#define lid for webservice using rest
from rest_framework import viewsets
from .serializers import PostSerializer
from django.core import serializers

# Create method by Huyvh date 21/082015 using Django FW


# def index(request):
#     return HttpResponse("Hello!")


# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)


# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)


# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)

# get list Blog
def blog_list(request):
        # get all data to DB using view
    #posts = Post.objects.all()
    posts = Post.objects.order_by('-published_date')
    paginator = Paginator(posts, 10) # Show 10 contacts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    #posts =Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    context = {'posts': posts}
    return render(request, 'blog/blog_list.html', context)

 # define using form in Django
def post_new(request):
    if request.method =="POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
           post = form.save(commit=False)
           post.author = request.user
           post.published_date = timezone.now()
           post.imgfile = request.FILES['imgfile']
           post.save()
           return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
# define post detail
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
#define post edit
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES ,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.imgfile = request.FILES['imgfile']
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# define methosd publish webservice using REST by HuyVH
class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Post.objects.all().order_by('-published_date')
    serializer_class = PostSerializer

# define moethod list call ws api
def blog_client(request):
    return render(request, 'blog/post_client.html',  {'' : ''})