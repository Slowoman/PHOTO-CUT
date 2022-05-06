from django.core.paginator import Paginator, EmptyPage
import html
import os
import datetime
from django.apps import apps
from pathlib import Path
from ImageRecommendationSystemPro.settings import *
from django.db.models import Sum,Count
app_name = "ImageRecommendationSystem"
app_name_Chinese = "图片推荐系统"
pageSize = 8
pageCountEveryPage = 10
from ImageRecommendationSystem.models  import * 
#公用数据
publicDataDict = {
	'MenuType':{'ChineseName': '菜单类别', 'keyValuePair': {'1': '后台', '2': '前端顶部', '3': '作者', '4': '前端左部'}},
'CanUsed':{'ChineseName': '功能可用', 'keyValuePair': {'2': '使用', '3': '禁用'}},
'FunctionName':{'ChineseName': '功能', 'keyValuePair': {'1': '增加', '2': '删除', '3': '修改', '4': '查询'}},
'ItemChoosen':{'ChineseName': '选中', 'keyValuePair': {'1': '选中', '0': '不选'}},
'Gender':{'ChineseName': '性别', 'keyValuePair': {'2': '男', '3': '女'}}
}
#正则检测字典
publicRegDict =  {
	'日期时间':{'EnglishName': 'Time', 'regExpress': '(\\d{4}-\\d{2}-\\d{2})\\s(\\d{2}:\\d{2}:\\d{2})'},
'密码':{'EnglishName': 'Password', 'regExpress': '[0-9A-Za-z]{6,16}$'},
'图片':{'EnglishName': 'Picture', 'regExpress': '.+(.jpg|.JPEG|.PNG|.GIF)$'},
'视频':{'EnglishName': 'Video', 'regExpress': '.+(.flv|.rvmb|.mp4|.avi|.wmv)$'},
'数字':{'EnglishName': 'Number', 'regExpress': '^\\d+(.\\d+)?$'},
'网址':{'EnglishName': 'URLAddress', 'regExpress': '^(http|ftp|https):\\/\\/([\\w\\-]+(\\.[\\w\\-]+)*\\/)*[\\w\\-]+(\\.[\\w\\-]+)*\\/?(\\?([\\w\\-\\.,@?^=%&:\\/~\\+#]*)+)?^'},
'邮箱':{'EnglishName': 'Mail', 'regExpress': '\\w@\\w*\\.\\w'},
'生日':{'EnglishName': 'Birthday', 'regExpress': '^(18|19|20)\\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)$'},
'身份证号':{'EnglishName': 'IdentityNumber', 'regExpress': '^[1-9]\\d{5}(18|19|20)\\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\\d{3}[0-9Xx]$'},
'手机号':{'EnglishName': 'PhoneNumber', 'regExpress': '^1[34578]\\d{9}$'},
'邮编':{'EnglishName': 'PostCode', 'regExpress': '^[1-9][0-9]{5}$'},
'IP地址':{'EnglishName': 'IPAddress', 'regExpress': '^((2[0-4]\\d|25[0-5]|[01]?\\d\\d?)\\.){3}(2[0-4]\\d|25[0-5]|[01]?\\d\\d?)$'},
'话题':{'EnglishName': 'Topic', 'regExpress': '#.+#'},
'音乐':{'EnglishName': 'Music', 'regExpress': '.+(.MP3|.mp3|.WMA|.wva)$'}
}
#表包含的子表
publicSonTableList = {}
#表包含的子表对象
publicSonTableObjectList = {}

#保存文件
def upload_path_handler(modelName):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    return "upload/{modelName}_p/{time}".format(modelName = modelName,time=now_time)

#得到文件名
def getFileName(modelName,fileName):
    uploadPath = upload_path_handler(modelName)
    filePath = os.path.join(BASE_DIR,app_name,uploadPath)
    Path(filePath).mkdir(parents=True, exist_ok=True)
    filename = os.path.join(filePath,fileName).replace('\\','/') 
    return "{filePath}/{fileName}".format(filePath = uploadPath[7:],fileName = fileName)


def save_file_mutil(modelName,myfile):
    import random
    if myfile:
        uploadPath = upload_path_handler(modelName)
        filePath = os.path.join(BASE_DIR,app_name,uploadPath)
        Path(filePath).mkdir(parents=True, exist_ok=True)
        #文件名前加随机数避免重复
        hasMutiFile = False
        try:
            myfile.name
        except:
            hasMutiFile = True
        if hasMutiFile == False:
            return ""    
        files = myfile  
        fileNameList = []  
        for f in files: 
            newFileName = "{}_{}".format(random.randint(0, 1000),f.name)
            filename = os.path.join(filePath,newFileName).replace('\\','/')       #定义上传的文件名（绝对路径），UPLOADFILE为settings中定义的文件上传路径
            print(filename)
           
            if not f:                                                        
                HttpResponse('no files for upload') 
            dest = open(filename,'wb+')                                    #创建一个文件，使用二进制模式打开，并写入文件流
            try:
                for chunk in f.chunks():
                    dest.write(chunk)
            finally:
                dest.close()
        
            fileNameList.append("{filePath}/{fileName}".format(filePath = uploadPath[7:],fileName = newFileName))

        return ";".join(fileNameList)
    else:
        return ""

