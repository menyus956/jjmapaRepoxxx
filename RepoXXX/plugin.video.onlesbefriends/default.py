'''
These addons are only possible because websites are open and allow us to view them for free.

These addons are also only possible due to the numerous hours the kodi developers and addon developers put in to ensure that
you, the user can have as much content as you need.

However, it is incredibly clear that numerous people exist to take content and pass it off as their own. PLEASE do not do that
if you are going to borrow code, then please ensure you credit those involved.

Author: oneil from Ninjasys - @oneilxm_uk / Golaith_Evolve
Git: github.com/Goliath-Evolve
Addon: Les-Be-Friends
Thank you / Acknowledgement: Those that exist in the Kodi telegram groups & Kodification for clean_name.py, ][ for his lack of help, Dandymedia for his insight.
'''

import sys, os, xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib, urllib2, cookielib, re, clean_name

settings = xbmcaddon.Addon(id='plugin.video.onlesbefriends')
cookiejar = cookielib.LWPCookieJar()
cookie_handler = urllib2.HTTPCookieProcessor(cookiejar)
opener = urllib2.build_opener(cookie_handler)
addon_id = 'plugin.video.onlesbefriends'
selfAddon = xbmcaddon.Addon(id=addon_id)
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))

def CATEGORIES():
    link = openURL('http://www.lesbianpornvideos.com/')
    match = re.compile('<li><a href=\"http://www.lesbianpornvideos.com/videos/lesbian/(.*?)\" >(.*?)<br><img src=\"(.*?)\" alt=').findall(link)
    for caturl, name, img in match:
        addDir(name, 'http://www.lesbianpornvideos.com/videos/lesbian/'+ caturl, 1, img, 1)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def VIDEOLIST(url):
    pg = 'http://www.lesbianpornvideos.com/'
    link = openURL(url)
    match = re.compile('<a href=\"http://www.lesbianpornvideos.com/click/.*/video/(.*?)\" class="thumb-img"><img src=\"(.*?)\" width=.* alt=\"(.*?)\"').findall(link)
    for ucode, img, name in match:
        addLink('[COLOR red]'+name+'[/COLOR]','http://www.lesbianpornvideos.com/video/'+ ucode, 2, img)
    next = re.compile('<div class=\"pagination\">.*<a href="([^"]*)\">.+?</a>.+?</div>',re.DOTALL).findall(link)
    for item in next:
        if url[-1] in '0123456789':
            url3 = url[:-1]+item
        else:
            url3 = item
        #addDir('Next Page',url3,1,icon,'')


def PLAYVIDEO(url):
    Dialog = xbmcgui.Dialog()
    sources = []
    link = openURL(url)
    match = re.compile('\{.*file\: \"(.*?)\"\,.*label\: \"720p HD\"\,', re.DOTALL).findall(link)
    for playlink in match:
        isFolder=False
        xbmc.Player().play(playlink)


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params)-1] == '/'):
            params = params[0:len(params)-2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


def addLink(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode)\
        + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="icon.png",
                           thumbnailImage=iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz, isFolder=False)
    return ok


def addDir(name, url, mode, iconimage, page):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) +\
        "&name=" + urllib.quote_plus(name) + "&page=" + str(page)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="icon.png",
                           thumbnailImage=iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz, isFolder=True)
    return ok


def openURL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link


def main():
    params = get_params()
    url = None
    name = None
    mode = None
    page = 1

    try:
        url = urllib.unquote_plus(params["url"])
    except:
        pass
    try:
        name = urllib.unquote_plus(params["name"])
    except:
        pass
    try:
        mode = int(params["mode"])
    except:
        pass
    try:
        page = int(params["page"])
    except:
        pass

    if mode == None or url == None or len(url) < 1:
        CATEGORIES()

    elif mode == 1:
        xbmc.log("VIDEOLIST " + url)
        xbmc.log("VIDEOLIST " + str(page))
        VIDEOLIST(url)

    elif mode == 2:
        xbmc.log("PLAYVIDEO ")
        PLAYVIDEO(url)


if __name__ == "__main__":
    main()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
