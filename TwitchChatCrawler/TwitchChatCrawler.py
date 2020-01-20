import requests
import bs4 as soup
from bs4 import BeautifulSoup
import pandas as pd
import sqlalchemy

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
    #timestamp is 1-19
    time = n[1:20]
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
df = pd.DataFrame(data = listofrows)
df.columns = ['Message_DTM','Username','Message_TXT']
# df


# database parameters
DB = {'servername': 'PHIL-PC\SQLEXPRESS',
      'database': 'TwitchChat_DB',
      'driver': 'driver=SQL Server Native Client 11.0'}

# create the connection
engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])

# write data to sql server
df.to_sql('Chat_Message_F'
          , index=False
          , con=engine
          , if_exists='replace'
          , chunksize=100
          )

# readback as a test to see if insert worked
pd.read_sql('SELECT * FROM Chat_Message_F', engine)