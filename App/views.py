from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from App.models  import *
import datetime
from django.db.models import Q
from App.extensions.auth import *

# Create your views here.


# def music_add(request):
#    music_typename = ['轻音乐', '民谣', '摇滚', '纯音乐', '动漫', '古典']
   # for i in music_typename:
   #     MusicType.objects.create(type_name=i)
   # return HttpResponse('添加成功！')

   # for i in range(11,30):
   #     Music.objects.create(music_name=f'歌曲-{i}',singer=f'张三{i}',longtime=datetime.timedelta(minutes=4,seconds=30),music_type_id=i%6+1)
   # return HttpResponse('添加成功！')

#分页功能
def paginate(request):
    page_number = request.GET.get('page', 1)
    per_page = 5
    all_data = Music.objects.all()
    paginator = Paginator(all_data,per_page)
    current_page = paginator.page(page_number)
    music_data = [
        {
            'name': music.music_name,
            'id': music.music_id,
            'author': music.singer,
            'duration': music.longtime,
            'description': music.description,
            'type':music.music_type.type_name
        } for music in current_page
    ]
    return JsonResponse({'music_list': music_data})

#按名字，种类，作者查询功能
def search_music(request):
    music_type = request.GET.get('type',None)
    music_singer = request.GET.get('singer',None)
    music_name = request.GET.get('name',None)
    if music_name:
        results = Music.objects.filter(music_name__icontains=music_name)
    if music_type:
        musictype = MusicType.objects.get(type_name__icontains=music_type)
        results = Music.objects.filter(music_type=musictype)
    if music_singer:
        results = Music.objects.filter(singer__icontains=music_singer)
    music_list = [
        {
            'name': music.music_name,
            'id': music.music_id,
            'author': music.singer,
            'duration': music.longtime,
            'description': music.description,
            'type':music.music_type.type_name
        } for music in results
    ]

    return JsonResponse({'music_list': music_list})

#根据id展示相应id的收藏表
class usercollect(View):
    def get(self,request,*args, **kwargs):
        user = request.jwt_payload.get('userid')
        page_number = request.GET.get('page',1)
        per_page = 5
        uid = User.objects.get(User_id=user)
        all_data = uid.collect.all()
        paginator = Paginator(all_data, per_page)
        current_page = paginator.page(page_number)
        collectlist =[
            {
                'name': music.music_name,
                'id': music.music_id,
                'author': music.singer,
                'duration': music.longtime,
                'description': music.description,
                'type':music.music_type.type_name

            } for music in current_page
        ]
        return JsonResponse({'collect_list':collectlist})

#根据id和曲目id添加相应的收藏表
def add_collect(request):

    music_collect = request.GET.get('music_id')
    user = request.jwt_payload.get('userid')
    collectmusic = Music.objects.get(music_id=music_collect)
    collect_user = User.objects.get(User_id=user)
    if collect_user.collect.filter(music_id=music_collect):
        return HttpResponse('该曲目已收藏')
    else:
        collect_user.collect.add(collectmusic)
        return HttpResponse('收藏成功')

#根据id和曲目id删除相应的收藏表
def dele_collect(request):
    music_collect = request.GET.get('music_id')
    user = request.jwt_payload.get('userid')
    collect_user = User.objects.get(User_id=user)
    if collect_user.collect.filter(music_id=music_collect):
        collect_user.collect.filter(music_id=music_collect).delete()
        return HttpResponse('该曲目已移除')
    else:
        return HttpResponse('该曲目不存在')

#注册（前端返回用户名与密码，后端在User数据库里添加）
# 'django.middleware.csrf.CsrfViewMiddleware',需要setting里注释这段话，或者前端{% csrf_token %}
def register_user(request):
    # data = request.json()
    username = request.POST.get('username')
    password = request.POST.get('password')
    if User.objects.filter(User_name=username).exists():
        return JsonResponse({'message': '该用户已存在'})
    else:
        User.objects.create(User_name=username,Password=password)
        return JsonResponse({'message': '创建成功'})


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    users = User.objects.filter(User_name=username,Password=password)
    if users.exists():
        response = JsonResponse({'message': '登录成功','User_name':username})
        user = users.first()
        response.set_cookie('userid', user.User_id, max_age=3600)
        return response
    else:
        return JsonResponse({'message': '密码或户名错误'})

#JWT实现登陆

# @method_decorator(JwtQueryParamMiddleware,name='dispatch')
class LoginView(View):
    def post(self, request, *args, **kwargs):
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        users = User.objects.filter(User_name=user, Password=pwd)

        if users.exists():
            user = users.first()
            token = create_token({'userid': user.User_id})
            return JsonResponse({'status': True, 'token': token})

        else:
            return JsonResponse({'status': False, 'error': '用户名或密码错误'})