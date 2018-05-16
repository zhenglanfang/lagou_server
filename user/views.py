import hashlib
import random
import uuid
from io import BytesIO

from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse
from PIL import Image,ImageDraw,ImageFont
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta,datetime

from user import models
from user import user_decorator
from service.util import send_email
from lagou_server import settings


#登录
def login(request):
    context = {}
    # 是否记住密码
    username = request.session.get('rem_username','')
    userpwd = request.session.get('rem_userpwd','')
    if username and userpwd:
        context['username'] = username
        context['userpwd'] = userpwd
    else:
        #获取cookie:userid
        uid = request.COOKIES.get('userid')
        query = models.User.objects.filter(pk=uid)
        if query.exists():
            # upwd = query[0].upwd
            context['username'] = query[0].user_name

    #判断是否提交
    if not request.POST:
        return render(request, 'user/login.html',context)
    #登录逻辑处理
    return login_handle(request)

#登录逻辑处理
def login_handle(request):
    context = {}
    agrs = request.POST
    username = agrs.get('username','').strip()
    userpwd = agrs.get('userpwd','').strip()
    rempwd = agrs.get('rempwd', None)
    #加密
    newpwd = hashlib.sha1(userpwd.encode('utf-8')).hexdigest()
    cekcode = agrs.get('verifycode').strip()
    context['username'] = username
    context['userpwd'] = userpwd
    if cekcode.upper() != request.session.get('verifycode'):
        context['err'] = '验证码错误！'
        return render(request, 'user/login.html', context)
    query = models.User.objects.filter(user_name=username, user_pwd=newpwd)
    # 登录成功
    if query.exists():
        # 未激活
        if query[0].user_code:
            context['err'] = '您还没有激活，请查看您的邮箱。'
            return render(request, 'user/login.html', context)

        userid = query[0].pk
        request.session['userid'] = userid
        request.session['username'] = username
        # request.session.set_expiry(0)
        if request.COOKIES.get('url'):
            response = HttpResponseRedirect(request.COOKIES.get('url'))
            response.delete_cookie('url')
        else:
            response = HttpResponseRedirect(reverse('index'))
        # 记住密码
        if rempwd:
            request.session['rem_username'] = username
            request.session['rem_userpwd'] = userpwd
        # 记住用户名
        response.set_cookie('userid', userid, expires=datetime.now() + timedelta(days=7))
        return response
    # 登录失败
    context['err'] = '用户名或密码错误！'
    context['userpwd'] = ''
    return render(request, 'user/login.html', context)

#退出
def logout(request):
    if request.session.get('userid') and request.session.get('username'):
        del request.session['userid']
        del request.session['username']
    return redirect(reverse('user:login'))
    # return HttpResponse('<script type="text/javascript">window.open("","_parent","");window.opener = window;window.close();</script>')

#注册
def register(request):
    agrs = request.POST
    if not agrs:
        return render(request, 'user/register.html')

    #注册逻辑处理
    username = agrs['username'].strip()
    userpwd = agrs['userpwd'].strip()
    email = agrs['email'].strip()
    context = {}
    update = False
    query = models.User.objects.filter(user_name=username)
    if query.exists():
        if query[0].user_code:
            update = True
        else:
            context['err'] = '手机号已被注册！'
            return render(request, 'user/register.html',context)
    user_code = uuid.uuid4()
    user_code_url = request.get_host() + reverse('user:activate') + '?code=%s' % user_code
    send_email_result = send_email.send_obj.send_email_html(
        [(username,email)],
        msg='您的激活码是<a href="http://%s">%s</a>' % (user_code_url,user_code_url),
        subject_test='激活码'
    )
    # print(send_email_result)
    if send_email_result:
        print(send_email_result)
        context['err'] = '发送邮件失败：%s'% send_email_result
        return render(request, 'user/register.html', context)

    # 添加用户
    userpwd = hashlib.sha1(userpwd.encode('utf-8')).hexdigest()
    if update:
        user = query[0]
        user.user_pwd = userpwd
        user.user_code = user_code
        user.user_email = email
        user.user_key = str(uuid.uuid4())
        user.save()
    else:
        models.User.objects.create(user_name=username,user_pwd=userpwd,
                               user_email=email,user_code=user_code,
                               user_key=str(uuid.uuid4()))

    # 注册成功返回登录页面
    response = HttpResponseRedirect(reverse('user:login'))
    result = models.User.objects.filter(user_name=username)
    userid = result[0].pk
    response.set_cookie('ok','ok')
    response.set_cookie('userid', userid,expires=datetime.now()+timedelta(days=7))
    # 删除cookie
    # response.delete_cookie('uname')
    return response


def activate(request):
    """激活"""
    code = request.GET.get('code')
    query = models.User.objects.filter(user_code=code)
    if code and query:
        print(query[0])
        query[0].user_code = None
        query[0].save()
        login_url = request.get_host() + reverse('user:login')
        response_html = '您已经激活成功，现在可以去<a href="http://%s">登录</a>啦' % login_url
    else:
        register_url = settings.ip + reverse('user:register')
        response_html = '您的激活码已失效，请重新<a href="http://%s">注册</a>' % register_url
    return HttpResponse(response_html)


#验证码
def verifycode(request):
    bgcolor = (random.randrange(20,101),random.randrange(20,101),random.randrange(101,255))
    height = 35
    width = height*4
    im = Image.new('RGB',(width,height),bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(200):
        xy = (random.randrange(0,width),random.randrange(0,height))
        draw.point(xy,fill=random_color())

    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    checkcode = ''

    for i in range(0,4):
        checkcode += str1[random.randint(0,len(str1)-1)]

    font = ImageFont.truetype('arial.ttf',18)
    # font = ImageFont.load_default().font

    for i in range(0,4):
        draw.text((height*i+7,5),checkcode[i],font=font,fill=random_color())

    del draw
    request.session['verifycode'] = checkcode
    buf = BytesIO()
    im.save(buf,'png')
    return HttpResponse(buf.getvalue(),'image/png')

#判断用户名是否存在
@csrf_exempt
def check_name(request):
    name = request.POST.get('name','').strip()
    if name:
        name = name.strip()
        query = models.User.objects.filter(user_name=name,user_code=None)
        if query.exists():
            return HttpResponse('error')
    return HttpResponse('ok')

#随机颜色
def random_color():
    return (255,random.randrange(0,255),random.randrange(0,255))








