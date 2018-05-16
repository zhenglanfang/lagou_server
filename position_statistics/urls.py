from django.conf.urls import url
from position_statistics import views

urlpatterns = [
    url(r'^$', views.statistics_index, name='index'),
    url(r'^positions_rank/$', views.positions_rank, name='positions_rank'),
    url(r'^position_type_distribute/$', views.position_type_distribute, name='position_type_distribute'),
    url(r'^city_distribute/$', views.city_distribute, name='city_distribute'),
    url(r'^position_city_distribute/$', views.position_city_distribute, name='position_city_distribute'),
    url(r'^education_distribute/$', views.education_distribute, name='education_distribute'),
    url(r'^second_type_salary/$', views.second_type_salary, name='second_type_salary'),
    url(r'^first_type_salary/$', views.first_type_salary, name='first_type_salary'),
    url(r'^city_salary/$', views.city_salary, name='city_salary'),
    url(r'^education_salary/$', views.education_salary, name='education_salary'),
    url(r'^work_year_salary/$', views.work_year_salary, name='work_year_salary'),
]
