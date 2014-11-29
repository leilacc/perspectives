
import urllib2
import urllib


Headers = {'User-agent': 'Mozilla/5.0'}
req  = urllib2.Request("http://www.nytimes.com/2014/11/07/world/europe/hague-prosecutor-cites-possible-israeli-war-crimes-but-declines-to-seek-inquiry-in-gaza-flotilla-raid.html", headers=Headers)
    
res  = urllib2.urlopen(req)
print res.read()
