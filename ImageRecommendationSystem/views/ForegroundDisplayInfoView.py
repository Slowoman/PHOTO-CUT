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
from ImageRecommendationSystem.views  import utlitComm,PublicView,SearchDataView,ImageInformationView  #view共有函数
from django.urls import path,re_path 
from django.shortcuts import reverse

from ImageRecommendationSystem.models  import ImageInformationModel  #view共有函数"
        
from django.apps import apps
from django.db.models import Sum,Count
import re
import time
#PC端
class  ForegroundDisplayInfo(PublicView.PublicView):
    def __init__(self):    
        PublicView.PublicView.__init__(self)
        self.basePath = "{appName}/ForegroundDisplayInfo".format(appName = utlitComm.app_name) 
        
        self.ImageInformationSearchData = SearchDataView.SearchData(ImageInformationModel,ImageInformationModel.ImageInformation,pageInfoIndex =  "/" + utlitComm.app_name + "/ForegroundDisplayInfo/ImageInformation_listInfo/")

        self.ImageInformationView = ImageInformationView.ImageInformation()
    def callMehtod(self,request,message = None):

        
        if request.path_info == "/{path}/{upName}_{method}/".format(path = self.basePath,upName = "ImageInformation",method =  "detail" ): 
            
            return self.ImageInformation_detail(request)        
        
        if request.path_info == "/{path}/{upName}_{method}/".format(path = self.basePath,upName = "ImageInformation",method =  "listInfo" ): 
            
            return self.ImageInformation_listInfo(request)    
        if request.path_info == "/{path}/{upName}_{method}/".format(path = self.basePath,upName = "ImageInformation",method =  "keywordSearch" ): 
            
            return self.ImageInformation_keywordSearch(request)  

        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "ImageInformation_Action" ): 
             return  self.ImageInformation_Action(request)   
        elif  request.path_info == "/{path}/{method}/".format(path = self.basePath,method =  "ImageInformation_AddComment" ):  
             return  self.ImageInformation_AddComment(request)    
        else:  
            return  self.index(request)  

    def index(self,request):
        
        return  self.ImageInformation_listInfo(request)     
        
         
    
    def ImageInformation_detail(self,request):
         eid=request.GET.get('eid') 
         
         tableName = "ImageInformation"
         searchSonCondition = {"id":eid}
         ImageInformationModelObject = apps.get_model(utlitComm.app_name,tableName)
         curEntryObject = ImageInformationModelObject.objects.values().filter(**searchSonCondition)[0]
         print(curEntryObject)
         MemberId = curEntryObject["MemberId_id"] 
         #图片列表
         images = curEntryObject["ImageLink"].split(";")
         curEntryObject["ImageLink"] = images
         
         
         #图片点赞数据
         tableName = "Likes"
         searchSonCondition = {"ImageInformationId":eid}
         ModelObject = apps.get_model(utlitComm.app_name,tableName)
         Likes = ModelObject.objects.values().filter(**searchSonCondition)
         curEntryObject["LikesCount"] = len(Likes)
         #图片浏览数据
         tableName = "BrowsingHistory"
         ModelObject = apps.get_model(utlitComm.app_name,tableName)
         BrowsingHistory = ModelObject.objects.values().filter(**searchSonCondition)
         curEntryObject["BrowsingHistoryCount"] = len(BrowsingHistory)

         #评论数据
         tableName = "Comment"
         CommentModelObject = apps.get_model(utlitComm.app_name,tableName)
         Comment = CommentModelObject.objects.values().filter(**searchSonCondition)
         curEntryObject["CommentCount"] = len(Comment)

         #评论用户数据
         CommentMemeberIds = []
         for item in Comment:
             CommentMemeberIds.append(item["MemberId_id"])
         #作者Id
         CommentMemeberIds.append(curEntryObject["MemberId_id"])
         tableName = "Member"
         ModelObject = apps.get_model(utlitComm.app_name,tableName)
         CommentMemeberIdInfo = ModelObject.objects.values().filter(**{"id__in":CommentMemeberIds})
         CommentMemeberIdInfoDict = {}
         for item in CommentMemeberIdInfo:
             CommentMemeberIdInfoDict[item["id"]] = item["WeChatAvatarPicture"]
         #更新个人评论点赞数据
         tableName = "CommentLikes"
         ModelObject = apps.get_model(utlitComm.app_name,tableName)
         CommentLikes = ModelObject.objects.values("MemberId").filter(**searchSonCondition).annotate(MemberIdCount=Count("MemberId"))
         memberCommentCount = {} 
         for item in CommentLikes:
             memberCommentCount[item["MemberId"]] = item["MemberIdCount"]
             
         print(memberCommentCount) 
         print(CommentMemeberIdInfoDict)   
         for item in Comment:
            if item["MemberId_id"] in memberCommentCount.keys():
                item["MemberIdCount"] = memberCommentCount[item["MemberId_id"]]
            else:
                item["MemberIdCount"] = 0

            item["WeChatAvatarPicture"] = CommentMemeberIdInfoDict[item["MemberId_id"]]

         #作者图片
         print(curEntryObject)
         curEntryObject["WeChatAvatarPicture"] = CommentMemeberIdInfoDict[curEntryObject["MemberId_id"]]
         #没有头像加默认图片
         if curEntryObject["WeChatAvatarPicture"] == '':
            curEntryObject["WeChatAvatarPicture"] =  "Member_p/defaultUserImg.jpg"
         curEntryObject =  utlitComm.updateHardCodeFieldValue(ImageInformationModelObject,curEntryObject)

         Comment = utlitComm.updatedPageInfo(CommentModelObject,Comment) 
         #标签处理
         ImageTags = curEntryObject["ImageTags"]
         #ImageTagsList = re.findall("(#.+#)",ImageTags)
         ImageTagsList = ImageTags.split("\n")
         ImageTagsListT = []
         for item in ImageTagsList:
             itemT = item.replace("\n","")
             if itemT.strip() != '':
                    ImageTagsListT.append(itemT)
         print(ImageTagsListT)

         curEntryObject["ImageTags"] = ImageTagsListT
         content = {}
         curEntryObject["CreatedTime"] = curEntryObject["CreatedTime"][:10]
         content["Comment"] = Comment
         content["curEntryObject"] = curEntryObject

         bannerList = []

         for index  in range(len(curEntryObject["ImageLink"])):
             bannerList.append({"picAddress":curEntryObject["ImageLink"][index],"index":index})

         content["bannerList"] = bannerList

         #增加点击记录
         tableName = "BrowsingHistory"
         ModelObject = apps.get_model(utlitComm.app_name,tableName)
         ImageInformationId = apps.get_model(utlitComm.app_name,"ImageInformation").objects.get(id=eid)
         
         #得到点击次数
         browseCount = 0
         try:
            browseCount = ModelObject.objects.values("ImageInformationId").filter(**{"ImageInformationId":eid})\
         .annotate(ImageInformationIdCount =Count("ImageInformationId"))\
         .order_by("-ImageInformationIdCount")[0]["ImageInformationIdCount"]
         except:
            pass

         content["browseCount"] = browseCount
         MemberId = request.session.get("frontusernameid")
         if MemberId:
                MemberId = apps.get_model(utlitComm.app_name,"Member").objects.get(id = MemberId) 
         CreatedTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) 

         BrowsingHistoryDict = {"CreatedTime":CreatedTime,"ImageInformationId":ImageInformationId}
         if MemberId:
            BrowsingHistoryDict['MemberId'] = MemberId
         print(BrowsingHistoryDict)
         ModelObject.objects.create(**BrowsingHistoryDict) 

         return render(request,'ForegroundDisplayInfo/ImageInformation/detail.html',context=content)           
        
         
    def ImageInformation_listInfo(self,request):
         inputParametersDict,pn = self.ImageInformationSearchData.getSearchParametersDict(request)
         content= self.ImageInformationSearchData.getSearchJosnData(inputParametersDict,pn) 
         
         return render(request,'ForegroundDisplayInfo/ImageInformation/search.html',context=content)        
    
    def ImageInformation_Action(self,request):
        return self.ImageInformationView.ImageInformationAction(request)
    def ImageInformation_AddComment(self,request):
        return self.ImageInformationView.ImageInformationAddComment(request)  
    def ImageInformation_keywordSearch(self,request):
         return self.ImageInformationView.keywordSearch(request)      
                 



