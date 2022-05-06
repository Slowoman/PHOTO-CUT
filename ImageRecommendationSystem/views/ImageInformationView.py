from django.shortcuts import render, redirect
#引用的model清单，包括外键和本身
from ImageRecommendationSystem.models import ImageInformationModel
from ImageRecommendationSystem.models import ImageTypeModel
from ImageRecommendationSystem.models import MemberModel

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

def fieldDataCheckDict():
        
        fieldDataCheckDict = {
            
        "ImageLink":{"checkType":"图片","FieldChineseName":"图片链接"},
                    
        }
        return fieldDataCheckDict  


#############PC接口
class  ImageInformation(PublicView.EntryView):
    def __init__(self):    
        entryModel = ImageInformationModel.ImageInformation
        entryObject =  ImageInformationModel.ImageInformation
        entryName = "ImageInformation"
        entryNameChinese = "图片信息"
        foreignkeyTableList =  {'ImageTypeId': 'ImageType', 'MemberId': 'Member'}
        sonTableList =  {}
        PublicView.EntryView.__init__(self,entryModel,entryObject,entryName,foreignkeyTableList,entryNameChinese,sonTableList)    

    def index_query(self,request,query):
        return  ImageInformationModel.ImageInformation.objects.values().filter(Q( WorkDescription__contains=query))

    def fieldDataCheckDict(self):
        return fieldDataCheckDict() 


