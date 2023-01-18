from GoogleNews import GoogleNews
googlenews = GoogleNews()
# googlenews = GoogleNews('en','d')

q=input("Input a keyword to Search: ")
googlenews.search(q)
googlenews.getpage(1)
# googlenews.gettext()
# googlenews.getlinks()

print("Google News")
print("-"*65)

for result in googlenews.result():
    print(result['title'])
    print(result['desc'])
    print(result['link'])
    print('-'*65)

for page in range(2,5):
    googlenews.clear()
    googlenews.getpage(page)
    for result in googlenews.result():
        print(result['title'])
        print(result['desc'])
        print(result['link'])
        print('-'*65)