from django.db import models

# Create your models here.
class SystemAccount(models.Model):
	id = models.AutoField(primary_key=True)

	
	CreatedTime = models.CharField(max_length=20,default ='',null=True,help_text="创建时间",verbose_name = "创建时间",db_column = "CreatedTime")

	UpdateTime = models.CharField(max_length=20,default ='',null=True,help_text="更新时间",verbose_name = "更新时间",db_column = "UpdateTime")

	Name = models.CharField(max_length=20,default ='',null=False,help_text="名称",verbose_name = "名称",db_column = "Name")

	SystemRoleId = models.IntegerField(default=0,null= True,blank = True,help_text="角色",verbose_name = "角色",db_column = "SystemRoleId")

	Password = models.CharField(max_length=20,default ='',null=False,help_text="密码",verbose_name = "密码",db_column = "Password")

	CanUsed = models.CharField(max_length=2,default ='',null=True,help_text="启用",verbose_name = "启用",db_column = "CanUsed")

	fieldDataCheckDict = {}               
	foreignkeyTableList =  {}
	sonTableList =  {}
	

	def __str__(self):

		return self.Name 

	class Meta:
		ordering=['id'] #默认排序
		app_label = 'ImageRecommendationSystem'
        
		db_table = 'SystemAccount'     
		verbose_name = '系统账户'  #用于后台admin单数
		verbose_name_plural = '系统账户'   #用于后台admin复数    