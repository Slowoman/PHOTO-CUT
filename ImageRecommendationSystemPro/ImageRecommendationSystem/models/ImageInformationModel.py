from django.db import models

# Create your models here.
class ImageInformation(models.Model):
	id = models.AutoField(primary_key=True)

	
	CreatedTime = models.CharField(max_length=20,default ='',null=True,help_text="创建时间",verbose_name = "创建时间",db_column = "CreatedTime")

	UpdateTime = models.CharField(max_length=20,default ='',null=True,help_text="更新时间",verbose_name = "更新时间",db_column = "UpdateTime")

	ImageTypeId = models.ForeignKey(to='ImageType',null= True,blank = True,on_delete=models.CASCADE,help_text="图片类型",verbose_name = "图片类型",db_column = "ImageTypeId")

	Name = models.CharField(max_length=20,default ='',null=True,help_text="标题",verbose_name = "标题",db_column = "Name")

	WorkDescription = models.CharField(max_length=1000,default ='',null=True,help_text="作品描述",verbose_name = "作品描述",db_column = "WorkDescription")

	ImageLink = models.FileField(upload_to='upload',null= True,blank = True,help_text="图片链接",verbose_name = "图片链接",db_column = "ImageLink")

	MemberId = models.ForeignKey(to='Member',null= True,blank = True,on_delete=models.CASCADE,help_text="作者",verbose_name = "作者",db_column = "MemberId")

	ImageTags = models.CharField(max_length=500,default ='',null=True,help_text="标签",verbose_name = "标签",db_column = "ImageTags")

	fieldDataCheckDict = {
        "ImageLink":{"checkType":"图片","FieldChineseName":"图片链接"},
        }               
	foreignkeyTableList =  {'ImageTypeId': 'ImageType', 'MemberId': 'Member'}
	sonTableList =  {}
	

	def __str__(self):

		return self.Name 

	class Meta:
		ordering=['id'] #默认排序
		app_label = 'ImageRecommendationSystem'
        
		db_table = 'ImageInformation'     
		verbose_name = '图片信息'  #用于后台admin单数
		verbose_name_plural = '图片信息'   #用于后台admin复数    