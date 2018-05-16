from service.base import BasePositions


class PositionStatistics(BasePositions):

    @classmethod
    def positions_rank(cls, rank_count=10):
        """
        职位的排名和比例
        :param rank_count:前多少名
        :return:返回排名前rank_count的职位信息:
        return: {year:{'first_type':[],'count':[],'score':[]}}
        """
        result = {}
        grouped = cls.group_by_year()
        for year, group in grouped:
            result[year] = {}
            first_type_counts = group['first_type'].value_counts()
            counts = first_type_counts.sum()
            score = first_type_counts.head(10) / counts * 100
            result[year]['type'] = list(score.index)
            result[year]['value'] = list(first_type_counts[0:rank_count])
            result[year]['score'] = list(score[0:rank_count])
        # import json
        # print(json.dumps(result,ensure_ascii=False,indent=2))
        # print(result)
        return result

    @classmethod
    def position_type_distribute(cls):
        """
         职位类别的比例和数量
         :return {year:{'second_type':[],'count':[],'score':[]}}
        """
        result = {}
        grouped = cls.group_by_year()
        for year, group in grouped:
            result[year] = {}
            second_type_counts = group['second_type'].value_counts()
            counts = second_type_counts.sum()
            score = second_type_counts / counts * 100
            result[year]['type'] = list(score.index)
            result[year]['value'] = list(second_type_counts)
            result[year]['score'] = list(score)
        return result

    @classmethod
    def city_position_type_distribute(cls):
        """不同城市的职位（主要是type）分布"""
        result = {}
        grouped = cls.group_by_year()
        for year, group in grouped:
            result[year] = []
            city_positions = group.groupby('city')
            sort_city = city_positions['city'].count().sort_values(ascending=False)
            for city in sort_city.index:
                city_group = city_positions.get_group(city)
                city_positions_count = (city_group.shape)[0]
                city_positions_score = city_positions_count / (group.shape)[0] * 100
                city_second_type_series = city_group['second_type'].value_counts()
                positions_type = list(city_second_type_series.index)
                positions_count = list(city_second_type_series)
                positions_score = list(city_second_type_series / city_positions_count * 100)
                # result[name][city] = [city_second_type.get(key,0) for key in second_type]
                city_item = {
                    'name': city,
                    'value': city_positions_count,
                    'score': city_positions_score,
                    'type_positions': {
                        'type': positions_type,
                        'count': positions_count,
                        'score': positions_score
                    }
                }
                result[year].append(city_item)

        return result

    @classmethod
    def position_city_distribute(cls):
        """
        职位在不同城市的分布
        :return {year:{first_type:{'city':[],'count',[],'score':[]}}}
        """
        result = {}
        grouped = cls.group_by_year()
        for year, group in grouped:
            result[year] = []
            type_positions = group.groupby('first_type')
            sort_type = type_positions['first_type'].count().sort_values(ascending=False).head(15)
            for first_type in sort_type.index:
                type_group = type_positions.get_group(first_type)
                city_positions_count = (type_group.shape)[0]
                value_counts = type_group['city'].value_counts()
                city_positions_item = {
                    'name': first_type,
                    'value': city_positions_count,
                    'score': city_positions_count / (group.shape)[0] * 100,
                    'type_positions': {
                        'type': list(value_counts.index)[0:20],
                        'count': list(value_counts)[0:20],
                        'score': list(value_counts / city_positions_count * 100)[0:20]
                    }
                }
                result[year].append(city_positions_item)
                # result[name][city] = [city_second_type.get(key,0) for key in second_type]
        return result

    @classmethod
    def education_position_distribute(cls):
        """
            职位的学历分布
            :return
            """
        result = {}
        grouped = cls.group_by_year()
        for year, group in grouped:
            result[year] = []
            education_positions = group.groupby('education')
            for education, education_group in education_positions:
                # result[year][education] = {}
                education_positions_count = (education_group.shape)[0]
                education_positions_score = education_positions_count / (group.shape)[0] * 100
                education_second_type_series = education_group['second_type'].value_counts()
                positions_type = list(education_second_type_series.index)
                positions_count = list(education_second_type_series)
                positions_score = list(education_second_type_series / education_positions_count * 100)
                # result[year][city] = [city_second_type.get(key,0) for key in second_type]
                education_item = {
                    'name': education,
                    'value': education_positions_count,
                    'score': education_positions_score,
                    'type_positions': {
                        'type': positions_type,
                        'count': positions_count,
                        'score': positions_score
                    }
                }
                result[year].append(education_item)
        return result

    @classmethod
    def second_type_salary(cls):
        """不同大类别职位的平均薪资"""
        result = {}
        df = cls.set_avg_salary()
        grouped = df.groupby('year')
        for year, group in grouped:
            salary_mean = group.groupby('second_type')['avg_salary'].mean().sort_values(ascending=False)
            second_type = list(salary_mean.index)
            values = list(salary_mean)
            result[year] = {
                'type': second_type,
                'value': values
            }
        return result

    @classmethod
    def first_type_salary(cls):
        """不同职位的平均薪资"""
        result = {}
        df = cls.set_avg_salary()
        grouped = df.groupby('year')
        for year, group in grouped:
            salary_mean = group.groupby('first_type')['avg_salary'].mean().sort_values(ascending=False)
            first_type = list(salary_mean.index)
            values = list(salary_mean)
            result[year] = {
                'type': first_type,
                'value': values
            }
        return result

    @classmethod
    def city_salary(cls):
        """不同城市的平均薪资"""
        result = {}
        df = cls.set_avg_salary()
        grouped = df.groupby('year')
        for year, group in grouped:
            result[year] = []
            city_salary_groups = group.groupby('city')
            sort_salary_city = city_salary_groups['avg_salary'].mean().sort_values(ascending=False).head(30)
            for city in sort_salary_city.index:
                first_type_mean = city_salary_groups.get_group(city).groupby('first_type')[
                    'avg_salary'].mean().sort_values(ascending=False)
                first_type_list = list(first_type_mean.index)
                values_list = list(first_type_mean)
                city_item = {
                    'name': city,
                    'value': sort_salary_city[city],
                    'type_positions': {
                        'first_type': first_type_list[0:20],
                        'values': values_list[0:20]
                    }
                }
                result[year].append(city_item)
        return result

    @classmethod
    def education_salary(cls):
        """不同学历要求的薪资分布"""
        result = {}
        df = cls.set_avg_salary()
        grouped = df.groupby('year')
        for year, group in grouped:
            result[year] = []
            education_salary_groups = group.groupby('education')
            sort_salary_education = education_salary_groups['avg_salary'].mean().sort_values(ascending=False)
            for education in sort_salary_education.index:
                first_type_mean = education_salary_groups.get_group(education).groupby('first_type')[
                    'avg_salary'].mean().sort_values(ascending=False)
                first_type_list = list(first_type_mean.index)
                values_list = list(first_type_mean)
                item = {
                    'name': education,
                    'value': sort_salary_education[education],
                    'type_positions': {
                        'first_type': first_type_list,
                        'values': values_list
                    }
                }
                result[year].append(item)
        return result

    @classmethod
    def work_year_salary(cls):
        """不同工作经验要求的薪资分布"""
        result = {}
        df = cls.set_avg_salary()
        grouped = df.groupby('year')
        for year, group in grouped:
            result[year] = []
            factor_salary_groups = group.groupby('work_year')
            sort_salary_factor = factor_salary_groups['avg_salary'].mean().sort_values(ascending=False)
            for factor in sort_salary_factor.index:
                first_type_mean = factor_salary_groups.get_group(factor).groupby('first_type')[
                    'avg_salary'].mean().sort_values(ascending=False)
                first_type_list = list(first_type_mean.index)
                values_list = list(first_type_mean)
                item = {
                    'name': factor,
                    'value': sort_salary_factor[factor],
                    'type_positions': {
                        'first_type': first_type_list,
                        'values': values_list
                    }
                }
                result[year].append(item)
        return result


if __name__ == '__main__':
    # work_year_salary = PositionStatistics.work_year_salary()
    position_rank = PositionStatistics.positions_rank()
