from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from django.views.decorators.cache import cache_page

from service.data_api import DataApi
from user import user_decorator
from user.models import User


@user_decorator.login
def data_index(request):
    context = {'key': get_user_key(request)}
    return render(request, 'data/date_api_all_positions.html', context)


@user_decorator.login
def api_company_static(request):
    context = {'key': get_user_key(request)}
    return render(request, 'data/date_api_company_positions.html', context)


def api_job(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    key = request.GET.get('key')
    # 用于下载数据前的展示
    flag = request.GET.get('show')
    # 判断key是否存在
    if not User.objects.filter(user_key=key).exists():
        context = {'status': 'error', 'data': 'Key error'}
        return JsonResponse(context)
    positions = []
    try:
        positions = DataApi.job_api(start_date=start_date, end_date=end_date)
    except Exception as e:
        context = {'status': 'error', 'data': str(e)}
    else:
        context = {'status': 'success', 'data': positions}
    if flag:
        context['data'] = positions[0:30]
        context['length'] = len(positions)
        return render(request, 'data/positions_table_include.html', context)
    return JsonResponse(context)


def api_company(request, company_name):
    # 用于下载数据前的展示
    flag = request.GET.get('show')
    key = request.GET.get('key')
    # 判断key是否存在
    if not User.objects.filter(user_key=key).exists():
        context = {'status': 'error', 'data': 'Key error'}
        return JsonResponse(context)
    positions = []
    try:
        positions = DataApi.company_api(company_name=company_name)
    except Exception as e:
        context = {'status': 'error', 'data': str(e)}
    else:
        context = {'status': 'success', 'data': positions}
    if flag:
        context['data'] = positions[0:30]
        context['length'] = len(positions)
        return render(request, 'data/positions_table_include.html', context)
    return JsonResponse(context)


@user_decorator.login
def download_positions(request):
    file_type = request.POST.get('file_type')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    company_name = request.POST.get('company_name')
    if company_name:
        file_name = '%s--职位' % company_name
        positions = DataApi.company_api(company_name=company_name)
    else:
        file_name = '%s--%s的职位' % (start_date, end_date)
        positions = DataApi.job_api(start_date, end_date)

    # out_file_path = path.sep.join((path.expanduser("~"), "Desktop", '百度.json'))
    # positions = DataApi.company_api(company_name='百度')

    file_name = '%s.%s' % (file_name, file_type)

    result = DataApi.download(file_type, positions)

    response = HttpResponse(result)
    if file_type == 'json':
        response['Content-Type'] = 'application/json'
    else:
        response['Content-Type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(file_name))
    return response


@user_decorator.login
def download_static(request, down_api):
    context = {}
    if down_api in ['all_positions', 'company_positions']:
        context[down_api] = down_api
    else:
        return HttpResponseRedirect(reverse('api:index'))
    context['key'] = get_user_key(request)
    return render(request, 'data/date_download.html', context)


def get_user_key(request):
    user_name = request.session.get('username')
    user = User.objects.get(user_name=user_name)
    return user.user_key


@cache_page(60 * 60)
def get_companies(request):
    company_names = DataApi.get_companies()
    return JsonResponse(company_names, safe=False)
