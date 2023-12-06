from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from .models import Books, Record
from django.shortcuts import render
from django.views import View
import json


# Create your views here.


class LoginView(View):

    def post(self, request):
        """登入接口
            获取参数 （表单/json）

        """
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # params = json.loads(request.body.decode())

        params = request.POST if len(request.POST) else json.loads(request.body.decode())
        username = params.get('username')
        password = params.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'code': 1000, 'message': '登入成功'})
        else:
            return JsonResponse({'code': 2001, 'message': '登入失败,账号或密码错误'})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return JsonResponse({'code': 1000, 'message': '已注销用户登录'})


class BookView(View):
    """图书管理系统接口"""

    def get(self, request):
        """获取图书列表"""
        # 判断用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({'code': 2000, 'message': '认证失败，未登录，没有访问权限'})
        bs = Books.objects.all()
        # data = []
        # for b in bs:
        #     dic = {'id': b.id, 'name': b.name, 'status': b.status}
        #     data.append(dic)
        data = [{'id': b.id, 'name': b.name, 'status': b.status} for b in bs]
        return JsonResponse({'code': 1000, 'message': '获取成功', 'data': data})

    def post(self, request):
        """添加图书"""
        if not request.user.is_authenticated:
            return JsonResponse({'code': 1000, 'message': '认证失败，未登录，没有访问权限'})
        # 获取参数
        params = request.POST if len(request.POST) else json.loads(request.body.decode())
        id = params.get('id')
        name = params.get('name')
        # 参数验证
        # 检验参数是否为空
        if not (id and name):
            return JsonResponse({'code': 2001, 'message': '参数不能为空'})
        # 检验参数类型
        if not isinstance(id, str):
            return JsonResponse({'code': 2001, 'message': 'id参数只能是字符串类型'})
        if not isinstance(name, str):
            return JsonResponse({'code': 2001, 'message': 'name参数只能是字符串类型'})
        # 验证是否存在该id
        try:
            Books.objects.create(id=id, name=name)
        except Exception as e:
            return JsonResponse({'code': 2001, 'message': '该书籍已经存在'})
        else:
            return JsonResponse({'code': 1001, 'message': '添加成功'})

    def delete(self, request):
        """删除图书"""
        # 校验用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({'code': 1000, 'message': '认证失败，未登录，没有访问权限'})
        # 获取参数
        id = request.GET.get('id')
        if not id:
            return JsonResponse({'code': 2001, 'message': '删除书籍id时必填项'})
        # 校验参数是否有效
        try:
            book = Books.objects.get(id=id)
        except Exception as e:
            return JsonResponse({'code': 2001, 'message': '传入书籍id有误'})
        else:
            # 删除图书信息
            book.delete()
            return JsonResponse({'code': 1000, 'message': '删除成功'})


class RecordView(View):
    """出借图书和归还图书"""

    def post(self, request):
        # if request.user.is_authenticated:
        #     return JsonResponse({'code': 2000, 'message': '认证失败，未登录，没有访问权限'})

        params = request.POST if len(request.POST) else json.loads(request.body.decode())
        book_id = params.get('book')
        name = params.get('name')
        if not(book_id and name):
            return JsonResponse({'code': 2001, 'message': '书籍编号和借书人名字不能为空'})
        # 校验书籍编号是否正确
        try:
            book = Books.objects.get(id=book_id)
        except Exception as e:
            return JsonResponse({'code': 2001, 'message': '未找到对应的书籍'})

        # 判断是否可以出借
        if book.status:
            return JsonResponse({'code': 2001, 'message': '该书籍已经借出，请确认书籍编号是否正确'})

        if not isinstance(name, str):
            return JsonResponse({'code': 2001, 'message': '借书人名字的类型必须是字符串'})

        # 借书操作
        with transaction.atomic():
            book.status = True
            book.save()
            Record.objects.create(book=book, name=name)
        return JsonResponse({'code': 1001, 'message': '借书成功'})
