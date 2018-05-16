/**
 * Created by Administrator on 2017/8/27.
 */
$(function () {
    var name = false;
    var pwd = false;
    var ackpwd = false;
    var email = false;
    $('#username').focus();
    $('#username,#userpwd,#ackpwd,#email').focus(function () {
        $(this).next().html('');
    });
    $('#username').blur(function () {
        if($(this).val().trim()==''){
            name = false;
            $(this).next().html('用户名不能为空！');
            return;
        }
        var reg = /^1[34578]\d{9}$/; //手机号
        if(check_reg(reg,$(this).val())){
            //发送异步请求，判断用户名是否存在
            /*var xmlhttp;
            xmlhttp = xmlhttpRequest();
            myajax(xmlhttp,function () {
                if (xmlhttp.readyState==4 && xmlhttp.status==200){
                    document.getElementById('check_name').innerText = xmlhttp.responseText;
                    if (xmlhttp.responseText == 'ok'){
                        name = true;
                    }
                    else {
                        name = false;
                    }
                }
            },'/check_name?name='+$(this).val()+'&t='+Math.random());*/
            //var url = "{% url 'user:check_name' %}";
            $.post('/user/check_name',{'name':$(this).val(),'t':Math.random()},function (data) {
                if(data == 'ok'){
                    name = true;
                }
                else {
                    name = false;
                    document.getElementById('check_name').innerText = '用户名已经存在！';
                }
            });
        }
        else {
            name = false;
            $(this).next().html('手机号格式错误！')
        }
    });
    $('#userpwd').blur(function () {
        if($(this).val().trim()==''){
            $(this).val('');
            pwd = false;
            $(this).next().html('密码不能为空！');
            return;
        }
        //密码是6到15位字母、数字、字符
        var reg = /^[@#$%^&*~\w]{6,15}$/;
        if(check_reg(reg,$(this).val())){
            pwd = true;
        }
        else {
            pwd = false;
            $(this).next().html('密码是6到15位字母、数字、字符！')
        }
    });
    $('#ackpwd').blur(function () {
        if($(this).val().trim()==$('#userpwd').val()){
            ackpwd = true;
        }
        else {
            ackpwd = false;
            $(this).next().html('两次输入的密码不一致！');
        }
    });
     $('#email').blur(function () {
        if($(this).val().trim()==''){
            email = false;
            $(this).next().html('邮箱不能为空！');
            return;
        }
        //邮箱
        var reg = /^(\w)+(\.\w+)*@(\w)+((\.\w{2,3}){1,3})$/;
        if(check_reg(reg,$(this).val())){
            email = true;
        }
        else {
            email = false;
            $(this).next().html('邮箱格式错误！')
        }
    });
    $('#register').click(function () {
        $('#userpwd').blur();
        $('#ackpwd').blur();
        $('#email').blur();
        if(name == true && pwd == true && ackpwd== true && email == true)
		{
            // alert('');
			return true;
		}
		else
		{
            // console.log(name,pawd,ackpwd,email)
			return false;
		}
    })
});


