from django.db import models

# Create your models here.
class FocusOn(models.Model):
	id = models.AutoField(primary_key=True)

	
	CreatedTime = models.CharField(max_length=20,default ='',null=True,help_text="创建时间",verbose_name = "创建时间",db_column = "CreatedTime")

	UpdateTime = models.CharField(max_length=20,default ='',null=True,help_text="更新时间",verbose_name = "更新时间",db_column = "UpdateTime")

	MemberId = models.ForeignKey(to='Member',null= True,blank = True,on_delete=models.CASCADE,help_text="用户",verbose_name = "用户",db_column = "MemberId")

	FanId = models.IntegerField(default=0,null= True,blank = True,help_text="粉丝",verbose_name = "粉丝",db_column = "FanId")

	fieldDataCheckDict = {}               
	foreignkeyTableList =  {'MemberId': 'Member'}
	sonTableList =  {}
	 

	class Meta:
		ordering=['id'] #默认排序
		app_label = 'ImageRecommendationSystem'
        
		db_table = 'FocusOn'     
		verbose_name = '关注'  #用于后台admin单数
		verbose_name_plural = '关注'   #用于后台admin复数    