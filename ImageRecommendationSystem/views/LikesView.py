from django.shortcuts import render, redirect
#引用的model清单，包括外键和本身
from ImageRecommendationSystem.models import LikesModel
from ImageRecommendationSystem.models import ImageInformationModel
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
                        
        }
        return fieldDataCheckDict  


#############PC接口
class  Likes(PublicView.EntryView):
    def __init__(self):    
        entryModel = LikesModel.Likes
        entryObject =  LikesModel.Likes
        entryName = "Likes"
        entryNameChinese = "点赞"
        foreignkeyTableList =  {'ImageInformationId': 'ImageInformation', 'MemberId': 'Member'}
        sonTableList =  {}
        PublicView.EntryView.__init__(self,entryModel,entryObject,entryName,foreignkeyTableList,entryNameChinese,sonTableList)    

    def index_query(self,request,query):
        return  LikesModel.Likes.objects.values().filter(Q( __contains=query))

    def fieldDataCheckDict(self):
        return fieldDataCheckDict() 


