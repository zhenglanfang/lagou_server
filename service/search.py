from datetime import date
from datetime import timedelta
from django.core.paginator import Paginator

from service.base import BasePositions
from service.util import util_functions


class SearchLogic(BasePositions):
    need_field = ['position_id', 'position_name', 'publish_date', 'education', 'work_year', 'job_nature', 'salary',
                  'city', 'district', 'company_name']

    @classmethod
    @util_functions.my_cache
    def filter_date(cls):
        now_date = date.today()
        start_date = now_date - timedelta(days=60)
        recent_positions = cls.filter_position_time(start_date=start_date, end_date=now_date)
        recent_positions = cls.set_avg_salary(recent_positions)
        return recent_positions

    @classmethod
    def search_position(cls, key_word=None, city=None, work_year=None, education=None, job_nature=None, salary=None, sort='0'):
        recent_positions = cls.filter_date()
        if key_word:
            result = recent_positions[(recent_positions['position_name'].str.contains(key_word)) |
                                  (recent_positions['job_detail'].str.contains(key_word))]
            result.sort_values(by='position_name', inplace=True)
        else:
            result = recent_positions
        if city and city[0]:
            result = result[result['city'].isin(city)]
        if work_year and work_year[0]:
            result = result[result['work_year'].isin(work_year)]
        if education and education[0]:
            result = result[result['education'].isin(education)]
        if job_nature and job_nature[0]:
            result = result[result['job_nature'].isin(job_nature)]
        if salary:
            salary_range = salary.split('-')
            if len(salary_range) > 1:
                salary_min = int(salary_range[0])
                salary_max = int(salary_range[1])
                result = result[(result['avg_salary'] >= salary_min) & (result['avg_salary'] <= salary_max)]
            else:
                result = result[result['avg_salary'] >= 50]
        if sort == '1':
            # 按时间索引进行排序
            result.sort_index(inplace=True, ascending=False)
        # 将dataframe对象转换为 [{key:value},...]
        result = result[cls.need_field]
        return result.to_dict(orient='records')

    # 分页
    @staticmethod
    def page(result, page_now, page_size=10):
        '''
        分页,下面的分页共显示9列,当点击第5的时候,添加一个
        :param result: 总数据集合
        :param page_size: 每页显示的数量
        :param page_now: 当前页码
        :return: context字典,包含需要的数据
        '''
        p = Paginator(result, page_size)
        page_range = p.page_range
        # 如果传递的page_now,不存在就设置为1
        # page_now.isdigit() ：传递的page_now是字符串
        page_now = int(page_now)
        if page_now not in p.page_range:
            page_now = 1

        # 总页小于9
        if p.num_pages <= 9:
            pass
        # page_now < 5 时
        elif page_now <= 5:
            page_range = range(1, 10)
        # page_now:下面的页数大于4
        elif p.num_pages - page_now >= 4:
            page_range = list(range(page_now - 4, page_now + 5))
        # page_now:下面的页数小于4
        else:
            page_range = page_range[-10:]

        pages = p.page(page_now)
        context = {
            'count': p.count,  # 总记录数
            'num_pages': p.num_pages,  # 总页数
            'page_range': page_range,  # 页码列表
            'page_now': page_now,  # 当前页码
            'objs': pages.object_list,  # 当前页上所有对象的列表
            'pages': pages  # 当前page对象
        }
        return context

    @classmethod
    def search_company(cls, company_name):
        recent_positions = cls.filter_date()
        result = recent_positions[recent_positions['company_name'] == company_name]
        result = result[cls.need_field]
        return result.to_dict(orient='records')

    @classmethod
    def search_one_position(cls, position_id):
        result = cls.get_positions_dataframe()
        result = result[result['position_id'] == position_id]
        result = result.to_dict(orient='records')
        return result


if __name__ == '__main__':
    SearchLogic.search_position(key_word='java')
