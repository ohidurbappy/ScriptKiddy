import sys

if sys.version_info.major == 3:
    from urllib.parse import urlencode, urlparse, urlunparse, parse_qs
else:
    from urllib import urlencode
    from urlparse import urlparse, urlunparse, parse_qs

url = 'http://example.com/?a=text&q2=text2&q3=text3&q2=text4&b#q2=keep_fragment'
u = urlparse(url)
query = parse_qs(u.query, keep_blank_values=True)
query.pop('q2', None)
u = u._replace(query=urlencode(query, True))
print(urlunparse(u))
