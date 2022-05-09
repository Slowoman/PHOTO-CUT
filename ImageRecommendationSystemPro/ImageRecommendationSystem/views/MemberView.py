from django.shortcuts import render, redirect
#引用的model清单，包括外键和本身
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
            
        "PhoneNumber":{"checkType":"手机号","FieldChineseName":"手机号"},
        
        "WeChatAvatarPicture":{"checkType":"图片","FieldChineseName":"微信头像图片"},
        
        "Password":{"checkType":"密码","FieldChineseName":"密码"},
        
        "Email":{"checkType":"邮箱","FieldChineseName":"E-mail"},
                    
        }
        return fieldDataCheckDict  


#############PC接口
class  Member(PublicView.EntryView):
    def __init__(self):    
        entryModel = MemberModel.Member
        entryObject =  MemberModel.Member
        entryName = "Member"
        entryNameChinese = "用户"
        foreignkeyTableList =  {}
        sonTableList =  {}
        PublicView.EntryView.__init__(self,entryModel,entryObject,entryName,foreignkeyTableList,entryNameChinese,sonTableList)    

    def index_query(self,request,query):
        return  MemberModel.Member.objects.values().filter(Q( Name__contains=query))

    def fieldDataCheckDict(self):
        return fieldDataCheckDict() 


