#_*_coding:utf-8
from django.shortcuts import render
from blog import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required#登陆后才能进入系统的模块
from blog import utils
from django.views.decorators.csrf import csrf_exempt
import  json

def acc_login(request):
    login_err = ''
    if request.method == 'POST':
        username = request.POST.get('inputUsername')
        password = request.POST.get('inputPassword')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            if user.is_active:
                return HttpResponseRedirect('/')
        login_err = "请检查用户名和密码是否正确"
    return render(request, 'login.html', {
        'login_err': login_err
    })

def acc_logout(request):
    logout(request)
    return  HttpResponseRedirect("/")

def index(request):
    articles = models.Article.objects.all().order_by('-publish_date')[0:5]  #获取文章列表并按时间排序
    return render(request,'index.html',{
        'articles': articles,
    })

def linuxyw(request):
    articles = models.Article.objects.filter(type='Linux运维').order_by('-publish_date')
    paginator =Paginator(articles,15)  # Show 10 contacts per page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request,'linuxyw.html',{
        'articles': articles,
    })

def pythonyw(request):
    articles = models.Article.objects.filter(type='Python编程').order_by('-publish_date')
    paginator =Paginator(articles,10)  # Show 10 contacts per page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request,'linuxyw.html',{
        'articles': articles,
    })

def aboutme(request):
    articles = models.Article.objects.all().order_by('-publish_date')[0:5]  # 获取文章列表并按时间排序
    return render(request,'aboutme.html',locals())

def article(request,id=None):
    articles = models.Article.objects.all().order_by('-publish_date')[0:5]  # 获取文章列表并按时间排序
    id_article = get_object_or_404(models.Article, pk=request.GET.get('id'))
    return render(request, 'article.html',locals())

@login_required
def create_blog(request):
    error = ''
    articles = models.Article.objects.all().order_by('-publish_date')[0:5]  # 获取文章列表并按时间排序
    Categorys=models.Category.objects.all()
    if request.method == "GET":
        return render(request, 'create_blog.html', {'articles':articles ,'Categorys':Categorys})
    elif request.method == 'POST':
        if request.POST.get('title') == '':
            error = '文章标题不能为空'
            return render(request, 'create_blog.html', {'articles': articles,'error':error})
        else:
            try:
                if models.Article.objects.get(title=request.POST.get('title')) != '':
                    error = '文章标题已经创建，请选择其它标题'
                    return render(request, 'create_blog.html', {'articles': articles, 'error': error})
            except:
                pass
        if request.POST.get('summary') == '':
            error = '文章简介不能为空'
            return render(request, 'create_blog.html', {'articles': articles,'error':error})
        if request.POST.get('content') == '':
            error = '内容不能为空'
            return render(request, 'create_blog.html', {'articles': articles,'error':error})
        Article = utils.ArticleGen(request)
        res = Article.create()
        html_ele = '''New article <<a href="/article/?id=%s">%s</a>>
             has been created successfully! ''' % (res.id, res.title)
        return HttpResponse(html_ele)

def search(request):
    articles = models.Article.objects.filter(title__icontains=request.POST.get('search'))
    # articles = models.Article.objects.all().filter(title__contains=request.POST.get('search'))
    return render(request, 'search.html', locals())

@csrf_exempt  #屏蔽跨站检测
def test(request):
    if request.method == 'POST' :
        # data= [  "{value:335, name:'直接访问'}",
        #         "{value:310, name:'邮件营销''}",
        #         "{value:234, name:'联盟广告'}",
        #         "{value:135, name:'视频广告'}",
        #         "{value:1548, name:'搜索引擎'}"]
        data=[]
        print json.dumps(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return render(request,'test.html', locals())