def save_file(modelName,myfile):
    hasMutiFile = False
    try:
        fileName = myfile.name
    except:
        hasMutiFile = True
    print(hasMutiFile)    
    if hasMutiFile:
            return save_file_mutil(modelName,myfile)
    else:
            return save_file_single(modelName,myfile)

def save_file_single(modelName,myfile):
    import random
    if myfile:
        uploadPath = upload_path_handler(modelName)
        filePath = os.path.join(BASE_DIR,app_name,uploadPath)
        Path(filePath).mkdir(parents=True, exist_ok=True)
        #文件名前加随机数避免重复
        newFileName = "{}_{}".format(random.randint(0, 1000),myfile.name)
        filename = os.path.join(filePath,newFileName).replace('\\','/')       #定义上传的文件名（绝对路径），UPLOADFILE为settings中定义的文件上传路径
        print(filename)
        
        if not myfile:                                                        
            HttpResponse('no files for upload') 
        dest = open(filename,'wb+')                                    #创建一个文件，使用二进制模式打开，并写入文件流
        try:
            for chunk in myfile.chunks():
                dest.write(chunk)
        finally:
            dest.close()
        
        return "{filePath}/{fileName}".format(filePath = uploadPath[7:],fileName = newFileName)
    else:
        return ""

def updatedPageInfo(entryObject,page,entryName = ""):
        updatedPageInfo = []
        print(page)
        for pageInfo in page:
            updatePage = updateHardCodeFieldValue(entryObject,pageInfo,entryName) 
            updatedPageInfo.append(updatePage)
        return updatedPageInfo  

def updateHardCodeFieldValue(entryObject,content,entryName = ""):
        newData = {}
        
        if entryName == "":
            entryName =  entryObject._meta.model_name
        for field in entryObject._meta.fields:             
            fieldName = field.name
            #字段含值为列表处理
            publicDataDictT = {}
            
            mixFieldName = "{}.{}".format(entryName,fieldName)
            checkNameList = [fieldName,mixFieldName]
            name = ""
            
            for name in checkNameList:
                if name in publicDataDict.keys():
                    publicDataDictT = publicDataDict[name]["keyValuePair"]
           
            if len(publicDataDictT) >0:
                content[fieldName] = publicDataDictT[content[fieldName]]#newData[fieldName] = publicDataDict[content[fieldName]]
            else:
                pass
            #外键查询
            fielTypeName = type(field).__name__
            
            if fielTypeName.lower() == "ForeignKey".lower(): #外键字段，检查有效性
                fieldValue = ""
                try:
                    fieldNameT = fieldName
                    foreignKeyModel = apps.get_model(app_name,fieldNameT.replace("Id","")) #去掉Id字样
                    try:
                            fieldValue = foreignKeyModel.objects.get(id=content[fieldName])
                    except:
                            fieldValue = foreignKeyModel.objects.get(id=content[fieldName+"_id"])    
                    
                    content[fieldName] = fieldValue
                    
                except:
                    pass
            
        return content       

    
def content_validity(content):
        if len(str(content)) > pageCountEveryPage:#字数自己设置
            return '{}……'.format(str(content)[0:40])#超出部分以省略号代替。
        else:
            return str(content)
                               
def getPageBar(urlName,page,query,pindex):
    pageStart = """
    <!-- 页码导航 开始 -->
    <nav aria-label="...">
					  <ul class="pagination justify-content-center"">
                      """
    pageInfo = ""
    if page.has_previous:
      try:
        previous_page_number = page.previous_page_number()
        pageInfo ="""
                <li class="page-item "><a class="page-link" href="{}?p={}&query={}" >
                    上一页</a></li>
                    """.format(urlName,previous_page_number,query)
      except:
        pass
        

    #
    startPage = page.number
    
    endPage = startPage + pageCountEveryPage
    if endPage > page.paginator.num_pages:
        endPage = page.paginator.num_pages
    if  endPage -  startPage < pageCountEveryPage:
            startPage = endPage - pageCountEveryPage
            if startPage < 0 :
                startPage = 1
    
    for num in page.paginator.page_range:
                
                if num < startPage:
                    continue               
                if num == page.number:
                   
                    pageInfo = pageInfo + """<li class="page-item active" aria-current="page">
						  <span class="page-link">{}</span>
						</li>
                        """.format(num)
                    
                else:
                    pageInfo = pageInfo + '<li class="page-item"><a class="page-link" href="{}?p={}&query={}">{}</a></li>\n'.format(urlName,num,query,num)
                if num >= endPage:
                    
                    break;
                
    if page.has_next:
            try:
                 pageInfo = pageInfo + """<li class="page-item"><a class="page-link" href="{}?p={}&query={}" >下一页
                      </a></li>
                      """.format(urlName,page.next_page_number(),query)
            except:
                pass
    pageEnd = """
					  </ul>
					</nav>
					<!--  页码导航 结束  -->
                    """
    txt = html.unescape("{}{}{}".format(pageStart,pageInfo,pageEnd)) #这样就得到了txt = '<abc>'   

    return txt

    def saveImgWX(request,savePath,imageName):
        print(request.method)
        if request.method == "POST":
            files = request.FILES
            '''
             需要通过小程序端的key（image）获取二进制数据
             获取文件内容
            '''
            content = files.get(imageName,None) 
            #fileObect = request.FILES.get(fieldName,None)            
            '''
            设置保存路径
                settings.IMAGES_DIR 已经默认设定
                默认保存文件名字为aaa.jpg
                    '''

                #文件上传
            fieldValue = save_file(savePath,content)  
            print(fieldValue)
            return Response({'status':0, "msg":"上传成功"})
    

