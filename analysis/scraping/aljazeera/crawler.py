import analysis
from BeautifulSoup import BeautifulSoup
import urllib2
import codecs
import copy
import re
import argparse
import sys
import json 
import wget
from get_query import get_keyword

def cnn(url):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    a = soup.find("title")
    k = a.text.split("-")
    title = k[0]
    date = k[1]
    output = ""
    output +=  "{\"title\": \"" + title + "\",\n"

    output +=  "\"date\": \""+ date + "\",\n"

    output +=  "\"article_text\": \""


    c = soup.findAll("p")
    for paragraph in c:
        try:
            output +=  paragraph.text.decode("utf-8").replace("\"","'") + " "
        except UnicodeEncodeError:
            pass
    output += "\"}"
    return output

def timesofisrael(url):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    output = "{\"title\": "
    a = soup.find("title")
    output +=  "\"" + a.text + "\",\n"


    b = soup.find("span", {"class": "date"})
    output +=  "\"date\": \""+ b.text + "\",\n"

    output +=  "\"article_text\": \""

    c = soup.findAll("p", {"itemprop": "articleBody"})
    for paragraph in c:
        try:
            output +=  paragraph.text.decode("utf-8").replace("\"","'") + " "
        except UnicodeEncodeError:
            pass

    output += "\"}\n"
    return output


def jpost(url):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    output = "{\"source\": \"" + "The Jerusalem Post" + "\",\n"
    output += "\"url\": \"" + url + "\",\n"
    output += "\"title\": "
    a = soup.find("title")
    output +=  "\"" + a.text + "\",\n"
   

    b = soup.find("p", {"class": "article-date-time"})

    date = b.text

#    11/06/2014 10
    arr = date.split(" ")[0]
    arr2 = arr.split("/")
    
    date = arr2[0] + "/" + arr2[1] + "/" + arr2[2][2:]
    
    
    output +=  "\"date\": \""+ date + "\",\n"

    output +=  "\"article_text\": \""
    
    c = soup.findAll("p")
    for paragraph in c:
        try:
            output +=  paragraph.text.decode("utf-8").replace("\"","'").replace("^M","").replace("\n","").replace("\\","").replace(r'\r','').replace("\r", "").replace("\n", "") + "  "
        except UnicodeEncodeError:
            pass

    output += "\"}\n"

    return ''.join([i if ord(i) < 128 else ' ' for i in output])



def aljazeera(url):
    with open(url) as f:
        content = f.readlines()
    a = ""
    for line in content:
        a += line + " "
    soup = BeautifulSoup(a)
    c = soup.findAll("a", {"ctype": "c"})
    arr = []
    for paragraph in c:
#        print paragraph
        j =  paragraph['href']
        arr.append(j)
    url1 = arr[0]
    url2 = arr[1]
    return [url1,url2]


def aljazeera2(url):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    output = ""
    a = soup.find("title")
    title = a.text
    output = "{\"source\": \"" + "Al Jazeera" + "\",\n"
    output += "\"url\": \"" + url + "\",\n"
    output +=  "\"title\": \"" + title + "\",\n"
    c = soup.find("span", {"id": "ctl00_cphBody_lblDate"})
    
    date = c.text
#    06 Nov 2014 14:09
    arr = date.split(" ")
    month = arr[1]
    y = arr[2][2:]
    m = 0
    d = arr[0]
    if month == "Jan":
        m = 1
    elif month == "Feb":
        m = 2
    elif month == "Mar":
        m =3
    elif month == "Apr":
        m = 4
    elif month == "May":
        m = 5
    elif month == "Jun":
        m = 6
    elif month == "Jul":
        m = 7
    elif month == "Aug":
        m = 8
    elif month == "Sep":
        m = 9
    elif month == "Oct":
        m = 10
    elif month == "Nov":
        m = 11
    elif month == "Dec":
        m = 12
    date = str(m) + "/" + d + "/" + y
    output +=  "\"date\": \""+ date + "\",\n"
    output +=  "\"article_text\": \""

    c = soup.findAll("p")
    for paragraph in c:
        try:
            output +=  paragraph.text.decode("utf-8").replace("\"","'").replace("\n","") + " "
        except UnicodeEncodeError:
            pass
    output += "\"}\n"
    return output
    


def nytimes(url):
    response = urllib2.urlopen(url)
    data = json.load(response)
    u = data["response"]["docs"][0]["web_url"]
    headline = data["response"]["docs"][0]["headline"]["main"]
    date = data["response"]["docs"][0]["pub_date"]
    arr = date.split("-") #2014-11-05T16:21:48Z"
    day = arr[2][:2]
    month = arr[1]
    year = arr[0][2:]
   
    output = "{\"source\": \"" + "The New York Times" + "\",\n"
    output +="\"url\": \"" + u + "\",\n"
    output +=  "\"title\": \"" + headline + "\",\n"
    d = month + "/" + day + "/" + year
    output +=  "\"date\": \""+ d + "\",\n"
