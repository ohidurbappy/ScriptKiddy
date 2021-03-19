from newsapi import NewsApiClient
import json

API_KEY='NEWS_API_KEY'


# Init
newsapi = NewsApiClient(api_key=API_KEY)

# /v2/top-headlines
# top_headlines = newsapi.get_top_headlines(q='bitcoin',
                                          
#                                           category='business',
#                                           language='en',
#                                           country='us')

# /v2/everything
# all_articles = newsapi.get_everything(q='bitcoin',
#                                       sources='bbc-news,the-verge',
#                                       domains='bbc.co.uk,techcrunch.com',
#                                       from_param='2017-12-01',
#                                       to='2017-12-12',
#                                       language='en',
#                                       sort_by='relevancy',
#                                       page=2)

all_articles = newsapi.get_everything(q='coronavirus',
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)

# /v2/sources
# sources = newsapi.get_sources()
f=open("response.json",'w')
json.dump(all_articles,f)
f.close()

print(all_articles)