
//排序开始
;(function(){
var tbody = document.querySelector('#tableSort').tBodies[0];
var th = document.querySelector('#tableSort').tHead.rows[0].cells;
var td = tbody.rows;
for(var i = 0;i < th.length;i++){
  th[i].flag = 1;
  th[i].onclick = function(){
    sort(this.getAttribute('data-type'),this.flag,this.cellIndex);
    this.flag = -this.flag;
  };
};
function sort(str,flag,n){
  var arr = [];//存放DOM
  for(var i = 0;i < td.length;i++){
    arr.push(td[i]);
  };
  arr.sort(function(a,b){//排序
    return method(str,a.cells[n].innerHTML,b.cells[n].innerHTML) * flag;
  });
  for(var i = 0;i < arr.length;i++){//添加
    tbody.appendChild(arr[i]);
  };
};
function method(str,a,b){//排序方法
  switch(str){
  case 'num': 
    return a-b;
    break;
  default://字符串
    return a.localeCompare(b);
  };
};
})();

//排序结束


  
