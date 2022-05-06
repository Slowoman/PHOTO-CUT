/**
 * 弹出式提示框，默认1.2秒自动消失
 * @param message 提示信息
 * @param style 提示样式，有alert-success、alert-danger、alert-warning、alert-info
 * @param time 消失时间
 */
var prompt = function (message, style, time)
{
    style = (style === undefined) ? 'alert-success' : style;
    time = (time === undefined) ? 1200 : time;
    $('<div>')
        .appendTo('body')
        .addClass('alert ' + style)
        .html(message)
        .show()
        .delay(time)
        .fadeOut();
};

// 成功提示
var success_prompt = function(message, time)
{
    prompt(message, 'alert-success', time);
};

// 失败提示
var fail_prompt = function(message, time)
{
    prompt(message, 'alert-danger', time);
};

// 提醒
var warning_prompt = function(message, time)
{
    prompt(message, 'alert-warning', time);
};

// 信息提示
var info_prompt = function(message, time)
{
    prompt(message, 'alert-info', time);
};
//字段合格性检查正则

var regDict = {
'Time':/(\d{4}-\d{2}-\d{2})\s(\d{2}:\d{2}:\d{2})/,
'Password':/[0-9A-Za-z]{6,16}$/,
'Picture':/.+(.jpg|.JPEG|.PNG|.GIF)$/,
'Video':/.+(.flv|.rvmb|.mp4|.avi|.wmv)$/,
'Number':/^\d+(.\d+)?$/,
'URLAddress':/^(http|ftp|https):\/\/([\w\-]+(\.[\w\-]+)*\/)*[\w\-]+(\.[\w\-]+)*\/?(\?([\w\-\.,@?^=%&:\/~\+#]*)+)?^/,
'Mail':/\w@\w*\.\w/,
'Birthday':/^(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)$/,
'IdentityNumber':/^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/,
'PhoneNumber':/^1[34578]\d{9}$/,
'PostCode':/^[1-9][0-9]{5}$/,
'IPAddress':/^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$/,
'Topic':/#.+#/,
'Music':/.+(.MP3|.mp3|.WMA|.wva)$/
};  
//保存输入  
function saveCurData(postUrl) {
	
	var editReg = /.+save_edit\/$/
	console.log(postUrl)
	var isEdit = editReg.test(postUrl)
	console.log(postUrl)
	console.log(isEdit)
	var errorMessage = checkInput(isEdit)
	if (errorMessage != "") {
		$("#errorMessage").html(errorMessage);
		return false;
	}
	
	if (errorMessage == "") 
	{		
		$("#errorMessage").html("");
		//处理文件字段
		var formData = new FormData();
		var csrf_data = $('[name=csrfmiddlewaretoken]').val();
		
		if (isEdit)
		{			
			objectId = $('[name=curObject_id]').val();
			formData.append("curObject_id", objectId);
		}
			
		$.each(checkObjectList, function(index,value) { // 这里的函数参数是键值对的形式，k代表键名，v代表值
			var curObject = $("#" + value.fieldName)
			
			if (curObject.prop('type')  == "file") {
			//if (value.regName == "图片" || value.regName == "视频" || value.regName == "音乐") {
				//多文件上传
				var files = document.getElementById(value.fieldName).files
				var fileLen = files.length
				console.log(fileLen)
				
				for (var i=0;i<fileLen;i++)
				{
				
					var fileObj = files[i];
				
					formData.append(value.fieldName, fileObj);
				}
				
			}
			else {
				var curObject = $("#" + value.fieldName)
				var curObjectVal = curObject.val() 
				if (curObject.prop('type') == "checkbox" && curObject .is(':checked') == false)
				{
						curObjectVal = 0
				}
				formData.append(value.fieldName, curObjectVal ); // $('#subject').val()
				
			}
		});
		formData.append('csrfmiddlewaretoken',csrf_data);
		
		$.ajax({　　　　　　　
            url:postUrl,
            type:'POST',		
            data:formData,
			contentType:false,
			processData:false,

            success:function(data){
				console.log(data);
				if (data.message.flag == 0){
						$('<div>').appendTo('body').addClass('alert alert-success').html('操作成功').show().delay(3000).fadeOut();
						$(location).attr('href', data.returnPage);
					}
			    else {
						$("#errorMessage").html(data.message.errorMessage);
					}
            },
            error:function(){
                $('<div>').appendTo('body').addClass('alert alert-danger').html('操作失败').show().delay(3000).fadeOut();
			},
            statusCode:{
				404:function(){
                alert("目标没有找到，请重试");
				},
				500:function(){
                alert("服务器发生错误，请稍候");
				},
			}
    });
    return false;
		
	}
}


//保存输入  
function saveCurDataManyTable(postUrl) {
	
	var editReg = /.+save_edit\/$/
	var isEdit = editReg.test(postUrl)
	var errorMessage = checkInput(isEdit)
	console.log(errorMessage)
	
	if (errorMessage != "") {
		$("#errorMessage").html(errorMessage);
		return false;
	}
	errorMessage = "";
	var curObject = null;
	if (errorMessage == "") 
	{		
		$("#errorMessage").html("");
		//处理文件字段
		var formData = new FormData();
		var csrf_data = $('[name=csrfmiddlewaretoken]').val();
		
		if (isEdit)
		{			
			objectId = $('[name=curObject_id]').val();
			formData.append("curObject_id", objectId);
		}
			
		$.each(checkObjectList, function(index,value) { // 这里的函数参数是键值对的形式，k代表键名，v代表值
			var currentObjectList = document.getElementsByName(value.fieldName)//$("""[id=" + value.fieldName +"]""")

			for (var i=0;i<currentObjectList.length;i++)
			//for (var curObject in currentObjectList)
			{
				curObject = currentObjectList[i]

				var curObjectVal = curObject.value
				var curObjectId = curObject.id
				if (curObject.type == "checkbox" && curObject.checked == false)
				{
						curObjectVal = 0
				}
				console.log(curObjectId)
				console.log(curObject.type)
				console.log(value.regName)
				if (!curObject.type){ continue;}
				if (curObject.type == "file") {
				//if (value.regName == "图片" || value.regName == "视频" || value.regName == "音乐") {
					var fileObj = document.getElementById(curObjectId).files[0];
					console.log(fileObj)
					formData.append(curObjectId, fileObj);
					
				}
				else {
					formData.append(curObjectId, curObjectVal); // $('#subject').val()
					
				}
			}
		});
		formData.append('csrfmiddlewaretoken',csrf_data);
		console.log(formData)
		$.ajax({　　　　　　　
            url:postUrl,
            type:'POST',		
            data:formData,
			contentType:false,
			processData:false,

            success:function(data){
				console.log(data);
				if (data.message.flag == 0){
						$('<div>').appendTo('body').addClass('alert alert-success').html('操作成功').show().delay(30000).fadeOut();
						$(location).attr('href', data.returnPage);
					}
			    else {
						$("#errorMessage").html(data.message.errorMessage);
					}
            },
            error:function(){
                $('<div>').appendTo('body').addClass('alert alert-danger').html('操作失败').show().delay(3000).fadeOut();
			},
            statusCode:{
				404:function(){
                alert("目标没有找到，请重试");
				},
				500:function(){
                alert("服务器发生错误，请稍候");
				},
			}
    });
    return false;
		
	}
}
//页面字段对象
function CheckInfo(fieldName,fieldChieseName, checkReg,maxlength,isNull,regName){
			this.fieldName = fieldName			
            this.fieldChieseName = fieldChieseName
            this.checkReg = checkReg
			this.maxlength = maxlength
			this.isNull = isNull
			this.regName = regName
}
//字段内容检查
function checkInput(isEdit)
{
	var errorMessage = ""
	var curObject = null
	try {
	$.each(checkObjectList, function(index,value) {  // 这里的函数参数是键值对的形式，k代表键名，v代表值

		var currentObjectList = document.getElementsByName(value.fieldName)//$("""[id=" + value.fieldName +"]""")

		for (var i=0;i<currentObjectList.length;i++)
		//for (var curObject in currentObjectList)
		{
			//var curObjectVal = $("#" + value.fieldName).val()
			curObject = currentObjectList[i]

			var curObjectVal = curObject.value

			var imgEdit = isEdit && value.regName == "图片" && curObjectVal == "";
			console.log(value.fieldChieseName)
			console.log(isEdit)
			console.log(value.regName)
			console.log(curObjectVal)
			if (curObjectVal == "None"){
				curObjectVal = ''
			}
			if (errorMessage == ""  && value.isNull == false && curObjectVal.length == 0 && imgEdit == false && value.checkReg != "" ) { //不能为空
				errorMessage = value.fieldChieseName + "不能为空，请输入...";
			}
			
			else if (errorMessage == ""  && value.checkReg != "" && curObjectVal.length != 0) { //格式检查
				//console.log(value.checkReg);
				//修改时，图片链接可以为空
				console.log(regDict[value.checkReg].test(curObjectVal))
				if (imgEdit == false && regDict[value.checkReg].test(curObjectVal) == false) {
					errorMessage = value.fieldChieseName + "【" + curObjectVal + "】格式不对，应为【" + value.regName + "】,请检查...";
				}			
			}		
		
			if (errorMessage != "")
			{
				//检查当前字段是否有前缀
				var preName = value.fieldName.match(/(.*)\./ );  	
				if (preName.length >0)//有前缀
				{
					var cuenrPreObject = document.getElementById(preName[1] + "-tab");
					cuenrPreObject.click();
				}

				curObject.focus();
				throw false;
				
			}
		}
	 });
	}
	catch(e)
	{
		
	}

	return errorMessage		
}
//批量删除
function deleteBatch(deleteallLink) {
    var valArr=[];
    var ones=document.getElementsByName('item');
    for (var i=0;i<ones.length;i++){
        if (ones[i].checked==true){
            valArr.push(ones[i].value)
        }
    }
    if (valArr.length!=0){
		
		var formData = new FormData();
		var csrf_data = $('[name=csrfmiddlewaretoken]').val();
		formData.append('csrfmiddlewaretoken',csrf_data);
		formData.append('vals',valArr);
        $.ajax({　　　　　　　//#地址一定要正确
            url: deleteallLink,　　　　　　//#全部大写
            type:'POST',
			data:formData,
			contentType:false,
			processData:false,
            success:function(data){
               if (data.message.flag == 0){
						$('<div>').appendTo('body').addClass('alert alert-success').html('操作成功').show().delay(5000).fadeOut();
					}
			    else {
						$('<div>').appendTo('body').addClass('alert alert-success').html('操作部分成功').show().delay(5000).fadeOut();
						
					}
				$(location).attr('href', data.returnPage);
				window.location.reload() //刷新当前页面.
            },
            error:function(){
                $('<div>').appendTo('body').addClass('alert alert-danger').html('操作失败').show().delay(3000).fadeOut();
			},
            statusCode:{
				404:function(){
                alert("目标没有找到，请重试");
				},
				500:function(){
                alert("服务器发生错误，请稍候");
				},
			}
        });
    }
    else {
        var error_m="请选择数据";
        alert(error_m);
    }
}
//导入excel文件  
function excelFileUpload(postUrl) {
	var errorMessage = ""
    var file_info = $('#uploadExcelFile')[0].files[0];
    console.log(file_info)
    var curObjectVal = $('#uploadExcelFile').val()

    if(file_info ==='' || file_info == undefined ){
    		errorMessage = '你没有选择任何文件'
    }
    if (errorMessage == "" && /\w+(.xlsx|.xls)$/.test(curObjectVal) == false) {	
		errorMessage = '文件格式不对，应为.xlsx|.xls'
	}
	if (errorMessage != "") {
		$('<div>').appendTo('body').addClass('alert alert-success').html(errorMessage).show().delay(3000).fadeOut();
		
		return false;
	}
	
	if (errorMessage == "") 
	{		
		
		//处理文件字段
		var formData = new FormData();
		//var csrf_data = $('[name=csrfmiddlewaretoken]').val();
		
        formData.append('uploadExcelFile',file_info);

		//formData.append('csrfmiddlewaretoken',csrf_data);
		
		$.ajax({　　　　　　　
            url:postUrl,
            type:'POST',		
            data:formData,
			contentType:false,
			processData:false,

            success:function(data){
				console.log(data);
				if (data.flag == 0){
						$('<div>').appendTo('body').addClass('alert alert-success').html('操作成功').show().delay(30000).fadeOut();
						$(location).attr('href', data.returnPage);
					}
			    else {
						
						alert(data.message);
					}
            },
            error:function(){
                $('<div>').appendTo('body').addClass('alert alert-danger').html('操作失败').show().delay(3000).fadeOut();
			},
            statusCode:{
				404:function(){
                alert("目标没有找到，请重试");
				},
				500:function(){
                alert("服务器发生错误，请稍候");
				},
			}
    });
    return false;
		
	}
}

//生成文件并下载文件
 
function excelFileExport(postUrl,downloadUrl){
	var formData = $('#searchForm').serialize();

    $.ajax({
        type:"GET",
        data: formData,
        url: postUrl, //后台处理函数的url
        dataType: "json",
        success: function(arg){
                console.log('后台反应会的数据');
                console.log(arg.data);
                 if (arg.code===0){ 
                     window.location.href=downloadUrl+arg.data+'';
                }else{
                    alert(arg.data)
                }
 
        },
        error: function(){
            alert("false");
        }
    });
    return false;

}
//得到二维数组的排列组合
function getArrayByArrays(arrays)
  {
    var arr = [""];
    for(var i = 0;i<arrays.length;i++)
    {
      arr = getValuesByArray(arr,arrays[i]);
    }
    return arr;
  }
  function getValuesByArray(arr1,arr2)
  {
    var arr = [];
    for(var i=0;i<arr1.length;i++)
    {
      var v1 = arr1[i];
      for(var j=0;j<arr2.length;j++)
      {
        var v2 = arr2[j];
        var value = v1+"_"+v2;
        arr.push(value);
      };
    };
    return arr;
  }

//一个数字数组，如果数字位数效2，则以0补齐
function getNumberString(numbers){
        var itemNumStr = ""
        for (var k =0;k<numbers.length;k++)
        {
            if (numbers[k] != "")
            {
              
                if (numbers[k].length<2)
                {
                    itemNumStr =  itemNumStr + "0" + numbers[k]
                }
                else
                {
                    itemNumStr += idList[k]
                }
            }
        }
        return itemNumStr
}