import json
import pandas as pd
import requests
from urlextract import URLExtract
import html2text
import ftfy

class Polapi():
    """This Class has methods to interact with the 4chan API and its EndPoints"""

    def get4chanboards(self,boardid=None):
        """This function returns a single board or a list of all 4Chan Boards"""

        url = "https://a.4cdn.org/boards.json"
        df = pd.DataFrame(json.loads(requests.get(url).text)['boards'])

        if boardid:
            return df.query(f'board == "{boardid}"')

        return df

    def getpolarchive(self,numtoreturn):
        """Get current /POL/ Archive numtoreturn limits the return"""
    
        url = "https://a.4cdn.org/pol/archive.json"
        response = json.loads(requests.get(url).text)[0:numtoreturn]
        threads = [post for post in response]
    
    def getpolpost(self,threadid):
        """Get a Single post from 4Chan by Thread ID"""

        url = f'https://a.4cdn.org/pol/thread/{threadid}.json'
        response = json.loads(requests.get(url).text)
        df = pd.DataFrame(response['posts'])

        def cleancomment(comobj):
            """This function cleans up an HTML String by removing HTML and Characters."""

            try:
                outtxt = ftfy.fix_text(html2text.html2text(comobj).replace('\n',' ').replace('  ',' '))
            except:
                outtxt = comobj

            return outtxt

        df.com = df.com.apply(cleancomment)

        return df
    
    
    def returnlinks(self,numtoreturn):
        """This Function crawls all archived /POL/ Posts and returns links"""

        extractor = URLExtract()
        archives = self.getpolarchive(numtoreturn)

        listofurls = []
        for post in archives:
            try:
                df = self.getpolpost(post)
                comments = [com for com in df.com]

                for com in comments:
                    try:
                        if extractor.find_urls(str(com)):
                            listofurls.append(com)
                    except Exception as e:
                        pass

            except Exception as e:
                pass

        return listofurls
    
    
    
    def returnlargedf(self,numtoreturn):
        """Return a DataFrame with many Posts in it"""
        
        archives = self.getpolarchive(numtoreturn)

        df = pd.DataFrame()

        for post in archives:
            try:
                df = self.getpolpost(post)
                df = df.append()

            except:
                pass
        return df


# This is a Production of the Patriotic Deep State.
# print(f"{chr(21328)}")
