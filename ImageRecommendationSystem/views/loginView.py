from django.shortcuts import render,redirect,HttpResponse
from django.shortcuts import render, redirect
#引用的model清单，包括外键和本身
#from ImageRecommendationSystem.models import AuthorModel

import datetime
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
import os
from ImageRecommendationSystemPro.settings import * #项目设置

from django.views import View
from django.http import Http404
from ImageRecommendationSystem.views  import utlitComm,PublicView #view共有函数
from django.urls import path,re_path 
from django.shortcuts import reverse

from django.utils.decorators import method_decorator # 在类试图中对函数进行添加装饰器使用
from django.views import View

from ImageRecommendationSystem.models import SystemAccountModel

                    
# 为全部请求方法添加装饰器
class Login(PublicView.PublicView):
    def __init__(self):
        PublicView.PublicView.__init__(self)
        self.basePath = "{appName}/admin/Login/".format(appName = utlitComm.app_name) 
            
    def callMehtod(self,request,message = None):
        returnValue = super().callMehtod(request,message)
        #三种结果：已登录，无权限；未登录（当然没有权限）；已登录，有权限；
        print(request.path_info)
        print("/{path}{method}/".format(path = self.basePath,method = "register" ))
        if request.path_info == "/{path}{method}/".format(path = self.basePath,method = "register" ):
            return self.register(request)
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "index" ):
            return self.index(request)
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method =  "login" ):
            return self.login(request)
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "logout" ):
            return self.logout(request) 
        else:
            return self.login(request)

    #登录检查
    def checkLogin(self, request):
        return None
        
    def login(self,request):
       
        if request.method=='GET':
            return render(request,'admin/Login/login.html')
        elif request.method=="POST":
            user=request.POST.get('username')
            pwd=request.POST.get('password')
            
            systemAccount = SystemAccountModel.SystemAccount.objects.filter(Name = user,Password =pwd) 
            print(systemAccount)            
            if len(systemAccount)>0:
                if request.POST.get('box')=="1":   #checkbox被按下
                    request.session.set_expiry(10)  #session认证时间为10s，10s之后session认证失效
                request.session['userid']= systemAccount[0].id
                request.session['username']=user   #user的值发送给session里的username
  
                request.session['is_login']=True   #认证为真
                return redirect(reverse('index'))
                
            else:
                return redirect(reverse('login'))


    def index(self,request):
        username = ""
        try:
                username =request.session['username']
        except:
                pass
        if username != '' and request.session.get('is_login',None):  #若session认证为真
            
            return render(request,'admin/Login/index.html',{'username':request.session['username']})
        else:
            return redirect(reverse('login'))

    def logout(self,request):                 #撤销
        del request.session["username"]        #删除session里的全部内容
        return redirect(reverse('login'))
        
    def register(self,request): 
        content = {
            "err_name":"",
            "err_email":"",
            "err_password":"",
            "err_confirm_password":"", 
            "err":"",      
            }                #撤销
        if request.method=='GET':
            return render(request,'admin/Login/register.html')
        elif request.method=="POST":
            #增加用户，进入登录页面

            user=request.POST.get('username')
            pwd=request.POST.get('password')
            
            confirm_password = request.POST.get('confirm_password')
            #保存数据 -todo
            #成功后重新登录系统
            
            return redirect(reverse('login'))
