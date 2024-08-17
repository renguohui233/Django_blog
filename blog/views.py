from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy,reverse
from .models import BlogCategory, Blog, BlogComment
from django.views.decorators.http import require_http_methods,require_POST
from .forms import PublishBlogForm
from django.http.response import JsonResponse
from django.db.models import Q


# Create your views here.


def index(request):
    blogs = Blog.objects.all()

    return render(request, 'index.html', {'blogs': blogs})


def details(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        blog = None
    
    return render(request, 'blog_detail.html',context={'blog':blog})


@require_http_methods(['GET', 'POST'])
@login_required(login_url=reverse_lazy('hauth:login'))
def publish(request):
    if request.method == 'GET':
        category_name = BlogCategory.objects.all()
        contexts = {
            'category_name': category_name
        }
        return render(request, 'pub_blog.html', context=contexts)
    else:
        form = PublishBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            category_id = form.cleaned_data['category']
            blog = Blog.objects.create(title=title, content=content, category_id=category_id,
                                author=request.user)
            return JsonResponse({'code': 200, 'msg': '博客发布成功',"data":{"blog_id":blog.id}})
        else:
            print(form.errors)
            return JsonResponse({'code': 400, 'msg': '参数错误'})

@require_POST
@login_required(login_url=reverse_lazy('hauth:login'))
def pub_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComment.objects.create(blog_id=blog_id, content=content,author=request.user)
    return redirect(reverse('blog:details',kwargs={"blog_id":blog_id}))


def search(request):
    # /search?q=xxx
    q = request.GET.get('q')
    blogs = Blog.objects.filter(Q(title__icontains=q)|Q(content__icontains=q)).all()
    return render(request,'index.html',context={"blogs":blogs})