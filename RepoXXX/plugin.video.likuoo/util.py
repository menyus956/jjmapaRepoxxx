import sys, urllib, urllib2, re, gzip, StringIO
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
 
ADDON_ID='plugin.video.javstream' 
UA = 'Mozilla/6.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.5) Gecko/2008092417 Firefox/3.0.3'

def post(url, data, headers={}):
    postdata = urllib.urlencode(data)
    req = urllib2.Request(url, postdata, headers)
    req.add_header('User-Agent', UA)
    response = urllib2.urlopen(req)
    data = response.read()
    response.close()
    return data

def getURL(url, header):
    try:
        req = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(req)
        if response and response.getcode() == 200:
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO.StringIO( response.read())
                gzip_f = gzip.GzipFile(fileobj=buf)
                content = gzip_f.read()
            else:
                content = response.read()
            content = content.decode('utf-8', 'ignore')
            return content
        return False
    except:
        xbmc.log('Error Loading URL '+url, xbmc.LOGERROR)
        xbmc.log('Content: '+response.read(), xbmc.LOGERROR)
        return False

def safeName(name):
    return re.sub(r'[^a-zA-Z0-9 ]','', name.lower()).replace(" ", "_")
  
def stripInvalid(name):
    return re.sub(r'[^a-zA-Z0-9 ]',' ', name.lower())
    
def urlSafe(name):
    return re.sub(r'[^a-zA-Z0-9 ]','', name.lower())
    
def alert(alertText):
    dialog = xbmcgui.Dialog()
    ret = dialog.ok(ADDON_ID, alertText)
    
def error(heading, message):
    dialog = xbmcgui.Dialog()
    dialog.notification(heading, message, xbmcgui.NOTIFICATION_ERROR, 5000)

def progressStart(title, status):
    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create(title, status)
    progressUpdate(pDialog, 1, status)
    return pDialog

def progressStop(pDialog):
    pDialog.close

def progressUpdate(pDialog, progress, status):
    pDialog.update(progress, status)
    
def relevanceCheck(title, animeList):
    returnList=[]
    for anime in animeList:
        if title.lower() in anime.lower():
            returnList.append(anime)
    return returnList

def searchBox() :
    keyb=xbmc.Keyboard('', 'Enter search text')
    keyb.doModal()
    searchText=''
    if (keyb.isConfirmed()) :
        searchText = keyb.getText()
    if searchText!='':
        return searchText
        
def addDir(name,url,mode,iconimage,plot=""):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot": plot} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def playMedia(title, thumbnail, link, mediaType='Video') :
    """Plays a video

    Arguments:
    title: the title to be displayed
    thumbnail: the thumnail to be used as an icon and thumbnail
    link: the link to the media to be played
    mediaType: the type of media to play, defaults to Video. Known values are Video, Pictures, Music and Programs
    """
    
    li = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail, path=link)
    li.setInfo( "video", { "Title" : title } )
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)

def parseParameters(inputString=sys.argv[2]):
    """Parses a parameter string starting at the first ? found in inputString
    
    Argument:
    inputString: the string to be parsed, sys.argv[2] by default
    
    Returns a dictionary with parameter names as keys and parameter values as values
    """
    parameters = {}
    p1 = inputString.find('?')
    if p1 >= 0:
        splitParameters = inputString[p1 + 1:].split('&')
        for nameValuePair in splitParameters:
            if (len(nameValuePair) > 0):
                pair = nameValuePair.split('=')
                key = pair[0]
                value = urllib.unquote(urllib.unquote_plus(pair[1])).decode('utf-8')
                parameters[key] = value
    return parameters

def notify(addonId, message, timeShown=5000):
    """Displays a notification to the user
    
    Parameters:
    addonId: the current addon id
    message: the message to be shown
    timeShown: the length of time for which the notification will be shown, in milliseconds, 5 seconds by default
    """
    addon = xbmcaddon.Addon(addonId)
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (addon.getAddonInfo('name'), message, timeShown, addon.getAddonInfo('icon')))


def showError(addonId, errorMessage):
    """
    Shows an error to the user and logs it
    
    Parameters:
    addonId: the current addon id
    message: the message to be shown
    """
    notify(addonId, errorMessage)
    xbmc.log(errorMessage, xbmc.LOGERROR)

