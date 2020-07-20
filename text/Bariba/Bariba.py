import os

import requests
import urllib.request
import time
from bs4 import BeautifulSoup

root_url = 'https://live.bible.is'

# New Testament Wycliffe Modern Version for English
#language = ['/bible/ENGASV', '/bible/BBABSB']

# Bible revised version 1885
#language = ['/bible/ENGASV', '/bible/BBABSB']

# Bible American Standard Version
language = ['/bible/ENGASV', '/bible/BBABSB']

# The bible (old + new testament)
book = ["GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT", "1SA", "2SA", "1KI", "2KI",
        "1CH", "2CH", "EZR", "NEH", "EST", "JOB", "PSA", "PRO", "ECC", "SNG", "ISA", "JER",
        "LAM", "EZK", "DAN", "HOS", "JOL", "AMO", "OBA", "JON", "MIC", "NAM", "HAB", "ZEP",
        "HAG", "ZEC", "MAL",'MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL',
        'EPH', 'PHP', 'COL','1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 'HEB', 'JAS', '1PE',
        '2PE', '1JN', '2JN','3JN', 'JUD', 'REV']

# new testament book
#book = ['MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL', 'EPH', 'PHP', 'COL',
#        '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 'HEB', 'JAS', '1PE', '2PE', '1JN', '2JN',
#        '3JN', 'JUD', 'REV']

# old testament book
#book = ["GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT", "1SA", "2SA", "1KI", "2KI",
#        "1CH", "2CH", "EZR", "NEH", "EST", "JOB", "PSA", "PRO", "ECC", "SNG", "ISA", "JER",
#        "LAM", "EZK", "DAN", "HOS", "JOL", "AMO", "OBA", "JON", "MIC", "NAM", "HAB", "ZEP",
#        "HAG", "ZEC", "MAL"]

%%time
lines = []
for i in range(len(language)):
    for j in range(len(book)):
        urls = []
        url = root_url + language[i] + "/" + book[j] + "/"
        urls.append(url)
        
        #book_of_nt = []
        for url_item in urls:
            for k in range(1,300): # Set the max number of chapter per book to 300 
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

#Preprocessing

import pandas as pd
bible = pd.DataFrame({'Language':lines})
bible

bible.to_csv('DATA/data.csv', index=False)

# add some codes here

# Manual Preprocessing

# add some comments here

# Is the data aligned now ?
pd.read_csv('DATA/dataDDN.txt').shape,pd.read_csv('DATA/dataEN.txt').shape
