from django.shortcuts import render,redirect,HttpResponse
from django.shortcuts import render, redirect
#引用的model清单，包括外键和本身

import datetime
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
import os
from ImageRecommendationSystemPro.settings import * #项目设置

from django.views import View
from django.http import Http404
from ImageRecommendationSystem.views  import utlitComm #view共有函数
from django.urls import path,re_path 
from django.shortcuts import reverse

from django.utils.decorators import method_decorator # 在类试图中对函数进行添加装饰器使用
from django.views import View

from django.apps import apps

from django.http import JsonResponse
import re
import time
from urllib import parse
from pathlib import Path
import xlrd
import json
from django.db import transaction
from django.db.models import Sum,Count
import jieba
###############################################                                   公共视图类开始          ####################################### 
# 为函数视图准备的装饰器
class EntryViewBaseTop():
    def __init__(self,entryModel,entryObject,entryName,foreignkeyTableList,entryNameChinese,viewType = "View",sonTableList = {}):
        #PublicViewWX.__init__(self)
        self.viewType  = viewType
         
        self.entryModel = entryModel
        self.entryObject =   entryObject
        self.entryName = entryName        
        self.foreignkeyTableList = foreignkeyTableList
        self.needCheckAuthority = True
        self.setPath()
        #装饰方法清单
        self.method_decorator_list = []
        #字段检查清单
        self.fieldDataCheckDict = self.fieldDataCheckDict()
        #日志
        self.entryNameChinese = entryNameChinese
        self.logProcess = LogProcess()
    #前台数据收集路径处理
        self.sonTableList = sonTableList

    def frontEndPathUpdate(self,request):
        path_info = request.path_info

        if path_info.find("FrontEnd/Member/") >0: 
            self.setSpecPath(upName = "FrontEnd",entryName = "Member")
            
        
        if path_info.find("MemberCenter/Member/") >0: 
            self.setSpecPath(upName = "MemberCenter",entryName = "Member")
            
        
        if path_info.find("MemberCenter/FocusOn/") >0: 
            self.setSpecPath(upName = "MemberCenter",entryName = "FocusOn")
            
        
        if path_info.find("MemberCenter/ImageInformation/") >0: 
            self.setSpecPath(upName = "MemberCenter",entryName = "ImageInformation")
            
        
                                        
    def fieldDataCheckDict(self):
        pass
    #检查字段内容格式的合法性
    def checkContentValid(self,checkContentDict,checkModel = None): 
        message = {"flag":0,"errorMessage":""}       
        valid = True
        fieldDataCheckDict = self.entryModel.fieldDataCheckDict #默认检查当前view的model
        if  checkModel:#外部指定Mode
            fieldDataCheckDict = checkModel.fieldDataCheckDict

        for key,value in checkContentDict.items(): #收集值

            if key in fieldDataCheckDict.keys():#实体字段需要检测清单
               
                checkType =  fieldDataCheckDict[key]["checkType"]   
                regExpress = utlitComm.publicRegDict[checkType]["regExpress"]            
                find =False
                find = re.findall(regExpress,value)
                
                if valid == False:
                    message["flag"] = 1
                    message["errorMessage"] = "{}【{}】格式不对，应为【{}】，请检查!".format(fieldDataCheckDict[key]["FieldChineseName"],value,checkType)
                    break
                    
        return message          
    def chaneNeedCheckAuthority(self, needCheckAuthority):
        self.needCheckAuthority = needCheckAuthority
    def chaneBasePath(self, basePath):
        self.basePath = basePath        
    #一些路径设置
    def setPath(self):
        self.systemLogin = ""
        self.entryIndex = "{entryName}index".format(entryName = self.entryName).lower()
        self.basePath = "{appName}/admin/{entryName}/".format(appName = utlitComm.app_name,entryName = self.entryName)
        
        self.indexHtmlPath = 'admin/{entryName}/index.html'.format(entryName = self.entryName)
        self.addHtmlPath = 'admin/{entryName}/add.html'.format(entryName = self.entryName.lower())
        self.editHtmlPath = 'admin/{entryName}/edit.html'.format(entryName = self.entryName.lower())
        self.vedioHtmlPath = 'admin/{entryName}/vedioTest.html'.format(entryName = self.entryName.lower())
        self.detailHtmlPath = 'admin/{entryName}/detail.html'.format(entryName = self.entryName.lower())
        
        self.deletePath = "admin//{entryName}/index/".format(entryName = self.entryName)
        
        self.pageInfoIndex = "/{basePath}index/".format(basePath = self.basePath)   
        
        self.startPage = "login"
    def setSpecPath(self,upName,entryName,indexIsSearch = True):
        self.systemLogin = ""
        self.entryIndex = "{upName}{entryName}search".format(upName = upName,entryName = entryName).lower()
        if upName == entryName + "Center":
            self.entryIndex = "{upName}index".format(upName = upName.lower())
        if upName == "FrontEnd":
            self.entryIndex = "frontendindexindex"
        self.basePath = "{appName}/{upName}/{entryName}/".format(appName = utlitComm.app_name,upName = upName,entryName = entryName)
        
        self.indexHtmlPath = '{upName}/{entryName}/index.html'.format(upName = upName,entryName = entryName)
        self.addHtmlPath = '{upName}/{entryName}/add.html'.format(upName = upName,entryName = entryName)
        self.editHtmlPath = '{upName}/{entryName}/edit.html'.format(upName = upName,entryName = entryName)
        self.vedioHtmlPath = '{upName}/{entryName}/vedioTest.html'.format(upName = upName,entryName = entryName)
        self.detailHtmlPath = '{upName}/{entryName}/detail.html'.format(upName = upName,entryName = entryName)
        
        self.deletePath = "{upName}/{entryName}/index/".format(upName = upName,entryName = entryName)
        
        self.pageInfoIndex = "/{basePath}index/".format(basePath = self.basePath)  
        if indexIsSearch:
            self.indexHtmlPath = '{upName}/{entryName}/search.html'.format(upName = upName,entryName = entryName)
            
        self.startPage = "frontendindexindex" 
        self.UserCenterIndex = "{upName}index".format(upName = upName.lower())
    def errInfoProcess(self,request,message):
        #显示错误信息
        errorInfo = ErrorInfo()
        return errorInfo.showErroInfo(request,message,self)
    #登录检查
    def checkLogin(self, request):
        pass
    #权限检查
    def  SystemRolePermissionsCheck(self, request):
         pass

   ####################################            
    def callMehtod(self,request,message = None):
        print("callMehtod")


        self.frontEndPathUpdate(request)
            
        if self.startPage == "frontendindexindex": 
            if not request.session.get('frontusername',None) and len(re.findall(".+FrontEnd.+/add",request.path_info)) == 0:   #前台没有登录且不是用户注册                
                return  redirect(reverse("frontendindexindex"))  
        else:
            if not request.session.get('username',None):                   
                return  redirect(reverse("login"))   
                                 
        returnValue = ""   
        
        self.frontEndPathUpdate(request)
            
        if request.session.get('frontusername_is_login',None) and returnValue !=  "AuthorityChecked" : #不满足【已登录，有权限】
               pass
        elif request.session.get('frontusername_is_login',None) and  len(re.findall("/(search)",request.path_info))>0 : #不满足【已登录，有权限】
               pass               
        elif not request.session.get('frontusername_is_login',None) and len(re.findall("FrontEnd(.+)add",request.path_info))>0 : #不满足【已登录，有权限】
               pass
        elif request.session.get('is_login',None) and returnValue !=  "AuthorityChecked" : #不满足【已登录，有权限】 request.session.get('is_login',None) 
               return returnValue  
        
           
        if (request.path_info == "/{path}{method}/".format(path = self.basePath,method = "index" )) or (request.path_info == "/{path}{method}/".format(path = self.basePath,method = "search" )):
            return self.index(request)     

           
        if request.path_info == "/{path}{method}/".format(path = self.basePath,method = "index" ):
            return self.index(request)
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "add" ):
            return self.add(request)
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method =  "save_add" ):
            return self.save_add(request)
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "edit" ):
            return self.edit(request)   
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method =  "save_edit" ):
            return self.save_edit(request)
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "delete" ):
            return self.delete(request)   
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "delete_all" ):        
            return self.delete_all(request) 
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "detail" ):       
            return self.detail(request)   
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "import_excel" ):        
            return self.import_excel(request)           
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "export_excel" ):      
            return self.export_excel(request) 
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "download_excel" ):        
            return self.download_excel(request)    
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "getFSInfo" ):        
            return self.getFSInfo(request)     
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "getInfo" ):        
            return self.getInfo(request)                                                                                                                                         
        else:
            if self.viewType == "View":
                return redirect(reverse(self.startPage))  #return self.index(request)
            else:
                return Response({'status':0, "msg":"操作成功","data":context,"gotoUrl":reverse(self.startPage)})

