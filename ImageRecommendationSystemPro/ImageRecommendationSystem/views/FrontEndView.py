from django.shortcuts import render, redirect
#引用的model清单，包括外键和本身

import datetime
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
import os
from ImageRecommendationSystemPro.settings import * #项目设置

from django.views import View
from django.http import Http404
from ImageRecommendationSystem.views  import utlitComm,PublicView  #view共有函数
from django.urls import path,re_path 
from django.shortcuts import reverse

from ImageRecommendationSystem.views  import SearchDataView,MemberView 

from ImageRecommendationSystem.models import HomeBannerModel,MemberModel





#PC接口使用开始
class FrontEnd(PublicView.PublicView):
    def __init__(self):   
        PublicView.PublicView.__init__(self)
        self.basePath = "{appName}/FrontEnd".format(appName = utlitComm.app_name) 
         #PC端View
        
        self.MemberView = MemberView.Member()
        self.MemberSearchData = SearchDataView.SearchData(MemberModel,MemberModel.Member,pageInfoIndex =  "/" + utlitComm.app_name + "/FrontEnd/Member_listInfo/")
        
                
    def callMehtod(self,request,message = None):

        if  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "index" ): 
          
            return  self.index(request)  
	
	
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "Member/add" ): 
             return  self.Member_add(request)          
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "Member/save_add" ): 
             return  self.Member_save_add(request)            
        else:
            return  self.login(request)  
    #登录检查
    def checkLogin(self, request):
        return None
        #print(menuDict)

    def index(self,request):
        if request.session.get('frontusername_is_login',None): 
            return render(request,'FrontEnd/index.html',{'username':request.session['frontusername']})
        else:
            return redirect(reverse('frontendlogin'))
    
    def Member_add(self,request):
        return self.MemberView.add(request)
    
    def Member_save_add(self,request):
        return self.MemberView.save_add(request)
        
#PC接口使用结束    
    


