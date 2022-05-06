function checkAll() {
    var all = document.getElementById("checkAll");

    if (all.checked == true) {
        var ones = document.getElementsByName("item");
        for (var i = 0; i <= ones.length; i++) {
            ones[i].checked = true;
        }
    } else {
        var ones = document.getElementsByName("item");
        for (var i = 0; i <= ones.length; i++) {
            ones[i].checked = false;
        }
    }
}

function checkOne() {
    var one=document.getElementsByName("item");
    one.checked=true;
}