def extractAll(text, startText, endText):
    """
    Extract all occurences of a string within text that start with startText and end with endText
    
    Parameters:
    text: the text to be parsed
    startText: the starting tokem
    endText: the ending token
    
    Returns an array containing all occurences found, with tabs and newlines removed and leading whitespace removed
    """
    result = []
    start = 0
    pos = text.find(startText, start)
    while pos != -1:
        start = pos + startText.__len__()
        end = text.find(endText, start)
        result.append(text[start:end].replace('\n', '').replace('\t', '').lstrip())
        pos = text.find(startText, end)
    return result

def extract(text, startText, endText):
    """
    Extract the first occurence of a string within text that start with startText and end with endText
    
    Parameters:
    text: the text to be parsed
    startText: the starting tokem
    endText: the ending token
    
    Returns the string found between startText and endText, or None if the startText or endText is not found
    """
    start = text.find(startText, 0)
    if start != -1:
        start = start + startText.__len__()
        end = text.find(endText, start + 1)
        if end != -1:
            return text[start:end]
    return None

def request(url, headers={}):
    debug('request: %s' % url)
    req = urllib2.Request(url, headers=headers)
    req.add_header('User-Agent', UA)
    response = urllib2.urlopen(req)
    data = response.read()
    response.close()
    debug('len(data) %s' % len(data))
    return data
    
def debug(text):
    xbmc.log(str([text]), xbmc.LOGDEBUG)
   
def makeLink(params, baseUrl=sys.argv[0]):
    """
    Build a link with the specified base URL and parameters
    
    Parameters:
    params: the params to be added to the URL
    BaseURL: the base URL, sys.argv[0] by default
    """
    return baseUrl + '?' +urllib.urlencode(dict([k.encode('utf-8'),unicode(v).encode('utf-8')] for k,v in params.items()))

def addMenuItem(caption, link, icon=None, thumbnail=None, folder=False):
    """
    Add a menu item to the xbmc GUI
    
    Parameters:
    caption: the caption for the menu item
    icon: the icon for the menu item, displayed if the thumbnail is not accessible
    thumbail: the thumbnail for the menu item
    link: the link for the menu item
    folder: True if the menu item is a folder, false if it is a terminal menu item
    
    Returns True if the item is successfully added, False otherwise
    """
    listItem = xbmcgui.ListItem(unicode(caption), iconImage=icon, thumbnailImage=thumbnail)
    listItem.setInfo(type="Video", infoLabels={ "Title": caption })
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=link, listitem=listItem, isFolder=folder)

