import pdfplumber
import re
import sys
import os

TAG = 'PdfPlumber_Demo:'


class Util:
    @staticmethod
    def get_page_text(text_page):
        text_str = []
        text_list = []
        for line in text_page:
            text_list.append(list(filter(lambda x: len(str(x[0]).strip()) > 0, line)))
            text_line = ''
            for ch in line:
                text_line += (str(ch[0]) + '~[' + str(ch[1]) + '->' + str(ch[2]) +
                              ' | ' + str(ch[3]) + '->' + str(ch[4]) + ']; ')
            text_str.append(text_line)
        text_str = "\n".join(text_str)
        return text_list, text_str

    __x_thr = 6
    col_list = ['2018', '2017', '權益總額']

    @staticmethod
    def get_value(text_list, key_list):
        col_list = Util.__get_col_loc(text_list)
        result_list = {}
        for key in key_list:
            for i in range(0, text_list.__len__()):
                cu_line = text_list[i]
                if list(filter(lambda x: x[0].strip().lower() == key.lower(), cu_line)):
                    result_line = Util.__check_col(cu_line, col_list, Util.__x_thr)
                    Util.__format_text(result_line)
                    result_list[key] = list(map(lambda x: {'key': x[0], 'col': x[1], 'val': x[2]}, result_line))
        return result_list

    @staticmethod
    def __get_col_loc(text_list):
        col_list = []
        for line in text_list:
            for cell in line:
                for col in Util.col_list:
                    if cell and re.match('^(' + col + ')$', str(cell[0])) is not None:
                        col_list.append([cell[0], cell[1], cell[2], cell[1] + (cell[2] - cell[1]) / 2])
        return col_list

    @staticmethod
    def __check_col(text_line, col_list, thr=5):
        result_line = []
        for col in col_list:
            cell_list = []
            for cell in text_line:
                d_l = abs(col[1] - cell[1])
                d_r = abs(col[2] - cell[2])
                d_c = abs(col[3] - (cell[1] + (cell[2] - cell[1]) / 2))
                dis = 0 if (d_l < thr) or (d_r < thr) else d_c
                cell_list.append([text_line[0][0] + '(' + text_line[1][0] + ')',
                                  col[0], cell[0].replace(' ', ''), dis])
            cell_list.sort(key=lambda x: x[3], reverse=False)
            if cell_list:
                result_line.append(cell_list[0])
        return result_line

    @staticmethod
    def __format_text(text):
        for cell in text:
            cell[2] = (cell[2] if re.match(
                '^(\(?-?([0-9]*,)*[0-9]+\.?[0-9]*\)?)$', cell[2]) is not None else '')
            # cell[2] = re.sub('[(),]+', '', cell[2])


def run(pdf_path, key_list=None, col_list=None, page_list=None):
    print('wwwwwwwwwwwwwwwwwww')
    if not key_list:
        return {}
    if col_list:
        Util.col_list = col_list
    print(TAG, 'file path =', pdf_path)
    pdf_file = pdfplumber.open(pdf_path)
    text_ori = []
    text_result = []
    page_i = 0
    for page in pdf_file.pages:
        page_i = page_i + 1
        if page_list and page_i not in page_list:
            continue
        text_list, text_str = Util.get_page_text(page.extract_text_my())
        text_ori.append(text_str)
        text_result.append(Util.get_value(text_list, key_list))
    print(TAG, 'pdf run end, page num =', page_i)
    pdf_file.close()
    return text_result, text_ori
