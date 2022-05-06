from django.db import models

# Create your models here.
class ImageTags(models.Model):
	id = models.AutoField(primary_key=True)

	
	CreatedTime = models.CharField(max_length=20,default ='',null=True,help_text="创建时间",verbose_name = "创建时间",db_column = "CreatedTime")

	UpdateTime = models.CharField(max_length=20,default ='',null=True,help_text="更新时间",verbose_name = "更新时间",db_column = "UpdateTime")

	ImageInformationId = models.ForeignKey(to='ImageInformation',null= True,blank = True,on_delete=models.CASCADE,help_text="图片",verbose_name = "图片",db_column = "ImageInformationId")

	ImageTagInfo = models.CharField(max_length=100,default ='',null=True,help_text="标签",verbose_name = "标签",db_column = "ImageTagInfo")

	fieldDataCheckDict = {}               
	foreignkeyTableList =  {'ImageInformationId': 'ImageInformation'}
	sonTableList =  {}
	 

	class Meta:
		ordering=['id'] #默认排序
		app_label = 'ImageRecommendationSystem'
        
		db_table = 'ImageTags'     
		verbose_name = '图片标签'  #用于后台admin单数
		verbose_name_plural = '图片标签'   #用于后台admin复数    