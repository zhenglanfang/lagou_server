from django.conf.urls import url
from data_service import views

urlpatterns = [
    url(r'^$', views.data_index, name='index'),
    url(r'^job/$', views.api_job, name='api_job'),
    url(r'^company/(.+)/$', views.api_company, name='api_company'),
    url(r'^download/$', views.download_positions, name='download_position'),
    url(r'^company_static/$', views.api_company_static, name='api_company_static'),
    url(r'^download_static/(.+)$', views.download_static, name='download_static'),
    url(r'^get_companies/$', views.get_companies, name='get_companies'),
]
