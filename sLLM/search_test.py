import pandas as pd
import os

def searchtest(query):
    use_col = [
        '접수연도',
        '자치구명',
        '법정동명',
        '지번구분명',
        '건물명',
        '계약일',
        '물건금액(만원)',
        '건물면적(㎡)',
        '토지면적(㎡)',
        '층',
        '건축년도',
        '건물용도',
        '신고한 개업공인중개사 시군구명',
        '신고구분'
    ]
    data_path = './data'
    file_nm = 'seoul_real_estate_2023.csv'
    df = pd.read_csv(os.path.join(data_path, file_nm), encoding='CP949', usecols= use_col)
    df = df.reset_index()
    temp = df[df['자치구명']==query].iloc[0, :].values
    return temp