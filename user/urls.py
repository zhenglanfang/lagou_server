from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^check_name', views.check_name, name='check_name'),
    url(r'^verifycode/$', views.verifycode, name='verifycode'),
    url(r'^activate/$', views.activate, name='activate'),
]