import requests
import pandas as pd 
from elasticsearch_dsl import Search
from news_app.get_env_values import get_secret
import json


# categories = json.loads(get_secret())
# print(categories)
categories = ['general','business','entertainment','health','science','sports','technology']


def get_ms_data():
    datadf = pd.DataFrame()
    ApiKey = get_secret('MEDIASTACK_KEY')
    ApiKey = 'ed13ad73bdb998a16dfa40dde2d4ef77'
    url ="https://api.mediastack.com/v1/news?access_key={api_key}&categories={category}"
    for category in categories:
        try:
            response = requests.get(url.format(api_key=ApiKey,category=category))
            response.raise_for_status() 
            data = response.json()
            if data:
                if 'data' in data.keys():
                    df=pd.DataFrame(data['data'])
                    df.drop(['language','country'],inplace=True, axis=1)
                    df=df.rename(
                        columns={'url':'source_url',
                                'published_at':'publishedAt' 
                                }
                    )
                    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
                    df = remove_duplicate(df,category)
                    datadf = pd.concat([df,datadf], ignore_index=True)
        except Exception as e:
            print(e)
        # status=insert_to_db(scrap_data)
        # print(status)
    datadf=datadf.drop_duplicates(subset=['title', 'description','category'])
    return datadf.to_dict(orient='records')


def remove_duplicate(df,category):
    try:
        search = Search(using='default', index='news')
        search = search.query('match', category=category)
        search = search.sort('-publishedAt')
        search = search[:1]
        response = search.execute()
        if len(response) > 0:
            res = response[0].publishedAt
            res = pd.to_datetime(res)
            df = df[(df['publishedAt'] > res) & (df['category'] == category)]
    except:
        pass
    return df

def clean_data(df):
    return df.dropna(axis=0,subset=['title','description','publishedAt'])