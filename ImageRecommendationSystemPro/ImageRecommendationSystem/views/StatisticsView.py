from django.shortcuts import render, redirect

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
from django.db.models import Count
from datetime import datetime
from django.apps import apps
from django.db.models import Sum,Count
class Statistics(PublicView.PublicView):
    def __init__(self,entryObject,entryModel,entryName,searchDateTimeFieldName,statisticsFileName,statisticsFileNameChinese):    
        PublicView.PublicView.__init__(self)
        self.basePath = "Statistics"
        self.detailHtmlPath = "{}/index.html".format(self.basePath)

        self.entryObject = entryObject 
        self.entryModel = entryModel 
        self.entryName = entryName 
        self.pageInfoIndex = 'admin/Statistics/{}.html'.format(statisticsFileName) 
        self.queryCondition = {}
        self.inputParametersDict = {}
        self.searchDateTimeFieldName = searchDateTimeFieldName
        self.statisticsFileNameChinese = statisticsFileNameChinese
        #日志
        self.logProcess = PublicView.LogProcess()                   
            
    def callMehtod(self,request,message = None):

        return self.searchData(request)

    def searchData(self,request):
        self.logProcess.AddSystemOperationLog(request,self.statisticsFileNameChinese,action = "查看") 
        self.getSearchParametersDict(request)

        indexDataMix = self.indexDataMix(request)
        print(indexDataMix)
        return render(request,self.pageInfoIndex,context=indexDataMix) 

    def indexDataMix(self,request):
        content = {   
        "Summary":self.getSummary(request),
        "DaySummary":self.getDaySummary(request),
        "{}".format(self.entryName):self.queryCondition,
         }
        return content 
    def indexResponseData(self,request):
         #组装首页数据
        content = self.indeDataMix()
        return HttpResponse(content)      
   
    #得到查询字段
    def getSearchParametersDict(self,request):
        inputParametersDict = {}
        for field in self.entryObject._meta.fields: #所有字段名
            fieldName = field.name
            fieldValue = request.GET.get(fieldName)
            if fieldValue and fieldValue != '':
                if fielTypeName == "CharField":
                    inputParametersDict[fieldName + "__contains"] = fieldValue
                else:
                    inputParametersDict[fieldName] = fieldValue
                    
                self.queryCondition[fieldName] = fieldValue
            #处理时间段
            if fieldValue == None:

               fieldValue = request.GET.get(fieldName + "Start")
               if fieldValue and fieldValue != '':  
                    inputParametersDict[fieldName + "__gte"] = fieldValue  
                    self.queryCondition[fieldName + "Start"] = fieldValue
               
               fieldValue = request.GET.get(fieldName + "End")
               if fieldValue and fieldValue != '':  
                        inputParametersDict[fieldName + "__lte" ] = fieldValue 
                        self.queryCondition[fieldName + "End"] = fieldValue 
        #设置默认日期
        if  "{}__gte".format(self.searchDateTimeFieldName) not in  inputParametersDict.keys():
               inputParametersDict["{}__gte".format(self.searchDateTimeFieldName)]  = datetime.now().strftime("%Y-%m-%d 00:00:00")  
               inputParametersDict["{}__lte".format(self.searchDateTimeFieldName)]  =  datetime.now().strftime("%Y-%m-%d 23:59:59")  

        print(self.queryCondition)
        print(inputParametersDict)
        self.inputParametersDict = inputParametersDict

    #得到查询的日期范围
    def getSearchDateList(self):
        import datetime 
        #得到日期列表
        searchDateList = []
        fromDate = self.inputParametersDict["{}__gte".format(self.searchDateTimeFieldName)][:10].split("-") 
        endDate =  self.inputParametersDict["{}__lte".format(self.searchDateTimeFieldName)][:10].split("-") 
        start = datetime.date(int(fromDate[0]),int(fromDate[1]),int(fromDate[2]))
        end = datetime.date(int(endDate[0]),int(endDate[1]),int(endDate[2])) 
        days = (end-start).days + 1
        print(days)
        for i in range(days):
            tempDate = start + datetime.timedelta(days=i)
            searchDateList.append(tempDate.strftime("%Y-%m-%d")) 
        return searchDateList
    #满足条件的指定数据项总额数据 
    def getSummary(self,request):        
        pass
    #满足条件的指定数据项按天总额数据
    def getDaySummary(self,request):        
        pass
######################################

