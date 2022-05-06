from django.shortcuts import render, redirect
#引用的model清单，包括外键和本身
from ImageRecommendationSystem.models import CommentLikesModel
from ImageRecommendationSystem.models import ImageInformationModel
from ImageRecommendationSystem.models import MemberModel
from ImageRecommendationSystem.models import CommentModel

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
class  CommentLikes(PublicView.EntryView):
    def __init__(self):    
        entryModel = CommentLikesModel.CommentLikes
        entryObject =  CommentLikesModel.CommentLikes
        entryName = "CommentLikes"
        entryNameChinese = "评论点赞"
        foreignkeyTableList =  {'ImageInformationId': 'ImageInformation', 'MemberId': 'Member', 'CommentId': 'Comment'}
        sonTableList =  {}
        PublicView.EntryView.__init__(self,entryModel,entryObject,entryName,foreignkeyTableList,entryNameChinese,sonTableList)    

    def index_query(self,request,query):
        return  CommentLikesModel.CommentLikes.objects.values().filter(Q( __contains=query))

    def fieldDataCheckDict(self):
        return fieldDataCheckDict() 


