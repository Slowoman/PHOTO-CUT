from django.db import models

# Create your models here.
class CommentLikes(models.Model):
	id = models.AutoField(primary_key=True)

	
	CreatedTime = models.CharField(max_length=20,default ='',null=True,help_text="创建时间",verbose_name = "创建时间",db_column = "CreatedTime")

	UpdateTime = models.CharField(max_length=20,default ='',null=True,help_text="更新时间",verbose_name = "更新时间",db_column = "UpdateTime")

	ImageInformationId = models.ForeignKey(to='ImageInformation',null= True,blank = True,on_delete=models.CASCADE,help_text="图片",verbose_name = "图片",db_column = "ImageInformationId")

	MemberId = models.ForeignKey(to='Member',null= True,blank = True,on_delete=models.CASCADE,help_text="用户",verbose_name = "用户",db_column = "MemberId")

	CommentId = models.ForeignKey(to='Comment',null= True,blank = True,on_delete=models.CASCADE,help_text="评论",verbose_name = "评论",db_column = "CommentId")

	fieldDataCheckDict = {}               
	foreignkeyTableList =  {'ImageInformationId': 'ImageInformation', 'MemberId': 'Member', 'CommentId': 'Comment'}
	sonTableList =  {}
	 

	class Meta:
		ordering=['id'] #默认排序
		app_label = 'ImageRecommendationSystem'
        
		db_table = 'CommentLikes'     
		verbose_name = '评论点赞'  #用于后台admin单数
		verbose_name_plural = '评论点赞'   #用于后台admin复数    