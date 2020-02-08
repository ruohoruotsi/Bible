# Scraping

import os
import requests
import urllib.request
import time
from bs4 import BeautifulSoup

root_url = 'https://live.bible.is'

# New Testament Wycliffe Modern Version for English
#language = ['/bible/ENGWMV', '/bible/DDNBIV']

# Bible revised version 1885
#language = ['/bible/ENGREV', '/bible/DDNBIV']

# Bible American Standard Version
language = ['/bible/ENGASV', '/bible/DDNBIV']

book = ['MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL', 'EPH', 'PHP', 'COL',
        '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 'HEB', 'JAS', '1PE', '2PE', '1JN', '2JN',
        '3JN', 'JUD', 'REV']
        
%%time
lines = []
for i in range(len(language)):
    for j in range(len(book)):
        urls = []
        url = root_url + language[i] + "/" + book[j] + "/"
        urls.append(url)
        
        #book_of_nt = []
        for url_item in urls:
            for k in range(1,30): # Set the max number of chapter per book to 30 
                page = url_item + str(k)
                print(page)
                response = requests.get(page)
                if response.url == page :
                    print(response) # display 200 meaning that we successfully access the link
                    soup = BeautifulSoup(response.content, "html.parser")
                    verses = soup.find_all("span", {"class": ""})
                    verses_of_nt = [verse.text for verse in verses]
                    verses_of_nt_prep = verses_of_nt[:-15] # a little preprocessing step
                    #book_of_nt.append(verses_of_nt_prep)

                    with open("DATA/"+language[i][-6:-3]+'.txt', 'a') as file: # specified the name of the file
                        for verse_no, line in enumerate(iterable=verses_of_nt_prep, start=1):
                            file.write("( "+book[j]+" "+str(k)+":" +str(verse_no)+" ), ")
                            if line !="-":
                                file.write(line)
                                lines.append(line) # for further preprocessing steps
                            else:
                                file.write("Interlude")
                                lines.append("Interlude") #for further preprocessing steps
                            file.write('\n')
                            
                else :
                    print("<Response [404]>") # Because links don't overflow we instead get back to square 1
                    break
    print("Youpi! 1 minute break \n",30*"=")
    time.sleep(60)
print("DONE")

# Preprocessing

import pandas as pd
bible = pd.DataFrame({'Language':lines})
bible

bible.to_csv('DATA/data.csv', index=False)

bible.loc[:7956, 'Language'].reset_index(drop=True).tail()

bible.loc[7957:, 'Language'].reset_index(drop=True).tail()

bible_bi = pd.DataFrame({'EN': bible.loc[:7956, 'Language'].reset_index(drop=True),
                         'DDN': bible.loc[7957:, 'Language'].reset_index(drop=True)})
bible_bi

bible_bi_preproc = bible_bi[bible_bi["EN"] != "Interlude"].reset_index(drop=True)

bible_bi.shape, bible_bi_preproc.shape

bible_bi_preproc.head()

bible_bi_preproc.isnull().sum()

bible_bi_preproc[['EN']].to_csv('DATA/dataEN.txt', index=False)

bible_bi_preproc[['DDN']].to_csv('DATA/dataDDN.txt', index=False)

# Manual Preprocessing

- (Mark 9:50-51) a new verse created in ddn version
- (Mark 10:52-53) same remark like above
- (Corinthians 2:13-14) same remark like above
- (John 3:14-15) ddn version has less verse than en version
- (Revelation 12&13:1&2) verse overlap between chapters
#Do not forget to add quotation mark ""

# Is the data aligned now ?
pd.read_csv('DATA/dataDDN.txt').shape,pd.read_csv('DATA/dataEN.txt').shape
