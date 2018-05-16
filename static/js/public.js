
//正则检验
function check_reg(reg,str) {
    return reg.test(str)
}

//去除前后空格,默认有trim方法
String.prototype.trim = function () {
    return this.replace(/(^\s*)|(\s*$)/g,'')
};

//去除左边空格
String.prototype.ltrim = function () {
    return this.replace(/^\s*/g,'')
};

//去除右边空格
String.prototype.rtrim = function () {
    return this.replace(/\s*$/g,'')
};

//搜索框事件
$(function () {
    $('.search_con form').submit(function () {
        var keywd = $(this).find('.input_search').val();
        if (keywd.trim() == ''){
            return false
        }
        else
            return true
    })
});

//获取XMLHttpRequest 对象
function xmlhttpRequest(){
    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    }
    else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xmlhttp
}

//ajax封装函数，xmlhttp:XMLHttpRequest 对象,func：处理响应的函数，url：请求的地址，method：请求方式，param：请求参数
/*function myajax(xmlhttp,func,url,method="GET",param="") {
    xmlhttp.onreadystatechange = func;
    xmlhttp.open(method,url,true);
    if (method == "POST"){
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    }
    xmlhttp.send(param);
}*/

//关闭窗口
function custom_close(){
    if (confirm("您确定要关闭本页吗？")) {
        $.get("/logout/",function () {
            window.open("","_parent","");
            window.opener = window;
            window.close();
        });
    }
    else {
        return false;
    }
}





