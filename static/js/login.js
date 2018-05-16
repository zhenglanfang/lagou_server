/**
 * Created by Administrator on 2017/8/27.
 */
$(function () {
    var name = false;
    var pwd = false;
    var verifycode = false;
    $('.name_input').focus();
    $('.name_input,.pwd_input').focus(function () {
        $(this).next().html('');
    });
    $('.verifycode_input').focus(function () {
        if($(this).prev().html()){
            $(this).prev().html('');
        }
    });

    $('.name_input').blur(function () {
        if($(this).val().trim()==''){
            name = false;
            $(this).next().html('用户名不能为空！');
            return;
        }
        var reg = /^1[34578]\d{9}$/; //手机号
        if(check_reg(reg,$(this).val())){
            name = true;
        }
        else {
            name = false;
            $(this).next().html('请输入正确的手机号格式！')
        }
    });

    $('.pwd_input').blur(function () {
        if($(this).val().trim()==''){
            pwd = false;
            $(this).next().html('密码不能为空！');
            return;
        }
        //密码是6到15位字母、数字、字符
        var reg = /^[@#$%^&*~\w]{5,16}$/;
        if(check_reg(reg,$(this).val())){
            pwd = true;
        }
        else {
            pwd = false;
            $(this).next().html('用户名或密码错误！')
        }
    });

    $('.verifycode_input').blur(function () {
        if($(this).val().trim()==''){
            verifycode = false;
            $(this).prev().html('验证码不能为空！');
            return;
        }
        if(/^\w{4}$/.test($(this).val())){
            verifycode = true;
        }
        else{
            verifycode = false;
            $(this).prev().html('验证码错误！');
        }

    });

    $('.form').submit(function () {
        // alert('name='+name+',pwd='+pwd);
        $('.name_input').blur();
        $('.pwd_input').blur();
        $('.verifycode_input').blur();
        if(name == true && pwd == true && verifycode == true){
            // alert('逻辑判断');
            return true;
        }
        else {
            return false;
        }
    });
});


