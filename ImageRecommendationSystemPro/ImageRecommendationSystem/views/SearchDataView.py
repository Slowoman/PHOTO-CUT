from django.shortcuts import render, redirect
#引用的model清单，包括外键和本身
#from ImageRecommendationSystem.models import authorModel

import datetime
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
import os
from ImageRecommendationSystemPro.settings import * #项目设置

from django.views import View
from django.http import Http404
from ImageRecommendationSystem.models  import *  #view共有函数
from django.urls import path,re_path 
from django.shortcuts import reverse

from ImageRecommendationSystem.views  import utlitComm  #view共有函数



class  SearchData():
    def __init__(self,entryModel,entryObject,pageInfoIndex):  
        self.entryObject = entryObject
        self.entryModel = entryModel
        self.pageInfoIndex = pageInfoIndex
    #获取某页数据
    def getSearchJosnData(self,inputParametersDict,pn):
        
        query=inputParametersDict

        if not inputParametersDict or len(inputParametersDict.keys()) == 0:

            entryObject = self.entryObject.objects.values().all()
            query = ''

        else:
            entryObject = self.entryObject.objects.values().filter(**inputParametersDict)
            print(entryObject)
        
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
            }
        except:
               page = {}
               context={ 
                "page":page,
                'query':inputParametersDict,
                'pageInfo':'',
              }
        #print(context)     
        return context
        #return JsonResponse(context, safe=False)  
    def getDetailData(self,eid):
        content = {}
        entryObject= self.entryObject.objects.values().get(id=eid)
        entryObject = utlitComm.updateHardCodeFieldValue(self.entryObject,entryObject)
        #需要编辑的记录及外键实体
        content["curEntryObject"] = entryObject 
        return content
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
            print(feildValue)
            if len(feildValue)==2 and feildValue[1] != '':
                fieldName = feildValue[0]
                fieldValue = feildValue[1]
                inputParametersDict[fieldName + "__icontains"]  = fieldValue      
        pn = request.GET.get('p')
        if not pn:
            pn = 1
              
        return inputParametersDict,pn  