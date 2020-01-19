import requests
from bs4 import BeautifulSoup

#pick url to parse
url = 'https://overrustlelogs.net/2mgovercsquared%20chatlog'
#get html from url via requests
htmltext = requests.get(url).text
#send html to bs4
soup = BeautifulSoup(htmltext, 'html.parser')
print(soup.prettify())

#loop through all href= links. These are the months for the chatlogs