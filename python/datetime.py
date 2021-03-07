import datetime

print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
print('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
print('Date now: %s' % datetime.datetime.now())
print('Date today: %s' % datetime.date.today())

today = datetime.date.today()
print("Today's date is {:%b, %d %Y}".format(today))

schedule = '{:%b, %d %Y}'.format(today) + ' - 6 PM to 10 PM Pacific'
schedule2 = '{:%B, %d %Y}'.format(today) + ' - 1 PM to 6 PM Central'
print('Maintenance: %s' % schedule)
print('Maintenance: %s' % schedule2)