#    new_u = u.replace("www","mobile")
 #   filename = wget.download("http://apple.com")
    
    with open("hard_coded_input/nytimes.html") as f:
        content = f.readlines()
    str = ""
    for line in content:
        str+= line + " "
    soup = BeautifulSoup(str)
    output +=  "\"article_text\": \""
    c = soup.findAll("p",{"class":"story-body-text story-content"})
    for paragraph in c:
        try:
            output +=  paragraph.text.decode("utf-8").replace("\"","'") + " "
        except UnicodeEncodeError:
            pass
    output += "\"}\n"
    return output


def zamandaily(url):   
    with open(url) as f:
        content = f.readlines()
    a = ""
    for line in content:
        a += line + " "

    soup = BeautifulSoup(a)
    output = "{\"source\": \"" + "Zaman Daily" + "\",\n"
    output += "\"url\": \"" + "http://www.todayszaman.com/diplomacy_ihh-icc-finds-israel-guilty-of-war-crimes-in-mavi-marmara-raid_363650.html" + "\",\n"
    output += "\"title\": "
    a = soup.find("title")
    
    output +=  "\"" + a.text + "\",\n"
  

    b = soup.find("div", {"class": "topDate"})
    #November 30, 2014, Sunday
    date = b.text
    arr = date.split(" ")

    month = arr[0]
    day = arr[1].strip(",")
    year = arr[2].strip(",")[2:]

    if month == "January":
        m = 1
    elif month == "February":
        m = 2
    elif month == "March":
        m =3
    elif month == "April":
        m = 4
    elif month == "May":
        m = 5
    elif month == "June":
        m = 6
    elif month == "July":
        m = 7
    elif month == "August":
        m = 8
    elif month == "September":
        m = 9
    elif month == "October":
        m = 10
    elif month == "November":
        m = 11
    elif month == "December":
        m = 12

    d = str(m) + "/" + day + "/" + year
    output +=  "\"date\": \""+ d + "\",\n"

    output +=  "\"article_text\": \""
    
    c = soup.findAll("p")
    for paragraph in c:
        try:
            output +=  paragraph.text.decode("utf-8").replace("\"","'").replace("^M","").replace("\n","").replace("\\","").replace(r'\r','').replace("\r", "").replace("\n", "") + " " 
        except UnicodeEncodeError:
            pass

    output += "\"}\n"
    return ''.join([i if ord(i) < 128 else ' ' for i in output])
#    return output






def main(line):
    if "timesofisrael.com" in line:
        print timesofisrael(line)
    elif "cnn" in line:
        print cnn(line)
    elif "zaman" in line:
 
        o =  zamandaily(line)
        return o
    elif "jpost" in line:
 
        o =  jpost(line)
        return o
        
    elif "http" not in line or ".com" not in line or "hard_coded" not in line: #input is key words, do search in aljazeera and ny times
        queries = line.split(" ")
        out = ""
        for q in queries:
            out += q + "%20"
        out = out[:-3]
        url = "http://www.aljazeera.com/Services/Search/?q=" + out.strip("\n")
    
        #arr = aljazeera(url)
        #hardcodedinput starts here
        arr = aljazeera("hard_coded_input/aljazeera_search.html")  
    #ended here


        u = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=" + out.strip("\n") + "&api-key=5dd8c298ba4af00cbd64648848f8b228:11:70247711"
        
        return aljazeera2(arr[0]) + "," + aljazeera2(arr[1]) + "," + nytimes(u)


#python crawler.py "http://www.jpost.com/Israel-News/ICC-rejects-pro-Turkey-war-crimes-allegations-against-IDF-in-Gaza-flotilla-raid-380955"
#python get_query.py > title.out #gets keyword from title
#python crawler.py title.out #gets title from url,pipes it into aljazeera and nytimes
#python crawler.py "hard_coded_input/zamandaily.html" #looks at todays zaman
line = sys.argv[1]
jpost_output = main(line)
keywords = get_keyword(jpost_output)
other_output = main(keywords)
zaman_output = main("hard_coded_input/zamandaily.html")

def combine_output(zaman_output,other_output,jpost_output):
    a =  "{\"results\": {\"news_sources\": ["
    a += jpost_output + other_output + "," + zaman_output
    a +=  "]}}"
    return a

j = combine_output(zaman_output,other_output,jpost_output)


results = analysis.differential(j)
print results