######################################
from ImageRecommendationSystem.models  import BrowsingHistoryModel
class BrowsingHistoryStatistics(Statistics):
    def __init__(self): 
        entryObject = BrowsingHistoryModel.BrowsingHistory
        entryModel = BrowsingHistoryModel 
        entryName = "BrowsingHistory"  
        searchDateTimeFieldName = "CreatedTime"
        statisticsFileName = 'BrowsingHistoryStatistics'
        statisticsFileNameChinese = '图片点击统计'
        Statistics.__init__(self,entryObject,entryModel,entryName,searchDateTimeFieldName,statisticsFileName,statisticsFileNameChinese)

  #满足条件的指定数据项总额数据 
    def getSummary(self,request):       
        inputParametersDict = self.inputParametersDict 
        if len(inputParametersDict.items()) >0:
            curObjList = self.entryObject.objects.filter(**inputParametersDict).aggregate(ImageInformationIdCount=Count('ImageInformationId'),idCount=Count('id'))
        else:
            curObjList = self.entryObject.objects.aggregate(ImageInformationIdCount=Count('ImageInformationId'),idCount=Count('id'))

        if len(curObjList) == 0:
            
            ImageInformationIdCount = 0     
        
            idCount = 0     
                    
        else:
            
            ImageInformationIdCount = curObjList["ImageInformationIdCount"]         
        
            idCount = curObjList["idCount"]         
        
        returnData = {'ImageInformationIdCount':ImageInformationIdCount,'idCount':idCount}
        return returnData 
    #满足条件的指定数据项按天总额数据
    def getDaySummary(self,request):       
        inputParametersDict = self.inputParametersDict 
        groupField = "{}1".format(self.searchDateTimeFieldName)
        groupField = "ImageInformationId"
        curObjList = self.entryObject.objects.values(groupField)\
                    .filter(**inputParametersDict)\
                    .annotate(ImageInformationIdCount=Count(groupField),idCount=Count('id'))\
                    .order_by(groupField)                   
        #得到日期列表
        print("curObjList:")
        print(curObjList)
        searchDateList = self.getSearchDateList() 
        
        ImageInformationIdCountList = []                              
        
        idCountList = []                              
        
           
        ImageInformationIdCount = 0     
    
        idCount = 0     
        ImageInformationNameList = []
        ImageInformationIdList = []
        ImageInformationIdCountDict = {}

        for k in range(len(curObjList)):
            
                ImageInformationIdCount = curObjList[k]["ImageInformationIdCount"]                    
                 
                idCount = curObjList[k]["idCount"]                    
                ImageInformationIdList.append(curObjList[k]["ImageInformationId"])
                ImageInformationIdCountList.append(ImageInformationIdCount)
            
                idCountList.append(idCount)
                ImageInformationIdCountDict[curObjList[k]["ImageInformationId"]] = ImageInformationIdCount

        tableName = "ImageInformation"
        print(ImageInformationIdList)
        inputParametersDict = {"id__in":ImageInformationIdList}
        ModelObject = apps.get_model(utlitComm.app_name,tableName)
        infoDetail = ModelObject.objects.filter(**inputParametersDict)
        print(infoDetail)
        infoDetailDict = {}

        ImageInformationTypeNameDict = {}
        ImageInformationTypeValue = []
        ImageInformationTypeName = []
        print(infoDetail)
        for item in infoDetail:
            print(item.ImageTypeId)
            infoDetailDict[item.id] = item.Name
            if item.ImageTypeId in ImageInformationTypeNameDict.keys():
                ImageInformationTypeNameDict[item.ImageTypeId] +=  "," + str(item.id)
            else:
                ImageInformationTypeNameDict[item.ImageTypeId] = str(item.id)
           
        print(infoDetailDict)    
        for item in ImageInformationIdList:
            ImageInformationNameList.append(infoDetailDict[item]) 

        for key,value in ImageInformationTypeNameDict.items():
               ImageInformationTypeName.append(str(key))
               ids = value.split(",") 
               tempValue = 0
               for curId in ids:
                    tempValue += ImageInformationIdCountDict[int(curId)]
               ImageInformationTypeValue.append(tempValue)
        #得到分类统计

        
        returnData = {"searchDateList":ImageInformationNameList,"ImageInformationIdCountList":ImageInformationIdCountList,
        "idCountList":idCountList,
        "ImageInformationTypeName":ImageInformationTypeName,
        "ImageInformationTypeValue":ImageInformationTypeValue}
        print(returnData)
        return returnData 
