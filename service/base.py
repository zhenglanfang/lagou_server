import re
import numpy as np
import pandas as pd

from search import models
from service.util import util_functions


class BasePositions(object):

    @classmethod
    @util_functions.my_cache
    def get_positions_dataframe(cls):
        """获取全部数据"""
        positions = models.Positions.objects.values()
        df = pd.DataFrame(list(positions))
        df['year'] = pd.to_datetime(df['publish_date']).dt.year
        df['date'] = pd.to_datetime(df['publish_date'])
        df['publish_date'] = df['publish_date'].apply(lambda x:str(x))
        return df

    @classmethod
    @util_functions.my_cache
    def group_by_year(cls):
        """按年份分组"""
        df = cls.get_positions_dataframe()
        grouped = df.groupby('year')
        return grouped

    @classmethod
    @util_functions.my_cache
    def get_second_type(cls):
        df = cls.get_positions_dataframe()
        second_type_series = df['second_type'].value_counts()
        return list(second_type_series.index)

    @classmethod
    @util_functions.my_cache
    def get_first_type(cls):
        df = cls.get_positions_dataframe()
        first_type_series = df['first_type'].value_counts()
        return list(first_type_series.index)

    @classmethod
    @util_functions.my_cache
    def get_city(cls):
        """获取所以城市"""
        df = cls.get_positions_dataframe()
        citys = df['city'].value_counts()
        return list(citys.index)

    @classmethod
    @util_functions.my_cache
    def get_companies(cls):
        """获取全部公司"""
        df = cls.get_positions_dataframe()
        companies = df['company_name'].value_counts()
        return list(companies.index)

    @classmethod
    def filter_position_time(cls, start_date, end_date):
        """选择某时间段的数据"""
        df = cls.get_positions_dataframe()
        # inplace=True 在原数据集上修改的, drop=True设置成索引的列会从DataFrame中移除
        recent_positions = df.set_index(df['date'], drop=False)
        recent_positions = recent_positions[str(start_date):str(end_date)]
        return recent_positions

    @staticmethod
    def get_avg(str):
        """计算平均薪资"""
        array = re.findall(r'(\d+)[kK]', str)
        x = np.array(array, dtype=np.int32)
        return x.mean()

    @classmethod
    def set_avg_salary(cls, df=None):
        if df is None:
            df = cls.get_positions_dataframe()
        df['avg_salary'] = df['salary'].map(cls.get_avg)
        return df


if __name__ == '__main__':
    # job = BasePositions()
    df = BasePositions.get_positions_dataframe()
    second_type = BasePositions.get_second_type()
    print(df.head())
