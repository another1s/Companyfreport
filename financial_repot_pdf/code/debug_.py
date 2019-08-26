import pandas as pd
import tabula
from pandas.api.types import *
import numpy as np
import csv
import pdfplumber
import re
import warnings
warnings.filterwarnings("ignore")
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
    #print('wwwwwwwwwwwwwwwwwww')
    if not key_list:
        return {}
    if col_list:
        Util.col_list = col_list
    #print(TAG, 'file path =', pdf_path)
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
    #print(TAG, 'pdf run end, page num =', page_i)
    pdf_file.close()
    return text_result, text_ori





def one_row(data):
    with open('result.csv', 'a+', newline='', encoding='utf-8') as f:
        header = data.keys()
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        writer.writerow(data)
        f.close()


def multi_row(data):
    with open('results.csv', 'a+') as f:
        header = data.keys()


def search_key(directory, query=None):
    chinese_target = ['收入', '利润', '资产', '负债', '权益']
    english_target = ['Revenues', 'Profit', 'asset', 'liabilities', 'equity', 'profit', 'revenues']
    target = set()
    for i, v in directory.items():
        if query:
            for q in query:
                try:
                    if v.find(q)>=0:
                        r = v.find(q)
                        target.add(i)
                        break
                except Exception as e:
                    #print(e)
                    pass
        else:
            for cw, ew in zip(chinese_target, english_target):
                try:
                    if v.find(cw)>=0 or v.find(ew)>=0:
                        r1 = v.find(cw)
                        r2 = v.find(ew)
                        target.add(i)
                        break
                except Exception as e:
                    #print(e)
                    pass
    return target


def specify_col(cols, colname):
    res = np.where(cols == colname)
    return res[0].min(), colname


def merge_result(res1, res2):
    res3 = res1.combine_first(res2)
    return res3

finalized_result = dict()
'''
ta = sys.argv
finalized_result['target'] = list()
for i in ta:
    if not (i == 'combine.py'):
        finalized_result['target'].append(i)
print(finalized_result['target'])
'''
finalized_result['target']=['商譽', '遞延稅項資產']
df = tabula.read_pdf("../datafolder/demo.pdf", pages='4', encoding='utf-8')
columns = df.columns
columns_name = columns._data
nn = list()
vv = list()
names = ['2014', '2013']
for name in names:
    v, n = specify_col(columns_name, name)
    finalized_result[name] = list()
    nn.append(n)
    vv.append(v)
rows = df.index
col1 = df.iloc[:, 0]
col2 = df.iloc[:, 1]
a, b = run("../datafolder/demo.pdf", finalized_result['target'] , ['2013', '2014'], [4])

if not(pd.isnull(col2).any()) and not (is_float_dtype(col2) and is_integer_dtype(col2)):
    #print("hello")
    DirOfTable = pd.concat([col1, col2], axis=0)
    #print(search_key(DirOfTable, ['profit']))
    for digit in search_key(DirOfTable, ['profit']):
        for col, name in zip(vv, nn):
            #print(df.iloc[digit, col])
            finalized_result[name].append(df.iloc[digit, col])
else:
    DirOfTable = col1
    #print(search_key(DirOfTable, ['商譽', '遞延稅項資產']))
    for digit in search_key(DirOfTable, finalized_result['target']):
        for col, name in zip(vv, nn):
            #print(df.iloc[digit, col])
            finalized_result[name].append(df.iloc[digit, col])
#print(finalized_result)
print(a, type(a))
for i in a:
    one_row(i)
df1 = pd.DataFrame(finalized_result)

#print('tabula_result:\n')
#print(df1)
df1.to_csv("test.csv", index=False, sep=',', encoding='utf_8_sig')
print("done\n")