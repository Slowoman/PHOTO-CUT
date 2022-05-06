from django.db import models

# Create your models here.
class ImageType(models.Model):
	id = models.AutoField(primary_key=True)

	
	CreatedTime = models.CharField(max_length=20,default ='',null=True,help_text="创建时间",verbose_name = "创建时间",db_column = "CreatedTime")

	UpdateTime = models.CharField(max_length=20,default ='',null=True,help_text="更新时间",verbose_name = "更新时间",db_column = "UpdateTime")

	Name = models.CharField(max_length=20,default ='',null=True,help_text="名称",verbose_name = "名称",db_column = "Name")

	Description = models.CharField(max_length=100,default ='',null=True,help_text="描述",verbose_name = "描述",db_column = "Description")

	fieldDataCheckDict = {}               
	foreignkeyTableList =  {}
	sonTableList =  {}
	

	def __str__(self):

		return self.Name 

	class Meta:
		ordering=['id'] #默认排序
		app_label = 'ImageRecommendationSystem'
        
		db_table = 'ImageType'     
		verbose_name = '图片类型'  #用于后台admin单数
		verbose_name_plural = '图片类型'   #用于后台admin复数    