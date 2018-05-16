from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


# 如果没有登录跳转到登录页面
def login(func):
    def login_check(request, *args, **kwargs):
        username = request.session.get('username')
        if username:
            return func(request, *args, **kwargs)
        red = HttpResponseRedirect(reverse('user:login'))
        # 记住访问的页面
        red.set_cookie('url', request.get_full_path())
        return red
    return login_check
