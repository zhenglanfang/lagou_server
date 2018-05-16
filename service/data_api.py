import json

from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

from service.base import BasePositions
from service.util import write_excel


class DataApi(BasePositions):
    need_field = ['position_name', 'salary', 'education', 'work_year', 'job_nature', 'company_name',
                  'city', 'district',  'job_detail','publish_date']

    @classmethod
    def job_api(cls, start_date, end_date):
        result = cls.filter_position_time(start_date=start_date, end_date=end_date)
        result = result[cls.need_field]
        # result = result[(result['position_name'].str.contains('java')) |
        #                           (result['job_detail'].str.contains('java'))]
        # result = result[result['education'] == '大专']
        # result = result[result['city'] == '上海']

        return result.to_dict(orient='records')

    @classmethod
    def company_api(cls, company_name):
        result = cls.get_positions_dataframe()
        result = result[result['company_name'] == company_name]
        result = result[cls.need_field]
        return result.to_dict(orient='records')

    @classmethod
    def download(cls, file_type, data):
        if file_type == 'json':
            # with open(file_path, 'wb') as f:
            write_data = json.dumps(data, ensure_ascii=False, indent=2)
            result = write_data.encode('utf-8')
        elif file_type == 'xlsx':
            wb = Workbook()
            sheet = wb.create_sheet(index=0)
            write_excel.WriteExcel.write_excel_dict(sheet, cls.need_field, data)
            result = save_virtual_workbook(wb)
            # wb.save(file_path)
            # result = '下载成功！'

        return result



