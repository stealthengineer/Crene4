import requests
import pandas as pd 
from elasticsearch_dsl import Search
from datetime import datetime,timedelta,date
from news_app.get_env_values import get_secret
import json



categories = json.loads(get_secret('NY_CATEGORY'))


def getdata_nytimes():
    datadf = pd.DataFrame()
    datadf = pd.DataFrame()
    ApiKey = get_secret('NYTIMES_KEY')

    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q={category}&begin_date={begin_date}&api-key={api_key}"
    for category in categories:
        try:
            response = requests.get(url.format(category=category, begin_date = get_begin_date(category), api_key = ApiKey))
            response.raise_for_status()  
            data = response.json()
            if data:
                if 'response' in data.keys():
                    df=manipulate_data(data['response']['docs'],category)
                status=11
                print(url.format(category=category, begin_date = get_begin_date(category), api_key = ApiKey))
                status=11
                print(url.format(category=category, begin_date = get_begin_date(category), api_key = ApiKey))
                print(status)
                datadf = pd.concat([df,datadf], ignore_index=True )
                datadf = pd.concat([df,datadf], ignore_index=True )
            else:
                print("Failed to fetch API data.")
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            status = e
    datadf=datadf.drop_duplicates(subset=['title', 'description','category'])
    return datadf.to_dict(orient='records')
    # return status

def manipulate_data(data,category):
    df = pd.DataFrame.from_records(data) 
    df['category'] = category
    
    df.rename(columns = {'lead_paragraph':'content', 
                    'headline':'title',
                        'web_url':'source_url',
                        'pub_date':'publishedAt',
                        'byline':'author',
                        'snippet':'description',
                    },
            inplace = True)

    df['title']= df['title'].apply(lambda x: x['print_headline'])
    df['author']= df['author'].apply(lambda x: x['original'])
    df =clean_data(df)
    df.fillna('No Data', inplace=True)
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df=remove_duplicate(df,category)
    df=df[['content', 'title','source_url','publishedAt','author','description','source','category']]
    return df
 


def get_begin_date(category):
    try:
        search = Search(using='default', index='news')
        search = search.query('match', category=category)   
        search = search.query('match', category=category)   
        search = search.sort('-publishedAt')
        search = search[:1]
        response = search.execute()
        if len(response) > 0:
            res = response[0].publishedAt
            dt_object = datetime.fromisoformat(res[:-6])
            if int(dt_object.month)<10 & int(dt_object.day)<10:
                return f'{dt_object.year}0{dt_object.month}0{dt_object.day}'
            elif int(dt_object.month)<10:
                return f'{dt_object.year}0{dt_object.month}{dt_object.day}'
            elif int(dt_object.day)<10:
                return f'{dt_object.year}{dt_object.month}0{dt_object.day}'
            return f'{dt_object.year}{dt_object.month}{dt_object.day}'
        else :
            return str(date.today()-timedelta(days = 1)).replace('-','')
    except:
        return str(date.today()-timedelta(days = 1)).replace('-','')


def remove_duplicate(df,category):
    try:
        search = Search(using='default', index='news')
        search = search.query('match', category=category)
        search = search.sort('-publishedAt')
        search = search[:1]
        response = search.execute()
        if len(response) > 0:
            date_string = response[0].publishedAt
            res = pd.to_datetime(date_string)
            date_string = response[0].publishedAt
            res = pd.to_datetime(date_string)
            df = df[(df['publishedAt'] > res) & (df['category'] == category)]
    except:
        pass
    return df

def clean_data(df):
    return df.dropna(axis=0,subset=['title','description','publishedAt'])
    return df.dropna(axis=0,subset=['title','description','publishedAt'])