import pandas as pd
import requests
import xml.etree.ElementTree as ET

def clean_url(searched_item, data_filter):
    x = pd.Timestamp.today()
    today = str(x)[:10]
    yesterday = str(x + pd.Timedelta(days=-1))[:10]
    this_week = str(x + pd.Timedelta(days=-7))[:10]
    if data_filter == 'today':
        time_period = 'after%3A' + yesterday
    elif data_filter == 'this_week':
        time_period = 'after%3A'+ this_week + '+before%3A' + today
    elif data_filter == 'this_year':
        time_period = 'after%3A'+str(x.year - 1)
    elif str(data_filter).isdigit():
        temp_time = str(x + pd.Timedelta(days=-int(data_filter)))[:10]
        time_period = 'after%3A'+ temp_time + '+before%3A' + today
    else:
        time_period = ''
    url = f'https://news.google.com/rss/search?q={searched_item}+'+time_period+'&hl=en-US&gl=US&ceid=US%3Aen'
    return url

def get_news(search_term, data_filter=None):
    url = clean_url(search_term, data_filter)
    response = requests.get(url)
    root = ET.fromstring(response.text)
    title = [i.text for i in root.findall('.//channel/item/title')]
    link = [i.text for i in root.findall('.//channel/item/link')]
    description = [i.text for i in root.findall('.//channel/item/description')]
    pubDate = [i.text for i in root.findall('.//channel/item/pubDate')]
    source = [i.text for i in root.findall('.//channel/item/source')]
    df = pd.DataFrame({'title': title, 'link': link, 'description': description, 'date': pubDate, 'source': source})
    df.date = pd.to_datetime(df.date, unit='ns')
    return df
