from GoogleNews import GoogleNews
from googletrans import Translator

translator = Translator()
# translator = Translator(service_urls=[
#       'translate.google.com',
#       'translate.google.co.kr',
#     ])

googlenews = GoogleNews()
# googlenews = GoogleNews('en','d')
googlenews.search('corona virus')
googlenews.getpage(1)
# googlenews.result()
# googlenews.gettext()
# googlenews.getlinks()
# googlenews.clear()

news_titles=[]
for result in googlenews.result():
    print(result['title'])
    news_titles.append(result['title'])

t=translator.translate(news_titles,dest='bn')

output=''
for title in t:
    print(title.origin+'->'+title.text)
    output+=title.origin+'\n:'+title.text+'\n'

f=open('translation.txt','w',encoding='utf-8')
f.write(output)
f.close()