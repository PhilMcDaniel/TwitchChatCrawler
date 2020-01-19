import requests
import bs4 as soup
from bs4 import BeautifulSoup

#loop through site to get logs for all days in a month
#loop through site to get logs for all months available

#pick url to parse
url = 'https://overrustlelogs.net/2mgovercsquared%20chatlog/January%202020/2020-01-18'+ '.txt'
#print (url)

#get html from url via requests
htmltext = requests.get(url).text
# print(htmltext)

#split text based on line ends
lines = htmltext.splitlines()
print(lines[1])

#timestamp is 1-24, username = 25 through first colon after 25
time = lines[1][1:24]
print (time)

username = lines[1][25:]
print(username)

#parse text from single day's chatlogs


#separate datetime
#separate user
#serarate chatmessage