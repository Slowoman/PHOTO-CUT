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

from ImageRecommendationSystem.views  import SearchDataView,MemberView,FocusOnView,ImageInformationView 

from ImageRecommendationSystem.models import HomeBannerModel,MemberModel,FocusOnModel,ImageInformationModel


from ImageRecommendationSystem.models import MemberModel        
        
from django.apps import apps
from django.db.models import Sum,Count


#PC接口使用开始
class MemberCenter(PublicView.PublicView):
    def __init__(self):   
        PublicView.PublicView.__init__(self)
        self.basePath = "{appName}/MemberCenter".format(appName = utlitComm.app_name) 
         #PC端View
        
        self.MemberView = MemberView.Member()
        self.MemberSearchData = SearchDataView.SearchData(MemberModel,MemberModel.Member,pageInfoIndex =  "/" + utlitComm.app_name + "/MemberCenter/Member_listInfo/")
        
        
        self.FocusOnView = FocusOnView.FocusOn()
        self.FocusOnSearchData = SearchDataView.SearchData(FocusOnModel,FocusOnModel.FocusOn,pageInfoIndex =  "/" + utlitComm.app_name + "/MemberCenter/FocusOn_listInfo/")
        
        
        self.ImageInformationView = ImageInformationView.ImageInformation()
        self.ImageInformationSearchData = SearchDataView.SearchData(ImageInformationModel,ImageInformationModel.ImageInformation,pageInfoIndex =  "/" + utlitComm.app_name + "/MemberCenter/ImageInformation_listInfo/")
        
                
    def callMehtod(self,request,message = None):

        if  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "getPersonInfo" ): 
             return  self.getPersonInfo(request)           

        if not request.session.get('frontusername',None):                   
            return  self.login(request)  

        if  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "index" ): 
          
            return  self.index(request)  
	
        
        
	
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "Member/edit" ): 
             return  self.Member_edit(request)          
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "Member/save_edit" ): 
             return  self.Member_save_edit(request)          
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "FocusOn/delete" ): 
             return  self.FocusOn_delete(request)          
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "FocusOn/edit" ): 
             return  self.FocusOn_edit(request)          
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "FocusOn/save_edit" ): 
             return  self.FocusOn_save_edit(request)          
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "FocusOn/search" ): 
             return  self.FocusOn_search(request)          
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "FocusOn/detail" ): 
             return  self.FocusOn_detail(request)          
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "ImageInformation/add" ): 
             return  self.ImageInformation_add(request)          
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "ImageInformation/save_add" ): 
             return  self.ImageInformation_save_add(request)          
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "ImageInformation/delete" ): 
             return  self.ImageInformation_delete(request)          
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "ImageInformation/edit" ): 
             return  self.ImageInformation_edit(request)          
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "ImageInformation/save_edit" ): 
             return  self.ImageInformation_save_edit(request)          
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "ImageInformation/search" ): 
             return  self.ImageInformation_search(request)          
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "ImageInformation/detail" ): 
             return  self.ImageInformation_detail(request)  
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "getPersonInfo" ): 
             return  self.getPersonInfo(request)           
        else:
            return  self.login(request)  
    #登录检查
    def checkLogin(self, request):
        return None
        #print(menuDict)

    def index(self,request):
        if request.session.get('frontusername_is_login',None): 
            return render(request,'MemberCenter/index.html',{'username':request.session['frontusername']})
        else:
            return redirect(reverse('membercenterlogin'))
    
    def Member_edit(self,request):
        return self.MemberView.edit(request)
    
    def Member_save_edit(self,request):
        return self.MemberView.save_edit(request)
    
    def FocusOn_delete(self,request):
        return self.FocusOnView.delete(request)
    
    def FocusOn_edit(self,request):
        return self.FocusOnView.edit(request)
    
    def FocusOn_save_edit(self,request):
        return self.FocusOnView.save_edit(request)
    
    def FocusOn_search(self,request):
        return self.FocusOnView.index(request)
    
    def FocusOn_detail(self,request):
        return self.FocusOnView.detail(request)
    
    def ImageInformation_add(self,request):
        return self.ImageInformationView.add(request)
    
    def ImageInformation_save_add(self,request):
        return self.ImageInformationView.save_add(request)
    
    def ImageInformation_delete(self,request):

        return self.ImageInformationView.delete(request)

    
    def ImageInformation_edit(self,request):
        return self.ImageInformationView.edit(request)
    
    def ImageInformation_save_edit(self,request):
        return self.ImageInformationView.save_edit(request)
    
    def ImageInformation_search(self,request):
        return self.ImageInformationView.index(request)
    
    def ImageInformation_detail(self,request):
        return self.ImageInformationView.detail(request)

    #公开个人资料
    
    def getPersonInfo(self,request):
       
        #基本资料
         MemberId = request.GET.get('MemberId') 
         tableName = "Member"
         searchSonCondition = {"id":MemberId}
         ModelObject = apps.get_model(utlitComm.app_name,tableName)
         curEntryObject = ModelObject.objects.values().filter(**searchSonCondition)[0]
         #没有头像加默认图片
         if curEntryObject["WeChatAvatarPicture"] == '':
            curEntryObject["WeChatAvatarPicture"] =  "Member_p/defaultUserImg.jpg"
         #粉丝
         tableName = "FocusOn"
         searchSonCondition = {"MemberId":MemberId}
         ModelObject = apps.get_model(utlitComm.app_name,tableName)
         infoDetail = ModelObject.objects.values("MemberId").filter(**searchSonCondition).annotate(MemberIdCount=Count("MemberId"))
         FanIdCount = 0
         try:
            FanIdCount = infoDetail[0]["MemberIdCount"]
         except:
            pass
         #关注 FanId
         searchSonCondition = {"FanId":MemberId}
         ModelObject = apps.get_model(utlitComm.app_name,tableName)
         infoDetail = ModelObject.objects.values("FanId").filter(**searchSonCondition).annotate(FanIdCount=Count("MemberId"))
         FocusOnMemberIdCount = 0
         try:
            FocusOnMemberIdCount = infoDetail[0]["FanIdCount"]
         except:
            pass
         
         #图片列表 - #按点击量排名前5
         tableName = "BrowsingHistory"
         searchSonCondition = {"MemberId":MemberId}
         ModelObject = apps.get_model(utlitComm.app_name,tableName)
         infoDetail = ModelObject.objects.values("ImageInformationId").filter(**searchSonCondition).annotate(MemberIdCount=Count("MemberId")).order_by("-MemberIdCount")[:10]
         ImageInformationIdList = []
         for item in infoDetail:
            ImageInformationIdList.append(item["ImageInformationId"])
         if len(ImageInformationIdList) == 10:#作品热度不高，加上最新发布的
            searchSonCondition["id__in"] = ImageInformationIdList

         tableName = "ImageInformation"
         ModelObject = apps.get_model(utlitComm.app_name,tableName)
         ImageInformationList = ModelObject.objects.values().filter(**searchSonCondition).order_by("CreatedTime")
         for item in ImageInformationList:
               
                images = item["ImageLink"].split(";")
                
                item["ImageLink"] = images[0]  
         content = {}
         content["ImageInformationList"] = ImageInformationList

         curEntryObject["FanIdCount"] = FanIdCount
         curEntryObject["FocusOnMemberIdCount"] = FocusOnMemberIdCount
         content["curEntryObject"] = curEntryObject
         print(content)
         return render(request,'MemberCenter/indexPublic.html',context=content)

        #其它资料
      
    def login(self,request):
       
        if request.method=='GET':
            return render(request,'MemberCenter/login.html')
        elif request.method=="POST":
            user=request.POST.get('username')
            pwd=request.POST.get('password')
            
            curAythor = MemberModel.Member.objects.filter(Name = user,Password =pwd)  
                      
            if len(curAythor)>0:
            
                request.session['frontusername']=user   #user的值发送给session里的username
                #权限和菜单数据准备
                #self.genMeunAndRoleAuthorityInfo(request)
                request.session['frontusernameid']= curAythor[0].id 
                request.session['frontusername_is_login']=True   #认证为真
                return redirect(reverse("membercenterindex"))
            else:
                return redirect(reverse("membercenterlogin"))
    
#PC接口使用结束    
    


