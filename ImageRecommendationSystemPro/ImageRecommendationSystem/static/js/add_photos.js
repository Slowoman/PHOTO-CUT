function inputUrl(id){ //点击div触发点击input事件
	$(id).click();
};

function fileUrl(self){ //当有图片输入时
    var read = new FileReader();
    img = document.getElementById(""+self.id).files[0];
    read.readAsDataURL(img);
    num = self.id[self.id.length-1];
    reads.onload = function(e){
    	$(".p-"+num+">img").attr("src",this.result);
    }
    $(".p-"+num+">img").css({"display":"block"});
    $(".p-"+num).siblings("button").css("display","block");
    var photoSize = $(".one-photo").length;
    num = parseInt(num);
    if (num>=photoSize && photoSize<=4) //最多支持添加五张图片
    	addNew(num+1);
}

function addNew(num){ //新增加一个输入框
	var boxDiv = $('<div class="one-photo"></div>');
	var imgDiv = $('<div class="add-now p-'+num+'" οnclick="inputUrl(\'#photo-'+num+'\')"></div>');
	var img = $('<img src = "" style="display: none; width:200px;">');
	var input = $('<input type="file" name="photo"  accept=".jpg,.jpeg,.png" style="display: none;" οnchange="fileUrl(this);" id="photo-'+num+'">');
	var delButton = $('<button οnclick="removeImge(\''+num+'\')" style="display:none;">删除</button>')
	imgDiv.append(img);
	boxDiv.append(imgDiv);
	boxDiv.append(input);
	boxDiv.append(delButton);
	$("#add-photos").append(boxDiv);

	
}

function removeImge(num){ 
	var photos = $(".one-photo");
	var photosLength = photos.length;
	photos[num-1].remove(); //删除当前图片框div
	for(var i=num;i<photosLength;++i){ //修改后面图片内容
		photos.eq(i).find("div.add-now").attr("class","add-now p-"+i);
		photos.eq(i).find("div.add-now").attr("onclick","inputUrl('#photo-"+i+"')");
		photos.eq(i).find("input").attr("id","photo-"+i);
		photos.eq(i).find("button").attr("onclick","removeImge(\""+i+"\")");
	}
}
