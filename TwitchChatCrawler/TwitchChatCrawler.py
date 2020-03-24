import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import re
import uuid


# database parameters
DB = {'servername': 'DESKTOP-1ERS7HG\SQLEXPRESS',
      'database': 'TwitchChat_DB',
      'driver': 'driver=SQL Server Native Client 11.0'}

# create guid for batch
batchid = uuid.uuid4()


# create the connection
engine = create_engine('mssql+pyodbc://' + DB['servername'] + '/' + DB['database'] + "?" + DB['driver'])

# base url, variables will be used for the rest of the link
base = 'https://overrustlelogs.net'

# at month level, read html text to get list of daily links later
soup = BeautifulSoup(requests.get(base+'/2mgovercsquared%20chatlog/March%202020').text, 'html.parser')
# print(soup)

# loop through all links that end in 10 char date format
for link in soup.find_all('a'):
    dayurl = ''
    links = base+link.get('href')
    # print(links)

    m = re.search(r"[\d]{4}-[\d]{1,2}-[\d]{1,2}",(links[len(links)-10:len(links)]))
    # if the pattern matches do stuff
    if m:
        dayurl = base+link.get('href')
        print(dayurl)
        # get html from url via requests
        htmltext = requests.get(dayurl+'.txt').text
        # print(htmltext)
        
        # split text based on line ends
        lines = htmltext.splitlines()
        # print(lines[1])

        # get channel name. starts @27 and ends @%20
        start = 27
        end = dayurl.find(' chatlog',0,-1)
        channel = dayurl[start:end]
        # print(channel)

        listofrows = []
        # initialize data frame
        df = pd.DataFrame()
        
        for n in lines:
            # print(n)

            # date is first 10 char
            date = n[1:11]
            # print (date)

            # timestamp is 1-19
            datetime = n[1:20]
            # print (datetime)

            # username = 25 + 1 for space through first colon after 25
            username = n[26:n.find(':',25)]
            # print(username)
            # chat message = first colon after 25(+1 for colon + 1 for space) through end of line
            message = n[n.find(':',25)+2:]
            # print (message)
            # put pieces into list
            row = [batchid,channel,date,datetime,username,message]
            # print (row)
            listofrows.append(row)
            # print(listofrows)
            
            df = pd.DataFrame(data = listofrows)
            df.columns = ['ETL_Batch_ID','Channel_NME','Message_DTE','Message_DTM','Username_TXT','Message_TXT']
        # df

        # write data to sql server
        df.to_sql('Chat_Message_F'
                    , index=False
                    , con=engine
                    , if_exists='append'
                    , chunksize=100
                    )

        # readback as a test to see if insert worked
        # pd.read_sql('SELECT * FROM Chat_Message_F', engine)