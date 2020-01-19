import requests
import bs4 as soup
from bs4 import BeautifulSoup
import pandas as pd

#loop through site to get logs for all days in a month
#loop through site to get logs for all months available

#pick url to parse
url = 'https://overrustlelogs.net/2mgovercsquared%20chatlog/January%202020/2020-01-18'+ '.txt'
#print (url)

#get html from url via requests
htmltext = requests.get(url).text
# print(htmltext)

# split text based on line ends
lines = htmltext.splitlines()
# print(lines[1])
listofrows = []
for n in lines:
    #print(n)
    #timestamp is 1-24
    time = n[1:24]
    #print (time)
    # username = 25 + 1 for space through first colon after 25
    username = n[26:n.find(':',25)]
    # print(username)
    # chat message = first colon after 25(+1 for colon + 1 for space) through end of line
    message = n[n.find(':',25)+2:]
    # print (message)
    # put pieces into list
    row = [time,username,message]
    # print (row)
    listofrows.append(row)

print(listofrows)