from BeautifulSoup import BeautifulSoup
import urllib2
import codecs
import copy
import re
import argparse
import sys


import json

with open('output.json') as data_file: 
    data = json.load(data_file)

query = data["title"]


line = sys.argv[1]


response = urllib2.urlopen(line)
html = response.read()

soup = BeautifulSoup(html)
def cnn(url):
    a = soup.find("title")
    k = a.text.split("-")
    title = k[0]
    date = k[1]
    output = ""
    output +=  "{\"title\": \"" + title + "\",\n"


    output +=  "\"date\": \""+ date + "\",\n"

    output +=  "\"article_text:\": \""


    c = soup.findAll("p")
    for paragraph in c:
        try:
            output +=  paragraph.text.decode("utf-8")
        except UnicodeEncodeError:
            pass
    output += "\"}"
    return output

def timesofisrael(url):
    a = soup.find("title")
    output +=  "\"" + a.text + "\",\n"


    b = soup.find("span", {"class": "date"})
    output +=  "\"date\": \""+ b.text + "\",\n"

    output +=  "\"article_text:\": \""

    c = soup.findAll("p", {"itemprop": "articleBody"})
    for paragraph in c:
        try:
            output +=  paragraph.text.decode("utf-8")
        except UnicodeEncodeError:
            pass

    output += "\"}\n"
    return output







if "timesofisrael.com" in line:
    print timesofisrael(line)
elif "cnn" in line:
    print cnn(line)
elif "aljazeera" in line:
    print aljazeera(line)
