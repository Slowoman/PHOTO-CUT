from django.db import models

# Create your models here.
class HomeBanner(models.Model):
	id = models.AutoField(primary_key=True)

	
	CreatedTime = models.CharField(max_length=20,default ='',null=True,help_text="创建时间",verbose_name = "创建时间",db_column = "CreatedTime")

	UpdateTime = models.CharField(max_length=20,default ='',null=True,help_text="更新时间",verbose_name = "更新时间",db_column = "UpdateTime")

	Name = models.CharField(max_length=20,default ='',null=False,help_text="名称",verbose_name = "名称",db_column = "Name")

	PictureAddress = models.FileField(upload_to='upload',null= True,blank = True,help_text="图片地址",verbose_name = "图片地址",db_column = "PictureAddress")

	LinkAddress = models.CharField(max_length=150,default ='',null=False,help_text="链接地址",verbose_name = "链接地址",db_column = "LinkAddress")

	CanUsed = models.CharField(max_length=2,default ='',null=True,help_text="启用",verbose_name = "启用",db_column = "CanUsed")

	ShowTitle = models.CharField(max_length=20,default ='',null=True,help_text="标题",verbose_name = "标题",db_column = "ShowTitle")

	Content = models.CharField(max_length=50,default ='',null=True,help_text="内容",verbose_name = "内容",db_column = "Content")

	fieldDataCheckDict = {
        "PictureAddress":{"checkType":"图片","FieldChineseName":"图片地址"},
        }               
	foreignkeyTableList =  {}
	sonTableList =  {}
	

	def __str__(self):

		return self.Name 

	class Meta:
		ordering=['id'] #默认排序
		app_label = 'ImageRecommendationSystem'
        
		db_table = 'HomeBanner'     
		verbose_name = '首页Banner'  #用于后台admin单数
		verbose_name_plural = '首页Banner'   #用于后台admin复数    