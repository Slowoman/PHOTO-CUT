from django.db import models

# Create your models here.
class SearchHistory(models.Model):
	id = models.AutoField(primary_key=True)

	
	CreatedTime = models.CharField(max_length=20,default ='',null=True,help_text="创建时间",verbose_name = "创建时间",db_column = "CreatedTime")

	UpdateTime = models.CharField(max_length=20,default ='',null=True,help_text="更新时间",verbose_name = "更新时间",db_column = "UpdateTime")

	ImageInformationId = models.ForeignKey(to='ImageInformation',null= True,blank = True,on_delete=models.CASCADE,help_text="图片",verbose_name = "图片",db_column = "ImageInformationId")

	MemberId = models.ForeignKey(to='Member',null= True,blank = True,on_delete=models.CASCADE,help_text="用户",verbose_name = "用户",db_column = "MemberId")

	Content = models.CharField(max_length=200,default ='',null=True,help_text="内容",verbose_name = "内容",db_column = "Content")

	fieldDataCheckDict = {}               
	foreignkeyTableList =  {'ImageInformationId': 'ImageInformation', 'MemberId': 'Member'}
	sonTableList =  {}
	 

	class Meta:
		ordering=['id'] #默认排序
		app_label = 'ImageRecommendationSystem'
        
		db_table = 'SearchHistory'     
		verbose_name = '搜索记录'  #用于后台admin单数
		verbose_name_plural = '搜索记录'   #用于后台admin复数    