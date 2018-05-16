from django.conf.urls import url
from search import views

urlpatterns = [
    url(r'^job/(\d+)/$', views.job_handle, name='job'),
    url(r'^city/$', views.get_city, name='city'),
    url(r'^company/(.+)/(\d+)$', views.company_handle, name='company'),
    url(r'^detail/([a-zA-Z0-9-]+)/$', views.detail_handle, name='detail'),
]