###############################################                                   公共视图类开始          ####################################### 
# 为函数视图准备的装饰器
class EntryViewBaseTop():
    def __init__(self,entryModel,entryObject,entryName,foreignkeyTableList,entryNameChinese,viewType = "View",sonTableList = {}):
        #PublicViewWX.__init__(self)
        self.viewType  = viewType
         
        self.entryModel = entryModel
        self.entryObject =   entryObject
        self.entryName = entryName        
        self.foreignkeyTableList = foreignkeyTableList
        self.needCheckAuthority = True
        self.setPath()
        #装饰方法清单
        self.method_decorator_list = []
        #字段检查清单
        self.fieldDataCheckDict = self.fieldDataCheckDict()
        #日志
        self.entryNameChinese = entryNameChinese
        self.logProcess = LogProcess()
    #前台数据收集路径处理
        self.sonTableList = sonTableList

    def frontEndPathUpdate(self,request):
        path_info = request.path_info

        if path_info.find("FrontEnd/Member/") >0: 
            self.setSpecPath(upName = "FrontEnd",entryName = "Member")
            
        
        if path_info.find("MemberCenter/Member/") >0: 
            self.setSpecPath(upName = "MemberCenter",entryName = "Member")


        if path_info.find("FrontEnd/Member/") >0: 
            self.setSpecPath(upName = "FrontEnd",entryName = "Member")
        
        if path_info.find("MemberCenter/Member/") >0: 
            self.setSpecPath(upName = "MemberCenter",entryName = "Member")
        
        if path_info.find("MemberCenter/FocusOn/") >0: 
            self.setSpecPath(upName = "MemberCenter",entryName = "FocusOn")
        
        if path_info.find("MemberCenter/ImageInformation/") >0: 
            self.setSpecPath(upName = "MemberCenter",entryName = "ImageInformation")
                    
        
                                        
    def fieldDataCheckDict(self):
        pass
    #检查字段内容格式的合法性
    def checkContentValid(self,checkContentDict,checkModel = None): 
        message = {"flag":0,"errorMessage":""}       
        valid = True
        fieldDataCheckDict = self.entryModel.fieldDataCheckDict #默认检查当前view的model
        if  checkModel:#外部指定Mode
            fieldDataCheckDict = checkModel.fieldDataCheckDict

        for key,value in checkContentDict.items(): #收集值

            if key in fieldDataCheckDict.keys():#实体字段需要检测清单
               
                checkType =  fieldDataCheckDict[key]["checkType"]   
                regExpress = utlitComm.publicRegDict[checkType]["regExpress"]            
                find =False
                find = re.findall(regExpress,value)
                
                if valid == False:
                    message["flag"] = 1
                    message["errorMessage"] = "{}【{}】格式不对，应为【{}】，请检查!".format(fieldDataCheckDict[key]["FieldChineseName"],value,checkType)
                    break
        if message["flag"] == 0:
              message = self.checkFieldContent(checkContentDict)   
        print(message)     
        return message   
    #检查字段内容唯一性
    def checkFieldContent(self,checkContentDict):
        print(checkContentDict)
        message = {"flag":0,"errorMessage":""}   
        if self.entryName == "Member":
            Name =  checkContentDict["Name"]    
            member = self.entryModel.objects.values().filter(**{"Name":Name})
            if member and member[0]["id"] != int(checkContentDict["id"]):#存在
                message["flag"] = 1
                message["errorMessage"] = "{}已存在，请用其它的名字!".format(Name)
        return message            

    def chaneNeedCheckAuthority(self, needCheckAuthority):
        self.needCheckAuthority = needCheckAuthority
    def chaneBasePath(self, basePath):
        self.basePath = basePath        
    #一些路径设置
    def setPath(self):
        self.systemLogin = ""
        self.entryIndex = "{entryName}index".format(entryName = self.entryName).lower()
        self.basePath = "{appName}/admin/{entryName}/".format(appName = utlitComm.app_name,entryName = self.entryName)
        
        self.indexHtmlPath = 'admin/{entryName}/index.html'.format(entryName = self.entryName)
        self.addHtmlPath = 'admin/{entryName}/add.html'.format(entryName = self.entryName.lower())
        self.editHtmlPath = 'admin/{entryName}/edit.html'.format(entryName = self.entryName.lower())
        self.vedioHtmlPath = 'admin/{entryName}/vedioTest.html'.format(entryName = self.entryName.lower())
        self.detailHtmlPath = 'admin/{entryName}/detail.html'.format(entryName = self.entryName.lower())
        
        self.deletePath = "admin//{entryName}/index/".format(entryName = self.entryName)
        
        self.pageInfoIndex = "/{basePath}index/".format(basePath = self.basePath)   
        
        self.startPage = "login"
    def setSpecPath(self,upName,entryName,indexIsSearch = True):
        self.systemLogin = ""
        self.entryIndex = "{upName}{entryName}search".format(upName = upName,entryName = entryName).lower()
        if upName == entryName + "Center":
            self.entryIndex = "{upName}index".format(upName = upName.lower())
        if upName == "FrontEnd":
            self.entryIndex = "frontendindexindex"
        self.basePath = "{appName}/{upName}/{entryName}/".format(appName = utlitComm.app_name,upName = upName,entryName = entryName)
        
        self.indexHtmlPath = '{upName}/{entryName}/index.html'.format(upName = upName,entryName = entryName)
        self.addHtmlPath = '{upName}/{entryName}/add.html'.format(upName = upName,entryName = entryName)
        self.editHtmlPath = '{upName}/{entryName}/edit.html'.format(upName = upName,entryName = entryName)
        self.vedioHtmlPath = '{upName}/{entryName}/vedioTest.html'.format(upName = upName,entryName = entryName)
        self.detailHtmlPath = '{upName}/{entryName}/detail.html'.format(upName = upName,entryName = entryName)
        
        self.deletePath = "{upName}/{entryName}/index/".format(upName = upName,entryName = entryName)
        
        self.pageInfoIndex = "/{basePath}index/".format(basePath = self.basePath)  
        if indexIsSearch:
            self.indexHtmlPath = '{upName}/{entryName}/search.html'.format(upName = upName,entryName = entryName)
            
        self.startPage = "frontendindexindex" 
        self.UserCenterIndex = "{upName}index".format(upName = upName.lower())
    def errInfoProcess(self,request,message):
        #显示错误信息
        errorInfo = ErrorInfo()
        return errorInfo.showErroInfo(request,message,self)
    #登录检查
    def checkLogin(self, request):
        pass
    #权限检查
    def  SystemRolePermissionsCheck(self, request):
         pass

   ####################################            
    def callMehtod(self,request,message = None):
        print("callMehtod")

                         
        returnValue = ""   
        
           
        if (request.path_info == "/{path}{method}/".format(path = self.basePath,method = "index" )) or (request.path_info == "/{path}{method}/".format(path = self.basePath,method = "search" )):
            return self.index(request)     

           
        if request.path_info == "/{path}{method}/".format(path = self.basePath,method = "index" ):
            return self.index(request)
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "add" ):
            return self.add(request)
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method =  "save_add" ):
            return self.save_add(request)
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "edit" ):
            return self.edit(request)   
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method =  "save_edit" ):
            return self.save_edit(request)
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "delete" ):
            return self.delete(request)   
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "delete_all" ):        
            return self.delete_all(request) 
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "detail" ):       
            return self.detail(request)   
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "import_excel" ):        
            return self.import_excel(request)           
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "export_excel" ):      
            return self.export_excel(request) 
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "download_excel" ):        
            return self.download_excel(request)    
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "getFSInfo" ):        
            return self.getFSInfo(request)       
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "getInfo" ):        
            return self.getInfo(request) 
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "ImageInformationAction" ):        
            return self.ImageInformationAction(request)    
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "ImageInformationAddComment" ):        
            return self.ImageInformationAddComment(request)   
         
        elif request.path_info == "/{path}{method}/".format(path = self.basePath,method = "keywordSearch" ):        
            return self.keywordSearch(request)                                                                                                                                         
        else:
            if self.viewType == "View":
                return redirect(reverse(self.startPage))  #return self.index(request)
            else:
                return Response({'status':0, "msg":"操作成功","data":context,"gotoUrl":reverse(self.startPage)})

####################################         以下无具体类无关开始   ################################################  
    def keywordSearch(self,request):
        self.frontEndPathUpdate(request)
        self.logProcess.addOperateLog(request,self.entryNameChinese,action = "搜索")   
        print(request.GET)
        #得到提交按钮
        keyword=request.GET.get('keyword') 
        normalSearch = request.GET.get('normalSearch')  
        viewAll = request.GET.get('viewAll')  
        if normalSearch is None:
            searchName = False
        else:
            searchName = True

        MemberId = request.session.get("frontusernameid")
        
        #得到分词
        seg_list = jieba.cut_for_search(keyword)  # 搜索引擎模式
        searchResult = None
        searchResultList = {}
        #开始搜索
        content = {}
        print("seg_list:")
        print(seg_list)
        if keyword:
            for item in seg_list:
                print(item)
                if searchName:
                    searchResult = self.entryObject.objects.values().filter(**{"Name__icontains":item})
                else:
                    searchResult = self.entryObject.objects.values().filter(**{"ImageTags__icontains":item})
                for record in searchResult:
                    searchResultList[record["id"]] = record

            CreatedTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            memberId = request.session.get("frontusernameid")
            #得到图片清单
            #增加搜索记录
            ImageInformationList = self.entryObject.objects.values().filter(**{"Name__in":seg_list})
            if MemberId:
                MemberId = apps.get_model(utlitComm.app_name,"Member").objects.get(id = MemberId)    
  
            sarchObjectList = self.entryObject.objects.values().filter(**{"Name":keyword}) 
            print(sarchObjectList)  
            searchLogDict = {"CreatedTime":CreatedTime,"Content":keyword} 
            if MemberId:
               searchLogDict["MemberId"]  = MemberId

            if len(sarchObjectList)>0:
                    for curObject in sarchObjectList:
                        ImageInformationId = apps.get_model(utlitComm.app_name,"ImageInformation").objects.get(id = curObject["id"])
                        searchLogDict["ImageInformationId"] = ImageInformationId
                        apps.get_model(utlitComm.app_name,"SearchHistory").objects.create(**searchLogDict)
            else:
                    apps.get_model(utlitComm.app_name,"SearchHistory").objects.create(**searchLogDict)
        elif viewAll:#查看全部
            searchResult = self.entryObject.objects.values().order_by("-id")
            for record in searchResult:
                    searchResultList[record["id"]] = record

        searchResultList = [item for item in searchResultList.values()]            
                   
        
        for item in searchResultList:
               
                images = item["ImageLink"].split(";")
                
                item["ImageLink"] = images[0]    
        
        content["searchResult"]  =  searchResultList          
        if self.viewType == "APPView":
            return Response({'status':0, "msg":"操作成功","data":content,"gotoUrl":self.detailHtmlPath}) 
        else:
            url = 'ForegroundDisplayInfo/{entryName}/searchResult.html'.format(entryName = self.entryName)
            return render(request,url,context=content)