def endListing():
    """
    Signals the end of the menu listing
    """
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def addMenuItems(details, show=True, isFolder=True):
    changed=False
    for detail in details:
        try:
            u=sys.argv[0]+"?url="+detail['url']+"&mode="+str(detail['mode'])+"&name="+urllib.quote_plus(detail['title'].encode("utf-8"))+"&icon="+detail['icon']
            liz=xbmcgui.ListItem(detail['title'].encode("utf-8"), iconImage=detail['icon'], thumbnailImage=detail['icon'])
            liz.setInfo(type=detail['type'], infoLabels={ "Title": detail['title'].encode("utf-8"),"Plot": detail['plot']} )
        except:
            u=sys.argv[0]+"?url="+detail['url']+"&mode="+str(detail['mode'])+"&name="+urllib.quote_plus(detail['title']).decode("utf-8")+"&icon="+detail['icon']
            liz=xbmcgui.ListItem(detail['title'].encode("utf-8"), iconImage=detail['icon'], thumbnailImage=detail['icon'])
            liz.setInfo(type=detail['type'], infoLabels={ "Title": detail['title'].decode("utf-8"),"Plot": detail['plot']} )
        
        try:
            u=u+"&extras="+detail["extras"]
        except:
            pass
        try:
            u=u+"&extras2="+detail["extras2"]
        except:
            pass
        try:
            liz.setProperty("Fanart_Image", detail['fanart'])
            u=u+"&fanart="+detail['fanart']
        except:
            pass
        try:
            liz.setProperty("Landscape_Image", detail['landscape'])
            u=u+"&landscape="+detail['landscape']
        except:
            pass
        try:
            liz.setProperty("Poster_Image", detail['poster'])
            u=u+"&poster="+detail['poster']
        except:
            pass
        try:
            if detail['mode']==6:
                dwnld = (sys.argv[0] +
                    "?url=" + urllib.quote_plus(detail['url']) +
                    "&mode=" + str(9) +
                    "&poster="+detail['poster']+
                    "&extras="+detail['extras']+
                    "&download=" + str(1) +
                    "&fanart="+detail['fanart']+
                    "&name=" + urllib.quote_plus(detail['extras2'].encode('utf-8')))
                
                liz.addContextMenuItems([('Download Video', 'xbmc.RunPlugin('+dwnld+')')])
            if detail['mode']==5 and detail['extras']!="44":
                changed=True
                view = (sys.argv[0] +
                    "?url=set-default-view" +
                    "&mode=" + str(10) +
                    "&poster="+detail['poster']+
                    "&fanart="+detail['fanart']+
                    "&extras="+sysarg+
                    "&name=" + "set-default-view")
                #liz.addContextMenuItems([('Set Default View', 'xbmc.RunPlugin('+view+')')])
                save2library = (sys.argv[0] +
                    "?url=" + detail['url'] +
                    "&mode=" + str(11) +
                    "&poster="+detail['poster']+
                    "&fanart="+detail['fanart']+
                    "&extras="+detail["extras"]+
                    "&name=" + urllib.quote_plus(detail['title'].encode("utf-8")))
                save2bookmarks = (sys.argv[0] +
                    "?url=" + detail['url'] +
                    "&mode=" + str(12) +
                    "&poster="+detail['poster']+
                    "&fanart="+detail['fanart']+
                    "&extras="+detail["extras"]+
                    "&name=" + urllib.quote_plus(detail['title'].encode("utf-8")))
                liz.addContextMenuItems([('Set default view', 'xbmc.RunPlugin('+view+')'), ('Add to library', 'xbmc.RunPlugin('+save2library+')'), ('Add to JAVStream favourites', 'xbmc.RunPlugin('+save2bookmarks+')')])
            elif detail['mode']==5 and detail['extras']=="44":
                changed=True
                view = (sys.argv[0] +
                    "?url=set-default-view" +
                    "&mode=" + str(10) +
                    "&poster="+detail['poster']+
                    "&fanart="+detail['fanart']+
                    "&extras="+sysarg+
                    "&name=" + "set-default-view")
                #liz.addContextMenuItems([('Set Default View', 'xbmc.RunPlugin('+view+')')])
                save2library = (sys.argv[0] +
                    "?url=" + detail['url'] +
                    "&mode=" + str(11) +
                    "&poster="+detail['poster']+
                    "&fanart="+detail['fanart']+
                    "&extras="+detail["extras"]+
                    "&name=" + urllib.quote_plus(detail['title'].encode("utf-8")))
                deletebookmarks = (sys.argv[0] +
                    "?url=" + detail['url'] +
                    "&mode=" + str(14) +
                    "&poster="+detail['poster']+
                    "&fanart="+detail['fanart']+
                    "&extras="+"single-delete"+
                    "&name=" + urllib.quote_plus(detail['title'].encode("utf-8")))
                liz.addContextMenuItems([('Set default view', 'xbmc.RunPlugin('+view+')'), ('Add to library', 'xbmc.RunPlugin('+save2library+')'), ('Remove from JAVStream favourites', 'xbmc.RunPlugin('+deletebookmarks+')')])
        except:
            pass
        try:
            if detail["extras"]=="force-search" and detail["extras2"]=="db-search":
                dwnld = (sys.argv[0] +
                    "?url=" + urllib.quote_plus(detail['url']) +
                    "&mode=" + str(31) +
                    "&poster="+detail['poster']+
                    "&extras="+"single-delete"+
                    "&fanart="+detail['fanart']+
                    "&name=" + urllib.quote_plus(detail['title'].encode('utf-8')))
                liz.addContextMenuItems([('Delete Search Term', 'xbmc.RunPlugin('+dwnld+')')])
        except:
            pass
        #addContextItem(liz, "Add to favourites","special://home/addons/plugin.video.javstream2/addFavourite.py", "id=909722")
        #addContextItem(liz, "Add idol to favourites","special://home/addons/plugin.video.javstream2/addFavouriteIdol.py", "id=909722")
        if isFolder:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            liz.setProperty('IsPlayable', 'true')
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    if show:
        if changed==True:
            xbmc.executebuiltin('Container.SetViewMode(%d)' % int(xbmcplugin.getSetting(int(sysarg), "vidview")))
        xbmcplugin.endOfDirectory(int(sysarg))