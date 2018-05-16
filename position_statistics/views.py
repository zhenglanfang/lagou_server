from django.shortcuts import render
from django.http import JsonResponse

from service.statistic import PositionStatistics
from user import user_decorator


@user_decorator.login
def statistics_index(request):
    return render(request, 'statistics/statistic_base.html')


def positions_rank(request):
    result = PositionStatistics.positions_rank()
    return JsonResponse(result)


def city_distribute(request):
    result = PositionStatistics.city_position_type_distribute()
    # result.sort(reversed=True, key=[item['value'] for item in result])
    return JsonResponse(result)


def position_type_distribute(request):
    result = PositionStatistics.position_type_distribute()
    return JsonResponse(result)


def position_city_distribute(request):
    result = PositionStatistics.position_city_distribute()
    # result.sort(reversed=True, key=[item['value'] for item in result])
    return JsonResponse(result)


def education_distribute(request):
    result = PositionStatistics.education_position_distribute()
    return JsonResponse(result)


def second_type_salary(request):
    result = PositionStatistics.second_type_salary()
    return JsonResponse(result)


def first_type_salary(request):
    result = PositionStatistics.first_type_salary()
    return JsonResponse(result)


def city_salary(request):
    result = PositionStatistics.city_salary()
    return JsonResponse(result)


def education_salary(request):
    result = PositionStatistics.education_salary()
    return JsonResponse(result)


def work_year_salary(request):
    result = PositionStatistics.work_year_salary()
    return JsonResponse(result)