#点赞、收藏、下载、播放动作记录
    def ImageInformationAction(self,request):
        self.frontEndPathUpdate(request)
        self.logProcess.addOperateLog(request,self.entryNameChinese,action = "预览")  
        print(request.GET) 
        print(request.POST) 
        eid=request.POST.get('curObject_id') 
        action=request.POST.get('action')

        MemberId = request.POST.get('MemberId') #作者
        CommentId = request.POST.get('CommentId') #评论编号
        FanId = None
        if MemberId:
            FanId = request.session.get("frontusernameid") #粉丝
        else:
            MemberId = request.session.get("frontusernameid") #作者

   
        modelObject = None
        #BrowsingHistory,Likes
        if action == "Likes": #Likes
            modelObject = apps.get_model(utlitComm.app_name,"Likes")
        elif  action == "BrowsingHistory":
            modelObject = apps.get_model(utlitComm.app_name,"BrowsingHistory") 
        elif  action == "FocusOn":
            modelObject = apps.get_model(utlitComm.app_name,"FocusOn") 
        elif  action == "CommentLikes":
            modelObject = apps.get_model(utlitComm.app_name,"CommentLikes") 

        CreatedTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())  
        ImageInformationId = apps.get_model(utlitComm.app_name,"ImageInformation").objects.get(id = eid) 

        #addInfo = {"CreatedTime":CreatedTime,'ImageInformationId':ImageInformationId} 
        addInfo = {"CreatedTime":CreatedTime}
        if MemberId and MemberId != '': 
            MemberId = apps.get_model(utlitComm.app_name,"Member").objects.get(id = MemberId) 
            addInfo['MemberId']  = MemberId

        if FanId and FanId != '' and action == "FocusOn": 
            #FanId = apps.get_model(utlitComm.app_name,"Member").objects.get(id = FanId) 
            addInfo['FanId']  = FanId  

        if  not FanId or FanId == '': 
            addInfo['ImageInformationId'] = ImageInformationId
        print(addInfo)

        #关注某人只能一次
        message = {"flag":0,"errorMessage":''}
       
        if action == "FocusOn":
            FanId = request.session.get('frontusernameid',None)
            MemberId = request.POST.get('MemberId')
            contentDict = {"FanId":FanId,"MemberId":MemberId}
            print(1111)
            print(contentDict)
            searchResult = modelObject.objects.values().filter(**contentDict)
            print(searchResult)
            if searchResult: #已关注
                 message["flag"] = 1
                 message["errorMessage"] = "你已关注过，不能重复关注"
            #自己不能关注自己
            if FanId == int(MemberId):
               message["flag"] = 1
               message["errorMessage"] = "自己不能关注自己！" 

        elif action == "Likes":
            print(222)
            ImageInformationId = request.POST.get('curObject_id')
            MemberId = request.session.get('frontusernameid')
            contentDict = {"ImageInformationId":ImageInformationId,"MemberId":MemberId}
            print(contentDict)
            searchResult = modelObject.objects.values().filter(**contentDict)
            print(searchResult)
            if searchResult: #已点赞
                 message["flag"] = 1
                 message["errorMessage"] = "你已点赞过，不能重复点赞"
        print(message)
        if message["flag"] == 0:         
            modelObject.objects.create(**addInfo)
       
        if  self.viewType == "View":
                    returnPage = {}
                    messageT = {"flag":message["flag"]}
                    returnData = { "message":message,"returnPage":returnPage}
                    return JsonResponse(returnData,
                        safe=False,
                        json_dumps_params={'ensure_ascii':False})  
        else:
                     
                    returnPaths = re.findall("/.+/(.+)WX/(.+)_save_(.+)/",request.path_info)[0]
                    
                    returnPath = ""
                    if returnPaths[0] == "FrontEnd":
                        returnPath = "/pages/{}Center/index/index".format(returnPaths[1])
                    else:
                        returnPath = "/pages/{}/{}/index/index".format(returnPaths[0],returnPaths[1])
           
                    return Response({'status':0, "msg":"操作成功","gotoUrl":returnPath})  
     #增加评论
    def ImageInformationAddComment(self,request):
        self.frontEndPathUpdate(request)
        self.logProcess.addOperateLog(request,self.entryNameChinese,action = "预览")  

        eid=request.POST.get('curObject_id') 
        action=request.POST.get('action')
        memberId = request.session.get("frontusernameid")
        Content =request.POST.get("Content")
        
        modelObject = None
        
        modelObject = apps.get_model(utlitComm.app_name,"Comment")
           
        CreatedTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())  
        ImageInformationId = apps.get_model(utlitComm.app_name,"ImageInformation").objects.get(id = eid)  
        MemberId = apps.get_model(utlitComm.app_name,"Member").objects.get(id = memberId) 

        addInfo = {"CreatedTime":CreatedTime,'ImageInformationId':ImageInformationId,'MemberId':MemberId,"Content":Content} 
        
        modelObject.objects.create(**addInfo)
       
        if  self.viewType == "View":
                    returnPage = {}
                    message = {"flag":0}
                    returnData = { "message":message,"returnPage":returnPage}
                    return JsonResponse(returnData,
                        safe=False,
                        json_dumps_params={'ensure_ascii':False})  
        else:
                     
                    returnPaths = re.findall("/.+/(.+)WX/(.+)_save_(.+)/",request.path_info)[0]
                    
                    returnPath = ""
                    if returnPaths[0] == "FrontEnd":
                        returnPath = "/pages/{}Center/index/index".format(returnPaths[1])
                    else:
                        returnPath = "/pages/{}/{}/index/index".format(returnPaths[0],returnPaths[1])
           
                    return Response({'status':0, "msg":"操作成功","gotoUrl":returnPath})  

    def getInfo(self,request):
        objectName = request.GET.get('objectName',"")
        objectId = request.GET.get('objectId',"") 
        objectInfo = self.getObject(request,objectName,True)
        print(objectInfo)
        #类型与商品的对应关系
       
        returnData = {"flag":0,  "message":"","data":objectInfo}
        if self.viewType == "View":
                    return JsonResponse(returnData,
                        safe=False,
                        json_dumps_params={'ensure_ascii':False})
        else:
            return Response({'status':0, "msg":"操作成功","data":objectInfo[objectName.lower()],"gotoUrl":reverse(self.startPage)})

           
    def getObject(self,request,modelName,needDict = False):
        searchSonCondition = {}
        ModelObject = apps.get_model(utlitComm.app_name,modelName)
        for field in ModelObject._meta.fields:
            fieldName = field.name
            fieldValue = ""
            if fieldValue != '':
                searchSonCondition[fieldName] = fieldValue
            
        if self.viewType == "View":
            objectInfo = ModelObject.objects.filter(**searchSonCondition)
        else:
            objectInfo = ModelObject.objects.values().filter(**searchSonCondition)
        content = {}    
        content[modelName  + "List"] = objectInfo     
        contentDict = {} 
        if needDict:#组装成字典，便于ajax返回使用
            from django.forms.models import model_to_dict
            for key,value in content.items(): 
                contentDict[key] = []
                for item in value:
                    
                    contentDict[key] = contentDict[key] + [model_to_dict(item)]  
            content = contentDict  
    
        return content
    def getInputParameter(self,request,paramList):
        searchSonCondition = {}
        for item in paramList:
            searchSonCondition[item[:len(item)-2]] = request.GET.get(item)
        return searchSonCondition

    def getObjectList(self,tableName,searchSonCondition,notAjax = False):
        #apps.get_model(utlitComm.app_name,fieldName[:len(fieldName)-2]) #去掉Id字样
        ModelObject = apps.get_model(utlitComm.app_name,tableName)#去掉Id字 
        
        if self.viewType == "View":
            objectInfo = ModelObject.objects.filter(**searchSonCondition)
        else:
            objectInfo = ModelObject.objects.values().filter(**searchSonCondition)
        if notAjax:
            return  objectInfo   

        returnData = {"flag":0,  "message":"","data":objectInfo}
        if self.viewType == "View":
                    return JsonResponse(returnData,
                        safe=False,
                        json_dumps_params={'ensure_ascii':False})
        else:
            return Response({'status':0, "msg":"操作成功","data":objectInfo[objectName.lower()],"gotoUrl":reverse(self.startPage)})
    
    #得到父子表的信息
    def getFSInfo(self,request):
        objectName = request.GET.get('objectName',"")
        objectId = request.GET.get('objectId',"") 
        objectInfo = self.getObjectFS(objectName,objectId,True)
        #类型与商品的对应关系

        returnData = {"flag":0,  "message":"","data":objectInfo}
        if self.viewType == "View":
                    return JsonResponse(returnData,
                        safe=False,
                        json_dumps_params={'ensure_ascii':False})
        else:
            return Response({'status':0, "msg":"操作成功","data":objectInfo[objectName.lower()],"gotoUrl":reverse(self.startPage)})

    #生成excel文件并下载 
    #@csrf_exempt
    def export_excel(self,request):  # 生成EXCEL表格
        import xlwt as ExcelWrite
        if request.method == 'GET':
            try:
                now = datetime.datetime.now()
                #得到数据

                context = self.getIndexContentAll(request)
                filename = '%s.xls' % (now.strftime("%Y-%m-%d-%H-%M-%S")+self.entryName)
                showFields = self.getSelectedFields(request) #request.GET.get("showFields").split(",")
                list_obj = context
                if list_obj:
                    # 创建工作薄
                    ws = ExcelWrite.Workbook(encoding='utf-8')
                    w = ws.add_sheet(self.entryNameChinese)
                    i = 0
                    for field in self.entryModel._meta.fields:        
                            if field.name in showFields:
                                w.write(0, i, field.verbose_name)
                                i += 1
     
                    # 写入数据
                    excel_row = 1
                    
                    for obj in list_obj:
                        i = 0
                        for field in self.entryModel._meta.fields:        
                            if field.name in showFields:
                                w.write(excel_row, i, obj[field.name])
                                i += 1
                        excel_row += 1
                    # 检测文件是够存在
                    # 方框中代码是保存本地文件使用，如不需要请删除该代码
                    ###########################
                    # exist_file = file_path+'test.xls'
                    # if exist_file:
                    #     os.remove(r"test.xls")
                    uploadPath =  utlitComm.upload_path_handler(self.entryName)
                    filePath = os.path.join(BASE_DIR,utlitComm.app_name,uploadPath,"excel")
                    Path(filePath).mkdir(parents=True, exist_ok=True)                    
                    savedFileName = os.path.join(filePath,filename)

                    ws.save(savedFileName)

                return JsonResponse({'code': 0, 'data': savedFileName})  # 将路径返回到前台
            except Exception as e:
                print(e)
                return JsonResponse({'code': 1, 'data': '导出表格失败!'})     
    #下载文件      
    def download_excel1(self,request):#

        from django.http import HttpResponse, Http404, StreamingHttpResponse
        try:
            filename = request.GET.get('data',None)
            def file_iterator(file_name):
                with open(file_name, 'rb')as f:
                    while True:
                        c = f.read(512)
                        if c:
                            yield c
                        else:
                            break
            response = StreamingHttpResponse(file_iterator(filename))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = "attachment;filename={0}".format(filename.split('/')[2])#这里改成自己需要的文件名
            
            return response
        except Exception as e:
            print (e)
            raise Http404
    def download_excel(self,request):
        from django.http import FileResponse, Http404, StreamingHttpResponse
        filename = request.GET.get('data',None)
        file = open(filename, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = "attachment;filename={0}".format(filename.split('/')[2])#这里改成自己需要的文件名
        return response           
    #上传文件到数据库
 #上传文件到数据库
    def import_excel(self, request):
        """导入excel表数据"""
        
        CreatedTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        excel_file = request.FILES.get('uploadExcelFile', '')  # 获取前端上传的文件
        file_type = excel_file.name.split('.')[1]  # 拿到文件后缀
        returnPage = self.genUrlPath(request,self.entryIndex)

        if file_type in ['xlsx', 'xls']:   # 支持这两种文件格式
            # 打开工作文件
            data = xlrd.open_workbook(filename=None, file_contents=excel_file.read())
            tables = data.sheets()  # 得到excel中数据表sheets1，sheets2...,一般只有只有一个，因为这是针对一个表的操作
            
            # 循环获取每个数据表中的数据并写入数据库
            for table in tables:
                rows = table.nrows   # 总行数
                
                try:
                    # 控制数据库事务交易
                    #with transaction.atomic():
                        # 获取数据表中的每一行数据写入设计好的数据库表
                        
                        for row in range(1, rows):  # 从1开始是为了去掉表头

                            row_values = table.row_values(row)  # 每一行的数据
                            
                            fieldLength =  len(self.entryModel._meta.fields) #所有字段名
                            rowData = {}
                            
                            i = 0

                            for field in self.entryModel._meta.fields:
                                
                                fieldName = field.name
                                
                                if fieldName in ["id","UpdateTime","CreatedTime"] :
                                    
                                    continue   
                                fieldValue = ""
                                try:
                                    fieldValue = str(row_values[i])
                                except:
                                    pass

                                if fieldValue != '' and type(field).__name__ == "CharField"  and fieldValue.find(".0") >=0:
                                       
                                        fieldValue = fieldValue[:len(fieldValue)-2]
                                #外键处理
                                if fieldName[len(fieldName)-2:] == "Id" and fieldValue != '':
                                   fieldValue = fieldValue[:len(fieldValue)-2]
                                   fieldValue = apps.get_model(utlitComm.app_name,fieldName[:len(fieldName)-2]).objects.get(id = int(fieldValue)) 
                                
                                if fieldValue != '':
                                    rowData[fieldName] = fieldValue 
                                i += 1 
                                print(rowData)
                            rowData["CreatedTime"] = CreatedTime    
                            print(rowData)   
                            self.entryModel.objects.create(**rowData)  #每一行的数据对应表的每列。由于id是自动生成的，所以id列不存入在excel中。

                except:
                    print(sys.exc_info())
                    returnData = {"flag":1,  "message":"解析excel文件或者数据插入错误","returnPage":returnPage}
                    if self.viewType == "View":
                        return JsonResponse(returnData,
                        safe=False,
                        json_dumps_params={'ensure_ascii':False})

            returnData = {"flag":0, "message":"成功","returnPage":returnPage}            
            if self.viewType == "View":
                    return JsonResponse(returnData,
                        safe=False,
                        json_dumps_params={'ensure_ascii':False})
        else:
                returnData = {"flag":1,  "message":"上传文件类型错误！","returnPage":returnPage}
                if self.viewType == "View":
                    return JsonResponse(returnData,
                        safe=False,
                        json_dumps_params={'ensure_ascii':False})
    ##############################              
    def index_query(self,request,query):
        return None
    #@IndexSystemOperationLog
    def index(self,request):
        self.frontEndPathUpdate(request)
        self.logProcess.addOperateLog(request,self.entryNameChinese,action = "查询")
        if self.viewType == "View":
            context = self.getIndexContent(request)
            return render(request,self.indexHtmlPath,context=context)
        else:
            #处理返回数据

            #returnData = self.processSearchDataForeignField(context)
            listInfo = self.listInfo(request)
            return listInfo
            #return Response({'status':0, "msg":"操作成功","data":returnData,"gotoUrl":self.indexHtmlPath,"totalPageCount":context["totalPageCount"]})
    #处理查询列表外键值
    def processSearchDataForeignField(self,content):
         returnData = []
         try: 
             #外键值处理
             
             for item in content["page"].object_list:
                for field in self.entryModel._meta.fields: #所有字段名
            
                    fielTypeName = type(field).__name__
                    fieldName = field.name
                         
                    if fielTypeName.lower() == "ForeignKey".lower(): #外键字段，检查有效性

                        item[fieldName] = str(item[fieldName])
               
             returnData = content["page"].object_list 

             #更新下拉框字段

         except:
                pass

         return returnData
    #查询
    def listInfo(self,request):

         inputParametersDict,pn = self.getSearchParametersDict(request)

         content= self.getSearchJosnDataForlistInfo(inputParametersDict,pn) 

         returnData = []
         try: 
             #外键值处理
             returnData = self.processSearchDataForeignField(content)
         except:
                pass
         
         return Response({'status':0, "msg":"查询成功","data":returnData,"gotoUrl":self.indexHtmlPath,"totalPageCount":content["totalPageCount"]})       
        
 #获取某页数据
    def getSearchJosnDataForlistInfo(self,inputParametersDict,pn):
        
        query=inputParametersDict

        if not inputParametersDict or len(inputParametersDict.keys()) == 0:

            entryObject = self.entryObject.objects.values().all()
            query = ''

        else:
            entryObject = self.entryObject.objects.values().filter(**inputParametersDict)  
        
        #将取得的记录传给Paginator，每页显示5条
        paginator=Paginator(entryObject,utlitComm.pageSize)
        
        try : #处理pn不存在的情况
            page=paginator.page(pn)

            updatedPageInfo = utlitComm.updatedPageInfo(self.entryObject,page.object_list)

            page.object_list = updatedPageInfo       
                
            #将page和查询字段传给前端
            context={ 
                "page":page,
                'query':inputParametersDict,
                'pageInfo':utlitComm.getPageBar(self.pageInfoIndex,page,query,pn),
                "deletePath":self.deletePath,
                "totalPageCount": paginator.num_pages
            }
        except:
               page = {}
               context={ 
                "page":page,
                'query':inputParametersDict,
                'pageInfo':'',
                "deletePath":self.deletePath,
                "totalPageCount": paginator.num_pages
              }    
        return context
    #得到查询条件    
    def getSearchParametersDict(self,request):
        inputParametersDict = {}
        for field in self.entryObject._meta.fields: #所有字段名
            fieldName = field.name
            fieldValue = request.GET.get(fieldName)
            if fieldValue and fieldValue != '':
                inputParametersDict[fieldName] = request.GET.get(fieldName)
        #处理模糊查询
        searchData = request.GET.get("searchData")
        if searchData and searchData != '':
            feildValue= searchData.split(",")
            if len(feildValue)==2 and feildValue[1] != '':
                fieldName = feildValue[0]
                fieldValue = feildValue[1]
                inputParametersDict[fieldName + "__icontains"]  = fieldValue      
        pn = request.GET.get('p')
        if not pn:
            pn = 1
              
        return inputParametersDict,pn  

     #得到查询字段
    def getSearchParametersDictIndex(self,request):
        inputParametersDict = {}
        queryCondition= {}

        for field in self.entryObject._meta.fields: #所有字段名
            fieldName = field.name
            fieldValue = request.GET.get(fieldName)
            if fieldValue and fieldValue != '':
                if fieldName in utlitComm.publicDataDict.keys():
                    inputParametersDict[fieldName] = fieldValue
                else: #模糊查询
                    if type(field).__name__ in ['CharField']:
                        inputParametersDict[fieldName + "__icontains" ] = fieldValue
                    else:
                        inputParametersDict[fieldName] = fieldValue

                queryCondition[fieldName] = fieldValue
            #处理时间段
            if fieldValue == None:
               fieldValue = request.GET.get(fieldName + "Start")
               if fieldValue and fieldValue != '':  
                    inputParametersDict[fieldName + "__gte"] = fieldValue  
                    queryCondition[fieldName + "Start"] = fieldValue
               
               fieldValue = request.GET.get(fieldName + "End")
               if fieldValue and fieldValue != '':  
                        inputParametersDict[fieldName + "__lte" ] = fieldValue 
                        queryCondition[fieldName + "End"] = fieldValue 
        #如果是前台用户，加个用户id
        print("self.entryIndex:",self.entryIndex)
        if len(re.findall("center",self.entryIndex)) >0:
            if "MemberId" not in inputParametersDict.keys():
                if len(re.findall("center",self.entryIndex)) >0 and len(re.findall("focusonsearch",self.entryIndex)) >0:
                                inputParametersDict["FanId"] = request.session.get('frontusernameid',None)
                else:
                                inputParametersDict["MemberId"] = request.session.get('frontusernameid',None)

        print("inputParametersDict",inputParametersDict)   

        inputParameters = {"inputParametersDict":inputParametersDict,"queryCondition":queryCondition}   
        return inputParameters
    #得到查询的所有数据
    def getIndexContentAll(self,request):
        #获取前端收到的查询的值，默认值为空

        inputParameters = self.getSearchParametersDictIndex(request)
        inputParametersDict = inputParameters["inputParametersDict"]
        queryCondition = inputParameters["queryCondition"]
        if len(inputParameters.keys()) >0:
            entryObjectSearchData = self.entryObject.objects.values().filter(**inputParametersDict)
        #否则取得所有的记录，并设置query的初始值为''
        else:
            entryObjectSearchData = self.entryObject.objects.values()

        updatedPageInfo = utlitComm.updatedPageInfo(self.entryObject,entryObjectSearchData,self.entryName)    

        return updatedPageInfo

    #得到选中的字段
    def getSelectedFields(self,request):

        fieldSelectedList = request.GET.getlist("fieldSelected")
        return fieldSelectedList

    #得到首页列表内容

    def getIndexContent(self,request):

        #获取前端收到的查询的值，默认值为空
        pn = request.GET.get('p')
        inputParameters = self.getSearchParametersDictIndex(request)
        inputParametersDict = inputParameters["inputParametersDict"]
        queryCondition = inputParameters["queryCondition"]
        if len(inputParameters.keys()) >0:
            entryObjectSearchData = self.entryObject.objects.values().filter(**inputParametersDict)
        #否则取得所有的记录，并设置query的初始值为''
        else:
            entryObjectSearchData = self.entryObject.objects.values()
        #将取得的记录传给Paginator，每页显示5条
        paginator=Paginator(entryObjectSearchData,utlitComm.pageSize)

        if pn:
            page=paginator.page(pn)
        else:
            page=paginator.page(1)
            
        updatedPageInfo = utlitComm.updatedPageInfo(self.entryObject,page.object_list,self.entryName)
        #粉丝账号
        if self.entryName == "FocusOn":
             ModelObject = apps.get_model(utlitComm.app_name,"Member")
             for item in updatedPageInfo:
                item["FanId"] = str(ModelObject.objects.get(id = item["FanId"]))
        
        page.object_list = updatedPageInfo 
        from urllib.parse import urlencode 
        query =  urlencode(inputParametersDict)
        #将page和查询字段传给前端
        context={ 
            "page":page,
            'pageInfo':utlitComm.getPageBar(self.pageInfoIndex,page,query,pn),
            "deletePath":self.deletePath,
            "totalPageCount": paginator.num_pages,
            "{}".format(self.entryName):queryCondition,
            "fieldNameList":json.dumps(self.getFieldNameList()),
            "fieldNameListSelected":self.getFieldNameList()
        }
        return context
    #得到字段列表
    def getFieldNameList(self):
        fieldNameList = []
        for field in self.entryModel._meta.fields: 
            if field.name not in ["id","UpdateTime","CreatedTime"]:
                fieldNameList.append({"fieldName":field.name,"fieldNameChinese":field.verbose_name})       
     
        return fieldNameList

    def add_forignObjectDict(self, request,dataUsePosition = ""):
        forignObjectDict = {}
        
        for fieldTableName in self.foreignkeyTableList.values(): #所有字段名

                foreignKeyModel = apps.get_model(utlitComm.app_name,fieldTableName)#去掉Id字样
                forign_obj = self.getForignObjectList(fieldTableName,dataUsePosition)#foreignKeyModel.objects.all()
                forignObjectDict[fieldTableName] =  forign_obj               
        return forignObjectDict 

    def add_forignObjectDictFS(self, request,dataUsePosition = ""):
        forignObjectDict = {}
        forignObjectDict = self.add_forignObjectDictNormal(request,self.entryModel)
        
        for fieldTableName in self.foreignkeyTableList.values(): #所有字段名

                foreignKeyModel = apps.get_model(utlitComm.app_name,fieldTableName)#去掉Id字             
                sonForignObj = self.add_forignObjectDictNormal(request,foreignKeyModel)
                forignObjectDict = {**forignObjectDict,**sonForignObj}

        return forignObjectDict 

    def add_forignObjectDictNormal(self, request,modelObj,dataUsePosition = ""):
        forignObjectDict = {}
        
        for fieldTableName in modelObj.foreignkeyTableList.values(): #所有字段名

                foreignKeyModel = apps.get_model(utlitComm.app_name,fieldTableName)#去掉Id字样
                forign_obj = self.getForignObjectList(fieldTableName,dataUsePosition)#foreignKeyModel.objects.all()
                forignObjectDict[fieldTableName] =  forign_obj               
        return forignObjectDict  
    #外键是自身的外键列表-按照上级外键分类列出，并且留出一个顶级选项
    def getForignObjectList(self,fieldTableName,dataUsePosition):
        foreignKeyModel = apps.get_model(utlitComm.app_name,fieldTableName)#去掉Id字样

        hasSun = False
        try:
            forign_obj = foreignKeyModel.objects.values().order_by('{}'.format(fieldTableName + "Id"))
            hasSun = True
        except: 
            
            forign_obj = foreignKeyModel.objects.all().order_by("id")  

        if dataUsePosition == "detail":
              hasSun = False
              forign_obj = foreignKeyModel.objects.all().order_by("id") 

        if hasSun:   

            rlist = {}
            listObject = forign_obj
            fieldTableNameId = fieldTableName + "Id"
            #顶级分类清单

            topTypeList = []
            for i in range(len(listObject)):
                if not listObject[i]["{}_id".format(fieldTableNameId)]:
                    topTypeList.append({"id":listObject[i]["id"]})
                if  listObject[i]["{}_id".format(fieldTableNameId)]:  
                    break

            for i in range(len(topTypeList)):

                id = topTypeList[i]["id"]

                parentId = 0
                curItem = forign_obj[i]
            
                level = 0
            
                self.recursiveList(listObject,id,parentId,curItem,rlist,fieldTableNameId)

            forign_objList = []
            forign_objList.append({"level":0,"id":"","{}".format(fieldTableNameId):"","Name":"顶级分类"})
            for value in rlist.values():
                forign_objList.append(value)

            forign_obj = forign_objList
            
        return forign_obj

    #给定一个id,parentId,name列表。如果某记录的parentId = 其它id则表示改记录为其它id记录的子类，该记录位于其父记录之下。
    #list结构：id,parentId,name
    def  recursiveList(self,listObject,id,parentId,curItem,rlist,fieldTableNameId):
            hasSun = False
            if len(rlist.items()) == 0:
                levelTemp = 0
            else:
                try:
                    levelTemp = rlist[parentId]["level"] + 1
                except:
                    levelTemp = 0
            spaces = self.getSpaces(levelTemp)
            rlist[id] = {"level":levelTemp,"id":id,"{}".format(fieldTableNameId):parentId,"Name":spaces + curItem["Name"]}
            
            for i in range(len(listObject)):
                if listObject[i]["{}_id".format(fieldTableNameId)] == id:
                    hasSun = True

                    self.recursiveList(listObject,listObject[i]["id"],id,listObject[i],rlist,fieldTableNameId)

            if  hasSun == False:

                   return     
    #得到空格个数
    def getSpaces(self,count):
        spaces = ""
        for i in range(count):
            spaces += "\u00a0\u00a0"

        return spaces
    #得到父子表的空白行
    def getAddContentFS(self,request) :
        content = self.add_forignObjectDict(request)
        FSBlank = self.getAllTableBlankRowListFS()
        content = {**content,**FSBlank}  
        return content
    def add(self,request,storage_dict = None,message = None):  
        self.frontEndPathUpdate(request)
        self.logProcess.addOperateLog(request,self.entryNameChinese,action = "新增") 
        if len(self.entryModel.sonTableList.keys())>0:
            content = self.getAddContentFS(request)
            
        else:        
            content = self.add_forignObjectDict(request)
            
            content["message"] = message
            content[self.entryName.lower()] = storage_dict
        if self.viewType == "View":
            return render(request,self.addHtmlPath,context=content)
        else:

            returnPaths = re.findall("/.+/(.+)WX/(.+)_(.+)/",request.path_info)[0]

            returnPath = ""
            if returnPaths[0] == "FrontEnd":
                returnPath = "/pages/{}Center/index/index".format(returnPaths[1])
            else:
                returnPath = "/pages/{}/{}/{}/{}".format(returnPaths[0],returnPaths[1],returnPaths[2],returnPaths[2])
   
            return Response({'status':0, "msg":"操作成功","data":content,"gotoUrl":returnPath})  

    def postDataCollection(self,request):
        postDataDict = {}
        
        for field in self.entryModel._meta.fields: #所有字段名
            
            fielTypeName = type(field).__name__
            fieldName = field.name
            if  fieldName == "id": #主键不处理
                continue
            if fielTypeName.lower() == "FileField".lower(): #文件字段
                
                #文件字段
                #fileObect = request.FILES.get(fieldName,None)
                fileObect = request.FILES.getlist(fieldName)
                #文件上传
                fieldValue = utlitComm.save_file(self.entryName,fileObect)                 
            elif fielTypeName.lower() == "ForeignKey".lower(): #外键字段，检查有效性
                if self.viewType == "View":
                    fieldValue = request.POST.get(fieldName)
                else:
                    fieldValue = request.data.get(fieldName)
                try:
                    foreignKeyModel = apps.get_model(utlitComm.app_name,self.foreignkeyTableList[fieldName]) #去掉Id字样
                    fieldValue = foreignKeyModel.objects.get(id=fieldValue)
                except:
                    fieldValue = ""
            else:
                if self.viewType == "View":
                    fieldValue = request.POST.get(fieldName)
                else:
                    fieldValue = request.data.get(fieldName)

            if   fieldValue and fieldValue != "": 
                  
                postDataDict[fieldName] = fieldValue 

                
        return postDataDict
    def genUrlPath(self,request,innerPage):
        return "{http}://{host}{path}".format(http = parse.urlsplit(request.build_absolute_uri(None)).scheme,host = request.META['HTTP_HOST'],path = reverse(innerPage))
    #子表和父表数据处理开始
    #得到输入值，文件与一般文本值分开
    def getPostDataCollectionFS(self,postData,modelDict,dataType = "normal",isEdit = False):
        postDataDict = {}
        if dataType == "file":
            files = postData
            postData = postData.items()
        for inputField,inputFieldValue in  postData:
            #得到输入的表，记录，字段
            inputFieldInfoFather =  re.findall("(.*)\.(.*)",inputField)  #主表
            inputFieldInfoSon =  re.findall("(\d+)_(.*)\.(.*)",inputField)  #一级子表
            inputFieldInfoSonSon =  re.findall("(\d+)_(\d+)_(.*)\.(.*)",inputField)  #二级子表  
            fatherRecordNo,sonRecordNo = -1 , -1
            tableName,fieldName = "",""
            if len(inputFieldInfoFather) >0 and len(inputFieldInfoSon) == 0 and len(inputFieldInfoSonSon) == 0:
                    tableName = inputFieldInfoFather[0][0]
                    fieldName = inputFieldInfoFather[0][1]
            elif len(inputFieldInfoFather) >0 and len(inputFieldInfoSon) > 0 and len(inputFieldInfoSonSon) == 0:
                    fatherRecordNo = inputFieldInfoSon[0][0]
                    tableName = inputFieldInfoSon[0][1]
                    fieldName = inputFieldInfoSon[0][2]

            elif len(inputFieldInfoFather) >0 and len(inputFieldInfoSon) > 0 and len(inputFieldInfoSonSon) > 0:
                    fatherRecordNo = inputFieldInfoSonSon[0][0]
                    sonRecordNo = inputFieldInfoSonSon[0][1]
                    tableName = inputFieldInfoSonSon[0][2]
                    fieldName = inputFieldInfoSonSon[0][3]

            #得到输入值
            #得到类型
            
            fieldValue = inputFieldValue
            try:
                fielTypeName = modelDict[tableName]["fieldType"][fieldName] #字段为空？
            except:

                continue

            if  fieldName == "id" and isEdit == False: #新增主键不处理
                continue
            if isEdit == True and fatherRecordNo == '0': #修改fatherRecordNo = 0不处理，
                    continue
                    
            #特殊类型处理 

            if dataType == "file": #文件字段
                
                #文件字段
                #fileObect = request.FILES.get(fieldName,None)
                fileObect = files.get(inputField,None)
                
                #文件上传

                fieldValue = utlitComm.save_file(tableName,fileObect) 
            if dataType == "normal" and fielTypeName.lower() == "ForeignKey".lower(): #外键字段，检查有效性
                try:
                    foreignKeyModel = apps.get_model(utlitComm.app_name,fieldName[:len(fieldName)-2]) #去掉Id字样
                    fieldValue = foreignKeyModel.objects.get(id=fieldValue)
                except:
                    fieldValue = ""

            if  not isEdit and not (fieldValue and fieldValue != ""): #如果新增，值为空，不是有效内容
                continue

            if  isEdit and not (fieldValue and fieldValue != ""): #如果修改中的新增，值为为空，是有效内容
                try:
                    if postDataDict[tableName][fatherRecordNo][sonRecordNo]["id"] == "0": ##id = 0 表示为新增
                        continue 
                except:
                    continue               
            #判定字段是否某表，如有效则保存
            #print("{}-{}-{}-{}".format(tableName,fatherRecordNo,sonRecordNo,fieldName))
            #值为None，忽略
            if fieldValue == "None" or fieldValue == 'undefined' :
                continue    

            if  tableName in  modelDict.keys(): #表有效  
                if fieldName in modelDict[tableName]["fields"]:#字段有效
                    if tableName not in postDataDict.keys():
                        postDataDict[tableName] =  {fatherRecordNo:{sonRecordNo:{fieldName:fieldValue}}}
                    elif fatherRecordNo not in postDataDict[tableName].keys():
                         postDataDict[tableName][fatherRecordNo] =  {sonRecordNo:{fieldName:fieldValue}}
                    elif sonRecordNo not in postDataDict[tableName][fatherRecordNo].keys():
                         postDataDict[tableName][fatherRecordNo][sonRecordNo] =  {fieldName:fieldValue}
                    else:
                        postDataDict[tableName][fatherRecordNo][sonRecordNo][fieldName] = fieldValue
               
        return postDataDict  
    #收集到子表和父表的输入值
    def postDataCollectionFS(self,request,isEdit = False):
        
        postDataDict = {}
        #得到所有子表
        allTableList = self.getAllTablesFS()

        modelDict = {}
        for table in allTableList.keys():
            model = apps.get_model(utlitComm.app_name,table)
            modelDict[table] = {"model":model,"fields":[field.name for field in model._meta.fields],
                "fieldType":{field.name:type(field).__name__ for field in model._meta.fields}}
        
        #得到输入字典
        postData = {}
        if self.viewType == "View":
                    postData = request.POST.items()
        else:
                    postData = request.data.items()

        postDataDict = self.getPostDataCollectionFS(postData,modelDict,dataType = "normal",isEdit = isEdit) 
        
        postDataDictFile =  self.getPostDataCollectionFS(request.FILES,modelDict,dataType = "file",isEdit = isEdit) 
        
        for key,value in postDataDictFile.items():#表
           
            for subKey,subValue in value.items():#组 -1
                
                for  subSubKey,subSubValue in subValue.items():#记录 -1
                   
                    for fileKey,fileValue in subSubValue.items():#字段列表
                        
                        try:
                            postDataDict[key][subKey][subSubKey][fileKey] = fileValue
                        except:
                            try:
                                postDataDict[key][subKey][subSubKey] = {fileKey:fileValue}
                            except:
                                try:
                                    postDataDict[key][subKey] = {subSubKey:{fileKey:fileValue}}
                                except:
                                    
                                    postDataDict[key] = {subKey:{subSubKey:{fileKey:fileValue}}}

                        
                                      
        return postDataDict  
    #得到父子表所有涉及的表
    def getAllTablesFS(self):
        sonTableList = {}
        allTableList = {}
        for sontable in self.entryModel.sonTableList.keys():
                try:
                    sonModel = apps.get_model(utlitComm.app_name,sontable)
                    sonTableList = {**sonTableList,**sonModel.sonTableList}
                except:
                    continue
        allTableList = {**sonTableList,**{self.entryName:self.entryNameChinese}}            
        allTableList = {**allTableList,**self.entryModel.sonTableList}
        return allTableList
    #检查输入
    def checkInputDataFS(self,inputDataFS):
        #得到所有涉及的表
        sonTableList = self.getAllTablesFS()
       
        for tabeleName in sonTableList.keys():
            checkModel = apps.get_model(utlitComm.app_name,tabeleName)
            if  tabeleName in inputDataFS.keys():#该表有数据输入
                checkContentDict = inputDataFS[tabeleName]
                checkMessage = self.checkContentValid(checkContentDict,checkModel)
                if checkMessage["flag"] == 1:#数据有误
                    break              
        return checkMessage
    #更新数据
    @transaction.atomic
    def manyTablesUpdateDataFS(self,inputDataFS):
        #得到主表
        storage_dict = inputDataFS[self.entryName][-1][-1]
        masterObject = self.entryObject.objects.filter(id=storage_dict["id"]).update(**storage_dict)

        masterObjectId = storage_dict["id"]

        #删除子表和子子表记录
        #得到原有记录的id 列表
        oldInfo = self.editProcessFS(None,masterObjectId,False)
        deleteInfo = {} 

        for sonTable in self.entryModel.sonTableList.keys():
            if  sonTable == self.entryName:
                continue
            oldRecord = oldInfo[sonTable.lower() + "List"]
            
            try:
                    nowRecord =  inputDataFS[sonTable].values()
            except:
                    nowRecord = {}
            idList = []
            if sonTable  in inputDataFS.keys():
                    
                for key,value in inputDataFS[sonTable].items():
                    for k,v in value.items():
                        idList.append(v["id"])

            for item in oldRecord:
                if str(item.id) not in idList:
                        try:
                            deleteInfo[sonTable] = {**deleteInfo[sonTable],**{item.id:item.id}}
                        except:
                            deleteInfo = {**deleteInfo,**{sonTable:{item.id:item.id}}}
                
            sonSonTableList = apps.get_model(utlitComm.app_name,sonTable).sonTableList                    
            if len(sonSonTableList.keys()) > 0:#子子表
                
                for sonSonTable in sonSonTableList.keys(): 

                    oldRecordSon = oldInfo[sonSonTable.lower() + "List"]
                    try:    
                            nowRecordSon =  inputDataFS[sonSonTable].values()
                    except:
                            nowRecordSon = {}  
                               
                    idListSon = []
                    if sonSonTable in inputDataFS.keys():
                        for key,value in inputDataFS[sonSonTable].items():
                            for k,v in value.items():
                                if "id" in v.keys():
                                    idListSon.append(v["id"])
                        
                    for item in oldRecordSon:
                        if str(item.id) not in idListSon:
                                try:
                                    deleteInfo[sonSonTable] = {**deleteInfo[sonSonTable],**{item.id:item.id}}
                                except:
                                    deleteInfo = {**deleteInfo,**{sonSonTable:{item.id:item.id}}}
                   
        #删除记录

        for sonTable in self.entryModel.sonTableList.keys():
            if sonTable == self.entryName:
                continue
            sonModel = utlitComm.publicSonTableObjectList[self.entryName][sonTable]
            sonSonTableList = sonModel.sonTableList #子表的子表
            if len(sonSonTableList.keys()) > 0:#子子表
                  
                for sonSonTable in sonSonTableList.keys(): 

                            sonSonModel = utlitComm.publicSonTableObjectList[sonTable][sonSonTable]
                            if sonSonTable in deleteInfo.keys():
                                idListSon =  list(deleteInfo[sonSonTable].keys())

                                if len(idListSon) >0:
                                        sonSonModel.objects.filter(**{"id__in":idListSon}).delete() 
                                       
            if sonTable in deleteInfo.keys():
                    idList =  list(deleteInfo[sonTable].keys())
                        
                    if len(idList) >0:#子表
                            
                            sonModel.objects.filter(**{"id__in":idList}).delete()     
                            
        #子表及子子表处理 - 修改和新增
        fatherTableName = self.entryName

        for sonTable in self.entryModel.sonTableList.keys():
            sonModel = apps.get_model(utlitComm.app_name,sonTable) #子表Model
            sonSonTableList = sonModel.sonTableList #子表的子表
            if sonTable not in inputDataFS.keys():#子表无记录
                continue
            sonTableRecordList = inputDataFS[sonTable] #子表记录
            if sonTable == fatherTableName:#本身，不执行子表更新操作
                continue
            if len(sonSonTableList.keys()) == 0:#无子子表

                self.updateFSRecordsEdit(sonModel = utlitComm.publicSonTableObjectList[fatherTableName][sonTable],sonDatasDict = {key:value[-1] for key,value in sonTableRecordList.items()},
                    relativeFieldFS = fatherTableName + "Id",masterObjectId = masterObjectId,fatherModel = self.entryObject)
            else:#有子子表
                for sonKey,sonValue in sonTableRecordList.items():  
                        
                        sonValue[-1][fatherTableName + "Id"] = self.entryObject.objects.get(id = masterObjectId) #更新与父表关联的字段
                        
                        for sonSonTable in sonSonTableList.keys(): 
                            if sonSonTable not in inputDataFS.keys():#只有父表有记录

                                self.updateFSRecordsEdit(sonModel = None,sonDatasDict = None,
                                    relativeFieldFS = sonTable + "Id",masterObjectId = sonValue[-1]["id"],fatherModel = utlitComm.publicSonTableObjectList[fatherTableName][sonTable],fatherDataDict = sonValue[-1])
                            
                            else:
                                #一部分父表有子记录
                                if sonKey in inputDataFS[sonSonTable].keys():#父表有子记录
                                    sonSonTableRecordList = inputDataFS[sonSonTable][sonKey] #所属子表记录
                                    sonSonModel = apps.get_model(utlitComm.app_name,sonSonTable)

                                    self.updateFSRecordsEdit(sonModel = utlitComm.publicSonTableObjectList[sonTable][sonSonTable],sonDatasDict = sonSonTableRecordList,
                                        relativeFieldFS = sonTable + "Id",masterObjectId = sonValue[-1]["id"],fatherModel = utlitComm.publicSonTableObjectList[fatherTableName][sonTable],fatherDataDict = sonValue[-1])
                                else:
                                    self.updateFSRecordsEdit(sonModel = None,sonDatasDict = None,
                                    relativeFieldFS = sonTable + "Id",masterObjectId = sonValue[-1]["id"],fatherModel = utlitComm.publicSonTableObjectList[fatherTableName][sonTable],fatherDataDict = sonValue[-1])
                            
    #更父表和子表，父表一条记录，子表多条记录（包括一条）.如果传入父表ID，则只更新子表
    def updateFSRecordsEdit(self,sonModel,sonDatasDict,relativeFieldFS,masterObjectId = "",fatherModel = None,fatherDataDict = None):
        #父表
        if masterObjectId == "0":
            if fatherDataDict:
                fatherDataDict.pop("id")
                masterObject = fatherModel.objects.create(**fatherDataDict)
                masterObjectId = masterObject.id 
        else:
            if fatherDataDict:
                masterObject = fatherModel.objects.filter(id=masterObjectId).update(**fatherDataDict)
        #子表
        if sonDatasDict:
            for key,value in sonDatasDict.items():
                sonDatasDict[key][relativeFieldFS] = fatherModel.objects.get(id = masterObjectId)
                if sonDatasDict[key]["id"] == "0": #新加的记录，移除id字段内容
                   sonDatasDict[key].pop("id") 
                   sonModel.objects.create(**sonDatasDict[key])
                else:#更新记录
                   sonModel.objects.filter(id=sonDatasDict[key]["id"]).update(**sonDatasDict[key])

    #保存数据
    @transaction.atomic
    def manyTablesSaveDataFS(self,inputDataFS):
        #得到主表
        storage_dict = inputDataFS[self.entryName][-1][-1]
        
        masterObject = self.entryObject.objects.create(**storage_dict)
        
        masterObjectId = masterObject.id

        #子表及子子表处理
        fatherTableName = self.entryName

        for sonTable in self.entryModel.sonTableList.keys():

            sonModel = apps.get_model(utlitComm.app_name,sonTable) #子表Model
            sonSonTableList = sonModel.sonTableList #子表的子表
            
            if sonTable not in inputDataFS.keys():#子表无记录
                continue
            sonTableRecordList = inputDataFS[sonTable] #子表记录
            if sonTable == fatherTableName:#本身，不执行子表更新操作
                continue
            if len(sonSonTableList.keys()) == 0:#无子子表

                if sonTable in inputDataFS.keys():#父表有记录
                    
                    #得到子表记录清单

                    self.updateFSRecords(sonModel = utlitComm.publicSonTableObjectList[fatherTableName][sonTable],sonDatasDict = {key:value[-1] for key,value in sonTableRecordList.items()},
                        relativeFieldFS = fatherTableName + "Id",masterObjectId = masterObjectId,fatherModel = self.entryObject)
            else:#有子子表
                for sonKey,sonValue in sonTableRecordList.items(): 
                        if -1 not in sonValue.keys():
                            sonValue = {**sonValue,**{-1:{fatherTableName + "Id":self.entryObject.objects.get(id = masterObjectId)}}} #更新与父表关联的字段
                        else:    
                            sonValue[-1][fatherTableName + "Id"] = self.entryObject.objects.get(id = masterObjectId) #更新与父表关联的字段
                        
                        for sonSonTable in sonSonTableList.keys(): 
                            if sonSonTable in inputDataFS.keys():#子表有记录
                                if sonKey in inputDataFS[sonSonTable].keys():#对应父表记录有子记录
                                    sonSonTableRecordList = inputDataFS[sonSonTable][sonKey] #所属子表记录
                                    sonSonModel = apps.get_model(utlitComm.app_name,sonSonTable)

                                    self.updateFSRecords(sonModel = utlitComm.publicSonTableObjectList[sonTable][sonSonTable],sonDatasDict = sonSonTableRecordList,
                                        relativeFieldFS = sonTable + "Id",masterObjectId = "",fatherModel = utlitComm.publicSonTableObjectList[fatherTableName][sonTable],fatherDataDict = sonValue[-1])
                        
                            else:#子表无记录
                                self.updateFSRecords(sonModel = None,sonDatasDict = None,
                                    relativeFieldFS = fatherTableName + "Id",masterObjectId = masterObjectId,fatherModel = self.entryObject)
    #更父表和子表，父表一条记录，子表多条记录（包括一条）.如果传入父表ID，则只更新子表
    def updateFSRecords(self,sonModel,sonDatasDict,relativeFieldFS,masterObjectId = "",fatherModel = None,fatherDataDict = None):

        if masterObjectId == "":
            
            masterObject = fatherModel.objects.create(**fatherDataDict)
            masterObjectId = masterObject.id 
        if sonDatasDict:   
            for key,value in sonDatasDict.items():
                sonDatasDict[key][relativeFieldFS] = fatherModel.objects.get(id = masterObjectId)
              
                sonModel.objects.create(**sonDatasDict[key])

    #新增

    #修改
    #得到Model的FS信息
    def getObjectFS(self,modelName,objectId,needDict = False):
         #先查询子表，再查询子子表
        content = {}
        entryObject = apps.get_model(utlitComm.app_name,modelName)

        for sonTable,sonValue in entryObject.sonTableList.items(): #一级子表
            if sonTable == modelName:
                continue
            sonModel =  utlitComm.publicSonTableObjectList[modelName][sonTable] 
            searchSonCondition = {"{}Id".format(modelName):objectId}
            if self.viewType == "View":
                sonObjectList = sonModel.objects.filter(**searchSonCondition)
            else:
                sonObjectList = sonModel.objects.values().filter(**searchSonCondition)

            content[sonTable.lower() + "List"] = sonObjectList
           
            #son id list
            
            sonIdList = [item.id for item in sonObjectList]
            #得到子表ID
            #子表的子表
            for sonSonTable,sonSonValue in sonModel.sonTableList.items():#二级子表
                    searchSonSonCondition = {"{}Id__in".format(sonTable):sonIdList}

                    if self.viewType == "View":
                        sonSonObjectList = utlitComm.publicSonTableObjectList[sonTable][sonSonTable].objects.filter(**searchSonSonCondition) #查询子子表
                    else:
                        sonSonObjectList =  utlitComm.publicSonTableObjectList[sonTable][sonSonTable].objects.values().filter(**searchSonSonCondition) #查询子子表
                    if sonSonTable.lower()  + "List" in content.keys():    
                        content[sonSonTable.lower()  + "List"] = {**content[sonSonTable.lower()  + "List"],**sonSonObjectList}
                    else:
                        content[sonSonTable.lower()  + "List"] = sonSonObjectList 
        contentDict = {} 
        if needDict:#组装成字典，便于ajax返回使用
            from django.forms.models import model_to_dict
            for key,value in content.items(): 
                contentDict[key] = []
                for item in value:
                    
                    contentDict[key] = contentDict[key] + [model_to_dict(item)]  
            content = contentDict  

        return content                     
    #得到编辑信息
    def editProcessFS(self,request,eid,needBlankRecrod = True):
        #得到主表、子表及子子表的信息，并且对信息编号进行组装
        #查询主表
        if self.viewType == "View":
            entryObject= self.entryObject.objects.get(id=eid)
        else:
            entryObject= self.entryObject.objects.values().get(id=eid)
        
        #需要编辑的记录及外键实体
        content = {}
        content[self.entryName.lower()] = entryObject 

        #先查询子表，再查询子子表
        
        for sonTable,sonValue in self.entryObject.sonTableList.items(): #一级子表
            if sonTable == self.entryName:
                continue
              
            sonModel =  utlitComm.publicSonTableObjectList[self.entryName][sonTable] 
            searchSonCondition = {"{}Id".format(self.entryName):eid}
            if self.viewType == "View":
                sonObjectList = sonModel.objects.filter(**searchSonCondition)
            else:
                sonObjectList = sonModel.objects.values().filter(**searchSonCondition)

            content[sonTable.lower() + "List"] = sonObjectList
           
            #son id list
            
            sonIdList = [item.id for item in sonObjectList]
            #得到子表ID
            #子表的子表
            for sonSonTable,sonSonValue in sonModel.sonTableList.items():#二级子表
                    searchSonSonCondition = {"{}Id__in".format(sonTable):sonIdList}

                    if self.viewType == "View":
                        sonSonObjectList = utlitComm.publicSonTableObjectList[sonTable][sonSonTable].objects.filter(**searchSonSonCondition) #查询子子表
                    else:
                        sonSonObjectList =  utlitComm.publicSonTableObjectList[sonTable][sonSonTable].objects.values().filter(**searchSonSonCondition) #查询子子表
                    if sonSonTable.lower()  + "List" in content.keys():    
                        content[sonSonTable.lower()  + "List"] = {**content[sonSonTable.lower()  + "List"],**sonSonObjectList}
                    else:
                        content[sonSonTable.lower()  + "List"] = sonSonObjectList  
            

        #        外键实体
        if needBlankRecrod:
        # #为各个子表增加一个空行
            blankRowList = self.getAllTableBlankRowListFS()
            for key,blankRow in  blankRowList.items():
                for item in content[key]:
                    blankRowList[key].append(item) 

            blankRowList[self.entryName.lower()] = entryObject  
            content = blankRowList 
 
        
        #增加子表下拉框信息 开始   
        objectInfo = self.getObjectFSInfo(content)
        content = {**content,**objectInfo}
        #增加子表下拉框信息 结束
        content = {**content,**self.add_forignObjectDictFS(request)} 
        return content 
    #增加子表下拉框信息    
    def getObjectFSInfo(self,content):
        return {}    
    #得到表空行列表
    def getAllTableBlankRowListFS(self):
        # #为各个子表增加一个空行
            blankRows = self.editProcessFSBlank()
            content = {}
            for key,blankRow in  blankRows.items():
                 rowList = []
                 rowList.append(blankRow)
                 content[key] = rowList
            return  content            
    #增加一条空白记录，id为0，用于页面新增记录
    def getTableBlankRow(self,tableName,masterTable = ""):
            tableModel =  apps.get_model(utlitComm.app_name,tableName) 
            
            tableBlankRow = {}
            for field in tableModel._meta.fields:
                    if field.name == "id":   
                        tableBlankRow[field.name] = 0
                    elif field.name == masterTable + "Id" and masterTable != '':
                        tableBlankRow[field.name + "_id"] = 0    
                    else:
                        tableBlankRow[field.name] = ''  

            return  tableBlankRow                 
    def editProcessFSBlank(self):
        #得到子表及子子表的信息，并且对信息编号进行组装

        #需要编辑的记录及外键实体
        content = {}
        #先查询子表，再查询子子表
        
        for sonTable,sonValue in self.entryObject.sonTableList.items(): #一级子表
            if sonTable == self.entryName:
                continue
            sonModel = apps.get_model(utlitComm.app_name,sonTable)     
            sonRecordBlank = self.getTableBlankRow(sonTable,masterTable = "")

            content[sonTable.lower()  + "List"] = sonRecordBlank
            #子表的子表
            for sonSonTable,sonSonValue in sonModel.sonTableList.items():#二级子表

                sonSonRecordBlank = self.getTableBlankRow(sonSonTable,masterTable = sonTable)
                
                content[sonSonTable.lower() + "List"] = sonSonRecordBlank

        return  content                       

    #删除
    @transaction.atomic
    def deleteFS(self,request):
        #从前端(html)获取did数据
        did = request.GET.get('did')
        #先删除子表，再删除主表
        for sonTable,sonValue in self.entryObject.sonTableList.items(): #一级子表
            sonModel =  utlitComm.publicSonTableObjectList[self.entryName][sonTable] 
            searchSonCondition = {"{}Id".format(self.entryName):did}
            sonObjectList = sonModel.objects.filter(**searchSonCondition)
            #son id list
            sonIdList = [item.id for item in sonObjectList]
            #得到子表ID
            #子表的子表
            for sonSonTable,sonSonValue in sonModel.sonTableList.items():#二级子表
                    searchSonSonCondition = {"{}Id__in".format(sonTable):sonIdList}
                    utlitComm.publicSonTableObjectList[sonTable][sonSonTable].objects.filter(**searchSonSonCondition).delete() #删除子子表
                    
                    sonObjectList.delete() #删除子表
                    

        #删除主表
        
        self.entryObject.objects.get(id=did).delete()

    #子表和父表数据处理结束    
    def save_add(self,request):
        curTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')   #转换字符串
        

        #判断是否是POST请求
        if request.method == 'POST':

            self.frontEndPathUpdate(request)
            self.logProcess.addOperateLog(request,self.entryNameChinese,action = "新增保存")
            storage_dict = {}
            #得到数据
            if len(self.entryModel.sonTableList.keys()) >0:#页面有子表：
                storage_dict = self.postDataCollectionFS(request)

                message = self.checkInputDataFS(storage_dict) #检查数据
                #添加创建时间
                for topKey,allValues in storage_dict.items():
                    for key,value in allValues.items():
                        for subKey,subValue in value.items():
                            
                            storage_dict[topKey][key][subKey]["CreatedTime"] = curTime        
                    
            else:
                storage_dict = self.postDataCollection(request)
                #创建日期字段设置            
                storage_dict["CreatedTime"] = curTime            
                #检查数据
                message = self.checkContentValid(storage_dict)   

            returnData = {}
            returnPage = ""


            if message["flag"] == 0:
                #保存数据
                if len(self.entryModel.sonTableList.keys()) == 0:#页面有子表：

                    
                    self.entryObject.objects.create(**storage_dict)  
                else:
                    self.manyTablesSaveDataFS(storage_dict)

                #返回列表 
                path_info = request.path_info
                pageParts = path_info.split("/")
                pagePathLen = len(pageParts)
                
                if pagePathLen > 3 and pageParts[pagePathLen-2] == "save_add" and pageParts[pagePathLen-4] == "FrontEnd":
                        
                        returnPage = self.genUrlPath(request,"{}centerlogin".format(pageParts[pagePathLen-3].lower()))
                        
                else:
                        returnPage = self.genUrlPath(request,self.entryIndex)
 
                returnData = { "message":message,"returnPage":returnPage}

                if  self.viewType == "View":
                    return JsonResponse(returnData,
                        safe=False,
                        json_dumps_params={'ensure_ascii':False})  
                else:
                     
                    returnPaths = re.findall("/.+/(.+)WX/(.+)_save_(.+)/",request.path_info)[0]
                    
                    returnPath = ""
                    if returnPaths[0] == "FrontEnd":
                        returnPath = "/pages/{}Center/index/index".format(returnPaths[1])
                    else:
                        returnPath = "/pages/{}/{}/index/index".format(returnPaths[0],returnPaths[1])
           
                    return Response({'status':0, "msg":"操作成功","gotoUrl":returnPath})                                             
                                
            else:
               
                returnData = { "message":message,"returnPage":returnPage}
              
                if  self.viewType == "View":
                    return JsonResponse(returnData,
                        safe=False,
                        json_dumps_params={'ensure_ascii':False})
                else:
                     
                    return Response({'status':1, "msg":message["errorMessage"]}) 
                        
    def updateHardCodeFieldValue(self,content):
        for field in self.entryModel._meta.fields: #所有字段名            
            fielTypeName = type(field).__name__
            fieldName = field.name
            publicDataDict = {}
            mixFieldName = "{}.{}"%(self.entryName,fieldName)
            if fieldName in utlitComm.publicDataDict.keys:
                publicDataDict = utlitComm.publicDataDict[fieldName]["keyValuePair"]
            elif  mixFieldName in utlitComm.publicDataDict.keys:
                publicDataDict = utlitComm.publicDataDict[mixFieldName]["keyValuePair"]
            
            if len(publicDataDict) >0:
                content[self.entryName.lower()][fieldName] = publicDataDict[content[self.entryName.lower()][fieldName]]   
        return content            
        
    def detail(self,request):
        self.frontEndPathUpdate(request)
        self.logProcess.addOperateLog(request,self.entryNameChinese,action = "预览")   
        eid=request.GET.get('eid') 
        content = self.detailProcess(request,eid)
        entryObject = content[self.entryName.lower()] 
        entryObject = utlitComm.updateHardCodeFieldValue(self.entryObject,entryObject,self.entryName)
        content["curEntryObject"]  = entryObject
        
        if self.viewType == "APPView":
            return Response({'status':0, "msg":"操作成功","data":content,"gotoUrl":self.detailHtmlPath}) 
        else:
            return render(request,self.detailHtmlPath,context=content)
        
    #得到图片字段
    def getImageFields(self):
        imageFields = {}
        
        fieldDataCheckDict = self.entryModel.fieldDataCheckDict #默认检查当前view的model

        for  key in fieldDataCheckDict.keys():#实体字段需要检测清单
           
           if fieldDataCheckDict[key]["checkType"] == "图片":  
                imageFields[key] = key

        return imageFields
                    
    def detailProcess(self,request,eid):
        entryObject= self.entryObject.objects.values().get(id=eid)
        #        外键实体      
        content = self.add_forignObjectDict(request,"detail")

        #需要编辑的记录及外键实体
        content[self.entryName.lower()] = entryObject 
        #得到多图片

        imageFields = self.getImageFields()
        for item in entryObject:

            if item in imageFields.keys():
                images = entryObject[item].split(";")
                if len(images) >1:#多张图片
                    content[item+"s"] = images 
        return content   
    #得到编辑信息            
    def edit(self,request,storage_dict = None,message = None): 
        
        self.frontEndPathUpdate(request)
        self.logProcess.addOperateLog(request,self.entryNameChinese,action = "修改")  
        eid=request.GET.get('eid') 
        if storage_dict:
            eid = storage_dict["id"]
         
        if len(self.entryModel.sonTableList.keys()) == 0: 
            content = self.editProcess(request,eid)
        else:
            content = self.editProcessFS(request,eid)

        if storage_dict:
            content[self.entryName.lower()] = storage_dict
        content["message"] = message
        
        if self.viewType == "View":
            
            return render(request,self.editHtmlPath,context=content)
        else:
            return Response({'status':0, "msg":"操作成功","data":content[self.entryName.lower()],"gotoUrl":reverse(self.startPage)})
        
    #得到编辑信息
    def editProcess(self,request,eid):
        if self.viewType == "View":
            entryObject= self.entryObject.objects.get(id=eid)
        else:
            entryObject= self.entryObject.objects.values().get(id=eid)
        
        #        外键实体      
        content = self.add_forignObjectDict(request)

        #需要编辑的记录及外键实体
        content[self.entryName.lower()] = entryObject 
        return content
    def save_edit(self,request):
        #判断表单过来的是否是post请求
        
        curTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')   #转换字符串
        if request.method == 'POST':
            self.frontEndPathUpdate(request)
            self.logProcess.addOperateLog(request,self.entryNameChinese,action = "修改保存")
            #如果是，则获取到相应的信息
            if self.viewType == "View":
                entryId = request.POST.get("curObject_id")
            else:
                entryId = request.data.get("curObject_id")

            storage_dict = {}
            if len(self.entryModel.sonTableList.keys()) >0:#页面有子表：
                storage_dict = self.postDataCollectionFS(request,True)
                
                message = self.checkInputDataFS(storage_dict) #检查数据
                #添加创建时间
                
                for topKey,allValues in storage_dict.items():
                    for key,value in allValues.items():
                        for subKey,subValue in value.items():
                            
                            storage_dict[topKey][key][subKey]["UpdateTime"] = curTime        
                    
            else:

                    storage_dict = self.postDataCollection(request)
                    storage_dict["id"] = entryId
                    message = self.checkContentValid(storage_dict)
                    storage_dict["UpdateTime"] = curTime 
            
            returnData = {}
            returnPage = ""
            if message["flag"] == 0:
            #保存数据
                if len(self.entryModel.sonTableList.keys()) == 0:#页面有子表：
                    self.entryObject.objects.filter(id=entryId).update(**storage_dict)  
                else:
                    self.manyTablesUpdateDataFS(storage_dict)               
                
                try:
                    returnPage = self.entryIndex
                except:
                    returnPage = self.UserCenterIndex

                returnPage = self.genUrlPath(request,returnPage)
                returnData = { "message":message,"returnPage":returnPage}

                if self.viewType == "View":
                    return JsonResponse(returnData,
                        safe=False,
                        json_dumps_params={'ensure_ascii':False})  
                else:
                    callPart = re.findall("/.+/(.+)WX/",request.path_info)[0]
                    
                    return Response({'status':0, "msg":"操作成功","gotoUrl":"/pages/{}/index/index".format(callPart)})  
            else:
                returnData = { "message":message,"returnPage":returnPage}
                if self.viewType == "View":
                    return JsonResponse(returnData,
                        safe=False,
                        json_dumps_params={'ensure_ascii':False})
                else:
                    return Response({'status':1, "msg":message["errorMessage"]})
                                                
    def delete(self,request):
        #从前端(html)获取did数据
        did=request.GET.get('did')
        if did:
            self.frontEndPathUpdate(request)
            self.logProcess.addOperateLog(request,self.entryNameChinese,action = "删除")
            
            #找到该数据，将其删除
            deleteFlag = True
            self.entryObject.objects.get(id=did).delete()
            #如果删除的是用户，某个用户在登录状态，则删除当前用户的登录状态
            if  self.entryName == "Member" and request.session.get('frontusernameid',None): 
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

            if deleteFlag:    
            #删除成功，返回显示页
                if self.viewType == "View":

                    return redirect(reverse(self.entryIndex))
                    
                else:
                    return Response({'status':0, "msg":"操作成功"})
            else:
                   return redirect(reverse(self.entryIndex))
            
    #返回数方式由子类决定
    def deleteReturn(self):
        pass
            
    def delete_all(self,request):
        #先判断发过来的是否是post请求
        if request.method=="POST":
            self.frontEndPathUpdate(request)
            self.logProcess.addOperateLog(request,self.entryNameChinese,action = "批量删除")
            #得到要删除的id列表
            values=request.POST.get('vals')
            values= values.split(",")
            errorMessage = ""
            for i in values:
                if i != '':
                    entryObject = self.entryObject.objects.get(id=i)
                    try:
                        entryObject.delete()
                    except:
                        errorMessage = errorMessage + str(i) + ","
            #删除成功返回显示页
            message = {"flag":0,"errorMessage":""}
            if errorMessage != "":
                 message = {"flag":1,"errorMessage":errorMessage}
                 
            returnPage = self.genUrlPath(request,self.entryIndex)
            returnData = { "message":message,"returnPage":returnPage}
            if self.viewType == "View":

                return JsonResponse(returnData,
                        safe=False,
                        json_dumps_params={'ensure_ascii':False})  
            else:
                return Response({'status':0, "msg":"操作成功","data":returnData})          
            #return redirect(reverse(self.entryIndex))
    #删除完成返回由子类决定
    def  delete_allReturn(self,returnData):
        pass       
    #视频播放      
    def playvedio(self,request):
        vid = request.GET.get("vid")
        entry_detail = self.entryObject.objects.get(id=vid)
        content = {
        'curEntry':entry_detail, 
        }
        #self.playvedioReturn(entry_detail,content)
        if self.viewType == "View":

            if entry_detail:            
                return render(request,self.vedioHtmlPath,context=content)
            else:
                raise Http404("资源不存在")
        else:
            return Response({'status':0, "msg":"操作成功","data":content,"gotoUrl":self.vedioHtmlPath})
    #播放返回由子类决定
    def playvedioReturn(self,content):
        pass
    #得到搜索条件字典
    def getSearchParametersDict(self,request):
        inputParametersDict = {}
        for field in self.entryModel._meta.fields: #所有字段名
            fieldName = field.name
            fieldValue = request.GET.get(fieldName)
            if fieldValue and fieldValue != '':
                inputParametersDict[fieldName] = request.GET.get(fieldName)

        pn = request.GET.get('p')
        if not pn:
            pn = 1
              
        return inputParametersDict,pn
    #数据查询--返回josn
    #inputParametersDict格式：字段名:字段值
    
    def getSearchJosnData(self,inputParametersDict,pn):
        
        query=inputParametersDict
       
        if len(inputParametersDict.keys()) == 0:
            entryObject = self.entryObject.objects.all()
        else:
            entryObject = self.entryObject.objects.filter(**inputParametersDict)
        #将取得的记录传给Paginator，每页显示5条
        paginator=Paginator(entryObject,utlitComm.pageSize)
        page=paginator.page(pn)
        #将page和查询字段传给前端
        context={ 
            "page":page,
            'query':inputParametersDict,
            'pageInfo':utlitComm.getPageBar(self.pageInfoIndex,page,query,pn),
        } 
        return context
        #return JsonResponse(context, safe=False)
    def getSearchJosnDataList(self,request):
        inputParametersDict,pn = self.getSearchParametersDict(request)
        return self.getSearchJosnData(inputParametersDict,pn)

#####################################         以下无具体类无关结束   ################################################  
###############################################                                   公共视图类结束          ####################################### 


################################公共方法开始##############################
def my_decorator(func):
    def wrapper(request, *args, **kwargs):
        return func(request, *args, **kwargs)
    return wrapper

################################公共方法结束##############################

################################视图超类开始##############################
# 为全部请求方法添加装饰器
#@method_decorator(my_decorator,name = 'dispatch')
class PublicView(View):
    def __init__(self):

        View.__init__(self)
        self.basePath = "" 
    #主要函数-调用业务逻辑        
   
    def get(self, request):

        return self.callMehtod(request,None)
        
    def post(self, request):
        
        return self.callMehtod(request,None)
    def callMehtod(self,request,message = None):
        pass    
    #登录检查
    def checkLogin(self, request):
        pass
    #权限检查
    def  SystemRolePermissionsCheck(self, request):
         pass

################################视图超类结束##############################
# 为函数视图准备的装饰器
class EntryViewBase(View,EntryViewBaseTop):
    def __init__(self,entryModel,entryObject,entryName,foreignkeyTableList,entryNameChinese,sonTableList):

        PublicView.__init__(self)
        EntryViewBaseTop.__init__(self,entryModel,entryObject,entryName,foreignkeyTableList,entryNameChinese,viewType = "View",sonTableList = sonTableList)

    def get(self, request):

        return self.callMehtod(request,None)
       
    def post(self, request):
        
        return self.callMehtod(request,None)     
##########################################################################################
#################视图类开始##############            
# 为函数视图准备的装饰器
class EntryView(EntryViewBase):
    def __init__(self,entryModel,entryObject,entryName,foreignkeyTableList,entryNameChinese,sonTableList):

        EntryViewBase.__init__(self,entryModel,entryObject,entryName,foreignkeyTableList,entryNameChinese,sonTableList)
        self.systemLogin = "login" #"/{appName}/Login/login/".format( appName = utlitComm.app_name)
        self.method_decorator_list = ['add','save_add','edit','save_edit','delete','delete_all',"import_excel","export_excel"]
    def __getattribute__(self, item):
        """建议对item进行一下判断，不要全局增加"""
        ret = super().__getattribute__(item)

        if type(ret) == "<class 'method'>":  # 类里面的成员分为三种，method（类方法和实例方法），function（实例方法），int,str...（变量成员），具体需要的时候还是通过type进行判断或者直接通过item来判断
            method_decorator_list = ['add','save_add','edit','save_edit','delete','delete_all',"index","import_excel","export_excel"]
            methodNeedDecorator = item in method_decorator_list
            if methodNeedDecorator:
                def res(*args, **kwargs):
                    #调用权限检查
                    SystemRolePermissionsCheck = self.SystemRolePermissionsCheck(request)
                    if AuthorityChecked == "AuthorityChecked":
                        retu = ret(*args, **kwargs)
                    else:
                        retu = SystemRolePermissionsCheck #logger.warning("接口访问延时18:" + str(time.time() - t) + ",name:" + item)
                    return retu
                
            else:
                return ret(*args, **kwargs)
        else:
            return ret
    def logincheck(self, request):
        adminLogin = request.session.get('is_login',None) 
        if not adminLogin:
               return redirect(reverse(self.systemLogin)) #后台登录页面
        else:
               return "logined"
    #权限检查
    def  SystemRolePermissionsCheck(self, request):
        #return "AuthorityChecked"  
        #从得到账户角色的权限清单，如果该账户目前访问的页面功能不在权限清单内，则提示用户没有该权限，请联系管理员，然后回到系统管理首页。如有有权限，则继续后面的操作。
        #当前访问的功能页面链接
        functionDesc = request.path_info
        #处理新增保存，编辑保存字眼
        
        functionDesc = functionDesc.replace("save_add","add")
        functionDesc = functionDesc.replace("save_edit","edit")
        
        functionDesc = functionDesc.replace("detail","index")
        functionDesc = functionDesc.replace("download_excel","export_excel")
        #如果不需要检查权限，则默认权限以检查
        logincheck = self.logincheck(request)
        if logincheck == "logined":
            if functionDesc not in request.session["userAuthorityDict"].values():#权限不存在
                    message = {}
                    message["flag"] = 0
                    message["message"] = "非常抱歉,您没有操作该页面的权限,请联系管理员咨询"
                    return self.errInfoProcess(request,message)
            else:
                return "AuthorityChecked"  
        else:
            return logincheck

    def callMehtod(self,request,message = None): 
        return super().callMehtod(request,message = None)  
#################视图类结束############## 
#################错误处理类开始############## 
class ErrorInfo(View):
    def __init__(self):
       self.errorHtmlPath = 'public/errorInfo.html' 
    def showErroInfo(self,request,messageInfo,callObject):
        if not messageInfo:
            messageInfo = {}
            messageInfo["message"] = "测试信息"

        return render(request,self.errorHtmlPath,{'erroMessage':messageInfo["message"]})
#################错误处理类结束############## 

#######################按需求增加终端类开始##########################
##############################################################前端数据处理开始############################################################
 
 # 为函数视图准备的装饰器
class FrontEntryView(EntryViewBase):
    def __init__(self,entryModel,entryObject,entryName,foreignkeyTableList,entryNameChinese):

        EntryViewBase.__init__(self,entryModel,entryObject,entryName,foreignkeyTableList,entryNameChinese)
        self.systemLogin = "authorcenterlogin"
    def __getattribute__(self, item):
        """建议对item进行一下判断，不要全局增加"""
        ret = super().__getattribute__(item)

        #装饰方法清单
        method_decorator_list = ['add','save_add','edit','save_edit','delete','delete_all']
        methodNeedDecorator = item in method_decorator_list
        
        if methodNeedDecorator and type(ret) == "<class 'method'>":  # 类里面的成员分为三种，method（类方法和实例方法），function（实例方法），int,str...（变量成员），具体需要的时候还是通过type进行判断或者直接通过item来判断
            def res(*args, **kwargs):
                #调用权限检查
                SystemRolePermissionsCheck = self.SystemRolePermissionsCheck(request)
                if AuthorityChecked == "AuthorityChecked":
                    retu = ret(*args, **kwargs)
                else:
                    retu = SystemRolePermissionsCheck #logger.warning("接口访问延时18:" + str(time.time() - t) + ",name:" + item)
                return retu
            return res
        else:
            return ret
    def logincheck(self, request):
        adminLogin = request.session.get('frontusername_is_login',None) 
        if adminLogin:
               return redirect(reverse(self.systemLogin)) #前台登录页面
        else:
               return "logined"
    #权限检查
    def  SystemRolePermissionsCheck(self, request):
       
        #从得到账户角色的权限清单，如果该账户目前访问的页面功能不在权限清单内，则提示用户没有该权限，请联系管理员，然后回到系统管理首页。如有有权限，则继续后面的操作。
        #当前访问的功能页面链接
        functionDesc = request.path_info
        #处理新增保存，编辑保存字眼
        
        functionDesc = functionDesc.replace("save_add","add")
        functionDesc = functionDesc.replace("save_edit","edit")
        
        functionDesc = functionDesc.replace("detail","edit")
        #如果不需要检查权限，则默认权限以检查
        logincheck = self.logincheck(request)
        if logincheck == "logined":
            return "AuthorityChecked"  
        else:
            return logincheck  
    def callMehtod(self,request,message = None): 
        return  super().callMehtod(request,message = None)

##############################################################前端数据处理结束############################################################


      
#######################按需求增加终端类结束##########################
#######################日志处理开始##########################
class LogProcess():
    def __init__(self):
        pass

    def get_client_ip(self,request):
        try:
          real_ip = request.META['HTTP_X_FORWARDED_FOR']
          regip = real_ip.split(",")[0]
        except:
          try:
            regip = request.META['REMOTE_ADDR']
          except:
            regip = ""
        return regip

    def addOperateLog(self,request,entryNameChinese,action):

        return
            
        path_info = request.path_info
        BrowseTerminal = "PC"
        IPAddress = self.get_client_ip(request)
        WeChatNickname = ""
        ActionURL = path_info
        keyValuePair = utlitComm.publicDataDict["BrowseTerminal"]["keyValuePair"]
        print(path_info)
        if path_info.find("/admin/") >0: #后台操作
            self.AddSystemOperationLog(request,entryNameChinese,action)
        else:
            if  path_info.find("Center/") >0: #前台操作:
            #PC端前端
                MemberId = request.session.get('frontusernameid',None) 
                
            #WX
            elif path_info.find("CenterWX/") >0: #小程序操作
                MemberId = request.session.get('frontusernameid',None) 
                BrowseTerminal = "微信小程序"
                IPAddress = ""
                WeChatNickname = ""
            #其它
            self.AddMemberLoginLog(request,MemberId,ActionURL,action,entryNameChinese,WeChatNickname ,IPAddress,BrowseTerminal )

    def AddSystemOperationLog(self,request,entryNameChinese,action):
        pass
    def AddMemberLoginLog(slef,request,MemberId,ActionURL,action,entryNameChinese,WeChatNickname = "",IPAddress = "",BrowseTerminal = ""):
        pass        
    
#######################日志处理结束##########################



