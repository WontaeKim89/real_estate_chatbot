import os
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from base.settings import ELASTIC_SEARCH



def index_dataframe_to_elasticsearch(df, index_name):
    es = Elasticsearch(
        hosts=ELASTIC_SEARCH["hosts"],
        http_auth=ELASTIC_SEARCH["http_auth"],
        verify_certs=ELASTIC_SEARCH["verify_certs"]
    )
    mappings = {
        "settintgs": {
            "analysis": {
                "analyzer": {
                    "korean": {
                        "type": "custom",
                        "tokenizer": "nori_tokenizer",
                        "filter": ["nori_readingform", "lowercase", "nori_part_of_speech_basic"]
                    }
                }
            }
        },

        "mappings": {
            "properties": {
                "자치구명": {
                    "type": "keyword",
                    "analyzer": "korean",  # '자치구명'필드에 한국어 형태 분석기 적용
                    "fields": {
                        "text": {
                            "type": "text"
                        }
                    }
                },
                "법정동명": {
                    "type": "keyword",
                    "analyzer": "korean",
                    "field": {
                        "text": {
                            "type": "text"
                        }
                    }
                },
                "건물명": {
                    "type": "text",
                    "analyzer": "korean",
                    "field": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "계약일": {"type": "integer"},
                "물건금액(만원)": {"type": "integer"},
                "건물면적(㎡)": {"type": "float"},
                "토지면적(㎡)": {"type": "float"},
                "층": {"type": "float"},
                "건축년도": {"type": "integer"},
                "건물용도": {
                    "type": "text",
                    "analyzer": "korean",
                    "field": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "신고구분": {
                    "type": "keyword",
                    "analyzer": "korean",
                    "field": {
                        "text": {
                            "type": "text"
                        }
                    }
                },
                "면적(평)": {"type": 'integer'},
                "사용승인일(연식)": {"type": "integer"}
            }
        }
    }

    # 인덱스 생성
    if not es.indices.exists(index="real_estate_lexical_db"):
        es.indices.create(index=index_name, body=mappings, ignore=400)

    # DataFrame에서 문서 생성
    def generate_documents():
        for _, row in df.iterrows():
            yield {
                "_index": index_name,
                "_source": row.to_dict()
            }

    # Bulk API를 사용하여 문서 색인화
    bulk(es, generate_documents())


def elastic_search_index_generator():
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
    df = pd.read_csv(os.path.join(data_path, file_nm), encoding='CP949', usecols=use_col)
    df = df.reset_index()

    # Preprocessing

    # 평수 컬럼 추가
    df['면적(평)'] = [int(i) for i in df['건물면적(㎡)'] / 3.306]

    # 건축연도 정보없는 데이터 제거
    df = df[~df['건축년도'].isnull()]
    df = df[~df['건물명'].isnull()]
    df = df[~df['신고구분'].isnull()]
    df['건축년도'] = df['건축년도'].astype(int)

    # 연식 컬럼 추가
    df['사용승인일(연식)'] = ['정보없음' if type(i) == str else int(2024 - i) for i in df['건축년도'].values]

    # 단독다가구의 개념이 모호하며, 데이터수가 많지 않아 제거함
    df[df['건물용도'] != '단독다가구']

    # 건물 형태에 대한 검색이 있을 경우, 연립다세대보다는 '빌라'로 검색하는 경우가 많기 때문에 '빌라(연립다세대)'로 변경
    df['건물용도'] = ['빌라(연립다세대)' if i == '연립다세대' else i for i in df['건물용도'].values]

    # 지번구분명이 대지가 아닌 데이터 제거(총 26건 - 산, 블럭에 해당)
    df = df[df['지번구분명'] == '대지']

    # 일반적인 질의 구문에 포함되지않을 것으로 보이는 정보 컬럼은 제거
    del df['접수연도'], df['지번구분명'], df['신고한 개업공인중개사 시군구명'], df['index']

    # DataFrame을 'real_estate_transactions' 인덱스에 색인화
    index_dataframe_to_elasticsearch(df, "real_estate_transactions")
