from django.db import models

# Create your models here.
class Member(models.Model):
	id = models.AutoField(primary_key=True)

	
	CreatedTime = models.CharField(max_length=20,default ='',null=True,help_text="创建时间",verbose_name = "创建时间",db_column = "CreatedTime")

	UpdateTime = models.CharField(max_length=20,default ='',null=True,help_text="更新时间",verbose_name = "更新时间",db_column = "UpdateTime")

	Name = models.CharField(max_length=10,default ='',null=False,help_text="名称",verbose_name = "名称",db_column = "Name")

	PhoneNumber = models.CharField(max_length=11,default ='',null=True,help_text="手机号",verbose_name = "手机号",db_column = "PhoneNumber")

	WechatNickname = models.CharField(max_length=20,default ='',null=True,help_text="微信号昵称",verbose_name = "微信号昵称",db_column = "WechatNickname")

	WeChatAvatarPicture = models.FileField(upload_to='upload',null= True,blank = True,help_text="微信头像图片",verbose_name = "微信头像图片",db_column = "WeChatAvatarPicture")

	Password = models.CharField(max_length=20,default ='',null=False,help_text="密码",verbose_name = "密码",db_column = "Password")

	LastLoginTime = models.CharField(max_length=20,default ='',null=True,help_text="最近登录时间",verbose_name = "最近登录时间",db_column = "LastLoginTime")

	Email = models.CharField(max_length=50,default ='',null=True,help_text="E-mail",verbose_name = "E-mail",db_column = "Email")

	CanUsed = models.CharField(max_length=2,default ='',null=True,help_text="启用",verbose_name = "启用",db_column = "CanUsed")

	NameSurname = models.CharField(max_length=20,default ='',null=True,help_text="姓名",verbose_name = "姓名",db_column = "NameSurname")

	Gender = models.CharField(max_length=2,default ='',null=True,help_text="性别",verbose_name = "性别",db_column = "Gender")

	Telephone = models.CharField(max_length=20,default ='',null=True,help_text="电话",verbose_name = "电话",db_column = "Telephone")

	Area = models.CharField(max_length=50,default ='',null=True,help_text="地区",verbose_name = "地区",db_column = "Area")

	Introduction = models.CharField(max_length=500,default ='',null=True,help_text="简介",verbose_name = "简介",db_column = "Introduction")

	fieldDataCheckDict = {
        "PhoneNumber":{"checkType":"手机号","FieldChineseName":"手机号"},
        
        "WeChatAvatarPicture":{"checkType":"图片","FieldChineseName":"微信头像图片"},
        
        "Password":{"checkType":"密码","FieldChineseName":"密码"},
        
        "Email":{"checkType":"邮箱","FieldChineseName":"E-mail"},
        }               
	foreignkeyTableList =  {}
	sonTableList =  {}
	

	def __str__(self):

		return self.Name 

	class Meta:
		ordering=['id'] #默认排序
		app_label = 'ImageRecommendationSystem'
        
		db_table = 'Member'     
		verbose_name = '用户'  #用于后台admin单数
		verbose_name_plural = '用户'   #用于后台admin复数    