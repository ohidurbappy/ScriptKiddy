#pip install newspaper3k
from newspaper import Article
url = "YOUR_TARGET_URL"
article = Article(url)
article.download()
article.parse()
print(article.authors)
print("Article Publication Date:")
print(article.publish_date)
print("Major Image in the article:")
print(article.top_image)
article.nlp()
print ("Keywords in the article")
print(article.keywords)
print("Article Summary")
print(article.summary)
print(article.article_html)