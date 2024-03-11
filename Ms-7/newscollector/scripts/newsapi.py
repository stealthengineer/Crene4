from decouple import config
import requests
import pandas as pd
import json
from elasticsearch_dsl import Search
from news_app.get_env_values import get_secret


CATEGORY = json.loads(get_secret('CATEGORY'))

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
    df = df[~df['title'].isin(['[Removed]','null'])]
    df = df[~df['description'].isin(['[Removed]','null'])]
    return df 

class DataCollector:
    def request_api(self):
        data = {}
        for each in CATEGORY:
            res = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&category={each}&apiKey={get_secret('NEWSAPI_SECRET')}")
            if res.status_code == 200:
                data[each]= list(json.loads(res.content).get('articles'))
        return data
    

    def manipulate_data(self,data):
        df = pd.DataFrame()
        for category,content in data.items():
            df1 = pd.DataFrame(content)
            df1['category'] = category
            df1['publishedAt'] = pd.to_datetime(df1['publishedAt'])
            df1 = remove_duplicate(df1,category)
            df = pd.concat([df,df1], ignore_index=True )

        df['source'] = df['source'].apply(lambda x:x['name'])
        df = df.rename(columns={'url': 'source_url'})
        df = clean_data(df)
        df=df.drop_duplicates(subset=['title', 'description','category'])
        final_data=df.to_dict('records')
        return final_data
    
    def main(self):
        res = 'No new data found'
        data = self.request_api()
        final_data = self.manipulate_data(data)
        if final_data:
        #     res = insert_to_db(final_data)
            return final_data
        #     res = insert_to_db(final_data)
            return final_data
        return res