from math import *

class  CollaborativeFilteringRecommendation():
    def __init__(self):  
        self.data = self.getRatingData()

    #得到字典来表示每位用户评论的图片和点击
    def getRatingData(self):
        data = {}

        tableName = "BrowsingHistory"
        ModelObject = apps.get_model(app_name,tableName)
        dataTemp = ModelObject.objects.values("MemberId","ImageInformationId").annotate(MemberIdCount=Count("ImageInformationId")).order_by("-MemberIdCount")

        #组装数据
        for item in dataTemp:
            if item["MemberId"] in data.keys():

                data[item["MemberId"]] = {**data[item["MemberId"]],**{item["ImageInformationId"]:int(item["MemberIdCount"])}}
            else:
                data[item["MemberId"]] = {item["ImageInformationId"]:int(item["MemberIdCount"])}
        print(data)
        return data
    # def getRatingData():
    #     pass
        
    #计算计算任何两位用户之间的相似度，由于每位用户评论的歌曲不完全一样，所以兽先要找到两位用户共同点击过的图片
    #   然后计算两者之间的欧式距离，最后算出两者之间的相似度

    def Euclidean(self,user1,user2):
        #取出两位用户评论过的歌曲和评分
        user1_data=self.data[user1]
        user2_data=self.data[user2]
        distance = 0
        #找到两位用户都评论过的电影，并计算欧式距离
        for key in user1_data.keys():
            if key in user2_data.keys():
                #注意，distance越大表示两者越相似
                distance += pow(float(user1_data[key])-float(user2_data[key]),2)
 
        return 1/(1+sqrt(distance))#这里返回值越小，相似度越大
 
    #计算某个用户与其他用户的相似度
    def top10_simliar(self,userID):
        res = []
        for userid in self.data.keys():
            #排除与自己计算相似度
            if not userid == userID:
                simliar = self.Euclidean(userID,userid)
                res.append((userid,simliar))
        print("userID:{}".format(userID))        
        print("before")        
        print(res)
        res.sort(key=lambda val:val[1])
        print("after") 
        print(res)
        return res[:10]
########################################################################
    #根据用户推荐图片给其他人
    def recommend(self,user):
        #相似度最高的用户
        try:
            top_sim_user = self.top10_simliar(user)[0][0]

            #相似度最高的用户的看图记录
            items = self.data[top_sim_user]
            recommendations = []
            #筛选出该用户未观看的图并添加到列表中
            for item in items.keys():
                if item not in self.data[user].keys():
                    recommendations.append((item,items[item]))
            recommendations.sort(key=lambda val:val[1],reverse=True)#按照点击量排序
            #返回评分最高的10张图片
            if len(recommendations)>10:
                return recommendations[:10]
            else:
                return recommendations
        except:
            return []

#########################################################################
    ##计算两用户之间的Pearson相关系数
    def pearson_sim(self,user1,user2):
        # 取出两位用户评论过的图片和点击
        user1_data = self.data[user1]
        user2_data = self.data[user2]
        distance = 0
        common = {}
     
        # 找到两位用户都评论过的图片
        for key in user1_data.keys():
            if key in user2_data.keys():
                common[key] = 1
        if len(common) == 0:
            return 0#如果没有共同评论过的图片，则返回0
        n = len(common)#共同图片数目
        print(n,common)
     
        ##计算评分和
        sum1 = sum([float(user1_data[item]) for item in common])
        sum2 = sum([float(user2_data[item]) for item in common])
     
        ##计算评分平方和
        sum1Sq = sum([pow(float(user1_data[item]),2) for item in common])
        sum2Sq = sum([pow(float(user2_data[item]),2) for item in common])
     
        ##计算乘积和
        PSum = sum([float(user1_data[it])*float(user2_data[it]) for it in common])
     
        ##计算相关系数
        num = PSum - (sum1*sum2/n)
        den = sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
        if den == 0:
            return 0
        r = num/den
        return r        