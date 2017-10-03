import util, urllib2, re, urllib, base64, difflib, time, json, HTMLParser, requests
import xbmcaddon,xbmcplugin,xbmcgui

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
       
ADDON_ID='plugin.video.likuoo'

sysarg=str(sys.argv[1]) 

# This function implements a horrible hack related to python 2.4's terrible unicode handling.
def makeAscii(data):
    #log(repr(data), 5)
    #if sys.hexversion >= 0x02050000:
    #        return data

    try:
        return data.encode('ascii', "ignore")
    except:
        #log("Hit except on : " + repr(data))
        s = u""
        for i in data:
            try:
                i.encode("ascii", "ignore")
            except:
                #log("Can't convert character", 4)
                continue
            else:
                s += i

        #log(repr(s), 5)
        return s

def replaceHTMLCodes(txt):
    #log(repr(txt), 5)

    # Fix missing ; in &#<number>;
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", makeUTF8(txt))

    txt = HTMLParser.HTMLParser().unescape(txt)
    txt = txt.replace("&amp;", "&")
    #log(repr(txt), 5)
    return txt

# This function handles stupid utf handling in python.
def makeUTF8(data):
    #log(repr(data), 5)
    return data
    try:
        return data.decode('utf8', 'xmlcharrefreplace') # was 'ignore'
    except:
        #log("Hit except on : " + repr(data))
        s = u""
        for i in data:
            try:
                i.decode("utf8", "xmlcharrefreplace") 
            except:
                #log("Can't convert character", 4)
                continue
            else:
                s += i
        #log(repr(s), 5)
        return s
        
def getVids(params) :
    param={}
    #del param['search']
    
    url=params['url']
    try:
        url=url+"&page="+params['page']
    except:
        pass
        
    content=util.getURL(url, hdr)
    if content!=False:
        films=util.extractAll(content, '<div class="item">', '<div class="item">')
        for film in films:
            param['title']=makeAscii(util.extract(film, 'title="', '"'))
            param['url']=util.extract(film, '<a href="', '" title="')
            param['poster']=util.extract(film, 'src="', '" title="')
            param['fanart']=param['poster']
            if param['url']!=None:
                u=sys.argv[0]+"?url="+param['url']+"&mode=5&name="+urllib.quote_plus(param['title'])+"&poster="+param['poster']
                liz=xbmcgui.ListItem(param['title'], iconImage="DefaultVideo.png", thumbnailImage=param['poster'])
                liz.setInfo( type="Video", infoLabels={ "Title": param['title'],"Plot": ""} )
                liz.setProperty("Poster_Image", param['poster'])
                liz.setProperty('IsPlayable', 'true')
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        
        next=util.extract(content, '<span class="current">', '</span>')
        
        if next!=None:
            if ">"+str(next)+"</span>" in content:
                prev=util.extract(content, '<span class="current">', '</a>')
                next=util.extract(prev, 'a href="', '"')
                if "likuoo.video" not in next:
                    next="http://likuoo.video"+next
                    
                u=sys.argv[0]+"?url="+next+"&mode=2&name=Next"
                liz=xbmcgui.ListItem("Next >", iconImage="DefaultNext.png", thumbnailImage=param['poster'])
                liz.setProperty('IsPlayable', 'false')
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        xbmcplugin.endOfDirectory(int(sysarg))

def buildMainMenu():
    util.addDir("Latest","http://www.likuoo.video/", 2, "","")
    util.addDir("Categories","http://www.likuoo.video/", 3, "","")
    util.addDir("Search","Search", 4, "","")
    xbmcplugin.endOfDirectory(int(sysarg))
    
def search():
    term=util.searchBox()
    if term:
        params={'search':1}
        params['url']="http://www.likuoo.video/search/?s="+urllib.quote_plus(term)
        getVids(params)

def getCategories(url):
    param={'category':1}
    content=util.getURL(url, hdr)
    if content!=False:
        cats=util.extractAll(content, '<div class="item">', '<div class="item">')
        for film in cats:
            param['title']=makeAscii(util.extract(film, 'title="', '"'))
            param['url']='http://www.likuoo.video'+util.extract(film, '<a href="', '" title="')
            param['poster']=util.extract(film, 'src="', '" title="')
            param['fanart']=param['poster']
            xbmc.log("Play URL:"+param['url'], xbmc.LOGERROR)
            if param['url']!=None:
                u=sys.argv[0]+"?url="+param['url']+"&mode=2&name="+urllib.quote_plus(param['title'])+"&poster="+param['poster']
                liz=xbmcgui.ListItem(param['title'], iconImage="DefaultVideo.png", thumbnailImage=param['poster'])
                liz.setInfo( type="Video", infoLabels={ "Title": param['title'],"Plot": ""} )
                liz.setProperty("Poster_Image", param['poster'])
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        xbmcplugin.endOfDirectory(int(sysarg))
                
def playVideo(params):
    #xbmc.log(str(params), xbmc.LOGERROR)
    content=util.getURL(params['url'], hdr)
    if content!=False:
        url=util.extract(content, 'id="post_in', '</div>')
        url=util.extract(url, 'src="', ' ')
        
        if "?v" in url:
            v=util.extract(url, "v=", '"')
            payload={"v":v, "t":"1"}
            url="http://www.likuoo.video/load.php"
            
            r=requests.post(url, data=payload)
            
            
            urls=util.extractAll(r.text, "<source", "/>")
            
            for source in urls:
                url=util.extract(source, 'src="', '"')
                break
        else:
            url=util.extract(url, "?x=", '"')
            url=base64.b64decode(url)
        
    util.playMedia(params['name'], params['poster'], url, "Video")

parameters=util.parseParameters()
try:
    mode=int(parameters["mode"])
except:
    mode=None
    
if mode==2:
    getVids(parameters)
elif mode==3:
    getCategories('http://www.likuoo.video/all-channels/')
elif mode==4:
    # search code goes here!!
    search()
elif mode==5:
    playVideo(parameters)
else :
    buildMainMenu()
