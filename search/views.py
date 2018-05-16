import json

from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from service import search


def index(request):
    return HttpResponseRedirect(reverse('search:job', args=[1]))


def job_handle(request, now_page):
    """搜索"""
    request_params = request.get_full_path().split('?')
    if len(request_params) > 1:
        request_params = request_params[1]
    else:
        request_params = ''
    key_word = request.GET.get('key_word')
    city = request.GET.getlist('city')
    work_year = request.GET.getlist('work_year')
    education = request.GET.getlist('education')
    job_nature = request.GET.getlist('job_nature')
    salary = request.GET.get('salary')
    sort = request.GET.get('sort') # 0:默认，1：按发布时间排序
    positions = search.SearchLogic.search_position(key_word=key_word, city=city, work_year=work_year,
                                                   education=education, job_nature=job_nature,
                                                   salary=salary, sort=sort)
    context = search.SearchLogic.page(positions, page_now=now_page, page_size=10)
    context['request_params'] = request_params
    context['request_get'] = json.dumps(dict(request.GET), ensure_ascii=False)
    context['page_url'] = 'search:job'
    print(context['request_get'])
    return render(request, 'positions_list.html', context=context)


def company_handle(request, company_name, now_page):
    """查找某公司的招聘信息"""
    request_params = request.get_full_path().split('?')
    if len(request_params) > 1:
        request_params = request_params[1]
    else:
        request_params = ''
    positions = search.SearchLogic.search_company(company_name)
    context = search.SearchLogic.page(positions, page_now=now_page, page_size=10)
    context['request_params'] = request_params
    context['request_get'] = json.dumps(dict(request.GET), ensure_ascii=False)
    context['company_name'] = company_name
    context['page_url'] = 'search:company'
    return render(request, 'company_positions.html', context=context)


def detail_handle(request, position_id):
    """单个职位的详细信息"""
    position = search.SearchLogic.search_one_position(position_id)
    if position:
        position = position[0]
    return render(request, 'position_detail.html', {'position': position})


def get_city(request):
    """获取所有城市"""
    citys = search.SearchLogic.get_city()
    return HttpResponse(json.dumps(citys))



