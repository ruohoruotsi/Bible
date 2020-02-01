import os
import requests
import urllib.request
import time
from bs4 import BeautifulSoup

root_url = 'https://live.bible.is'

# New Testament Wycliffe Modern Version for English
#language = ['/bible/ENGWMV', '/bible/DDNBIV']

# New Testament English Standard Version
language = ['/bible/EN1ESV', '/bible/DDNBIV']

book = ['MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL', 'EPH', 'PHP', 'COL',
        '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 'HEB', 'JAS', '1PE', '2PE', '1JN', '2JN',
        '3JN', 'JUD', 'REV']
        
for i in range(len(language)):
    for j in range(len(book)):
        urls = []
        url = root_url + language[i] + "/" + book[j] + "/"
        urls.append(url)
        
        #book_of_nt = []
        for url_item in urls:
            for k in range(1,30): #the max num represent the number of chapter we could have in a book
                page = url_item + str(k)
                print(page)
                response = requests.get(page)
                if response.url == page :
                    print(response)
                    soup = BeautifulSoup(response.content, "html.parser")
                    verses = soup.find_all("span", {"class": ""})
                    verses_of_nt = [verse.text for verse in verses]
                    verses_of_nt_prep = verses_of_nt[:-15] # a little preprocessing step
                    #book_of_nt.append(verses_of_nt_prep)

                    with open( language[i][-6:-3]+".txt", 'a') as file: #specified the name of the file
                        for line in verses_of_nt_prep:
                            file.write(line)
                            file.write('\n')
                else :
                    print("<Response [404]>")
                    break
  
