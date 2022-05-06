from django.shortcuts import render, redirect
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
from django.db.models import Sum,Count

import datetime
from ImageRecommendationSystem.models  import ImageInformationModel
from django.apps import apps
from django.db.models import Sum,Count

#PC接口使用开始
class FrontEndIndex(PublicView.PublicView):
    def __init__(self):    
        PublicView.PublicView.__init__(self)
        self.basePath = "FrontEndIndex"
        self.detailHtmlPath = "{}/index.html".format(self.basePath)
        
    def callMehtod(self,request,message = None):

        if  request.path_info.find("/{appName}/{path}/{method}/".format(appName = utlitComm.app_name,path =  self.basePath,method = "logout" ))==0:
            return self.logout(request)
        else:
            return self.index(request)
        
    def index(self,request):
         #组装首页数据
         content =self.indexDataMix(request)

         return render(request,self.detailHtmlPath,context=content)
    def indexDataMix(self,request):
        content = {
	
        "ImageInformationList":self.getImageInformationList(),
        "getImageInformationRecommendList":self.getImageInformationRecommendList(request)
        
         }
        return content 
    def indexResponseData(self,request):
         #组装首页数据
        content = self.indeDataMix()
        return HttpResponse(content)      
    #得到首页展现数据
   
     	
    def getImageInformationList(self):
       
        curObjList = ImageInformationModel.ImageInformation.objects.values(  'id','ImageTypeId', 'Name','MemberId','ImageLink').order_by('-id')[:5.0] 
        
        #分割图片

        for item in curObjList:
               
                images = item["ImageLink"].split(";")
                
                item["ImageLink"] = images[0]  

        curObjList = utlitComm.updatedPageInfo(ImageInformationModel.ImageInformation,curObjList)   
        print(curObjList)  

        return curObjList         
        
    def getImageInformationRecommendList(self,request):
        
        #用户没有登录就那点击量最高的前5
        tableName = "BrowsingHistory"
        ModelObject = apps.get_model(utlitComm.app_name,tableName)
        BrowsingHistory = ModelObject.objects.values("ImageInformationId").annotate(MemberIdCount=Count("ImageInformationId")).order_by("-MemberIdCount")[:5.0]
        idListNormal = [item["ImageInformationId"] for item in BrowsingHistory]
        print("idListNormal:")
        print(idListNormal)
        #如有登录按协同推荐拿前5，如果协同没有数据，也拿总点击前5
        cfr = utlitComm.CollaborativeFilteringRecommendation()
        memberId = request.session.get("frontusernameid")
        recommend = cfr.recommend(memberId)
        print("recommm: crf")
        print(recommend)
        i = 0
        idList = []
        for item in recommend:
            idList.append(item[0])
            if (i>10):
                break
            i += 1
        print("recommm:")
        print(idList)
        if len(idList)<5:
             idList = idListNormal  
             
        if len(idList) >0:
                ModelObject = apps.get_model(utlitComm.app_name,"ImageInformation")
                curObjList = ModelObject.objects.values().filter(**{"id__in":idList})
        else:
                curObjList = None
            
        #分割图片
        if curObjList:
            for item in curObjList:
                   
                    images = item["ImageLink"].split(";")
                    
                    item["ImageLink"] = images[0]  

            curObjList = utlitComm.updatedPageInfo(ImageInformationModel.ImageInformation,curObjList)   
        print(curObjList)  

        return curObjList         
        

    def logout(self,request): 
        
        try:
            request.session['frontusername'] = '' #删除登录信息
        except:
            pass

        try:
             request.session['frontusernameid'] = '' #删除登录信息
        except:
            pass

        try:

            request.session['frontusername_is_login'] = '' #删除登录信息
        except:
            pass    
        return redirect(reverse('frontendindexindex'))


#PC接口使用结束   












