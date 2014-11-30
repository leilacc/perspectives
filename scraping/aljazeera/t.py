from BeautifulSoup import BeautifulSoup
import urllib2
import codecs
import copy
import re
import argparse
import sys
import json 
import wget




def enter(url):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)

    output = "{\"title\": "
    a = soup.find("title")
    output +=  "\"" + a.text + "\",\n"


    b = soup.find("div", {"class": "top-date"})
    output +=  "\"date\": \""+ b.text + "\",\n"

    output +=  "\"article_text\": \""

    c = soup.findAll("p")
    for paragraph in c:
        try:
            output +=  paragraph.text.decode("utf-8").replace("\"","'").replace("^M","").replace("\n","").replace("\\","").replace(r'\r','').replace("\r", "").replace("\n", "")
        except UnicodeEncodeError:
            pass

    output += "\"}\n"
    return output



print enter("http://www.todayszaman.com/diplomacy_ihh-icc-finds-israel-guilty-of-war-crimes-in-mavi-marmara-raid_363650.html")
