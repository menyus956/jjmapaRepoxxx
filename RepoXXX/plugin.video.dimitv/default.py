import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs, json, urlparse
import shutil
import urllib2,urllib
import re
import extract
import downloader
import time
import zipfile
import ntpath
from resources.modules import skinSwitch , backuprestore


addon_id = 'plugin.video.dimitv'
ADDON = xbmcaddon.Addon(id=addon_id)
AddonID='plugin.video.dimitv'
AddonTitle="[COLOR purple]Dimitrology TV[/COLOR] [COLOR white]Wizard[/COLOR]"
dialog       =  xbmcgui.Dialog()
HOME         =  xbmc.translatePath('special://home/')
HOME_ADDONS      =  xbmc.translatePath('special://home/addons')
dp           =  xbmcgui.DialogProgress()
U = ADDON.getSetting('userlist')
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
DBPATH = xbmc.translatePath('special://database')
TNPATH = xbmc.translatePath('special://thumbnails');

skin         =  xbmc.getSkinDir()
EXCLUDES     = ['backupdir','plugin.video.dimitv','script.module.addon.common','backup','backup.zip','Database','plugin.video.salts']
packagedir    =  xbmc.translatePath(os.path.join('special://home/addons/packages',''))
ARTPATH      =  '' + os.sep
UPDATEPATH     =  xbmc.translatePath(os.path.join('special://home/addons',''))
UPDATEADPATH	=  xbmc.translatePath(os.path.join('special://home/userdata/addon_data',''))
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
MEDIA        =  xbmc.translatePath(os.path.join('special://home/media',''))
AUTOEXEC     =  xbmc.translatePath(os.path.join(USERDATA,'autoexec.py'))
AUTOEXECBAK  =  xbmc.translatePath(os.path.join(USERDATA,'autoexec_bak.py'))
ADDON_DATA   =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
PLAYLISTS    =  xbmc.translatePath(os.path.join(USERDATA,'playlists'))
DATABASE     =  xbmc.translatePath(os.path.join(USERDATA,'Database'))
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons',''))
CBADDONPATH  =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'default.py'))
GUISETTINGS  =  os.path.join(USERDATA,'guisettings.xml')
GUI          =  xbmc.translatePath(os.path.join(USERDATA,'guisettings.xml'))
GUIFIX       =  xbmc.translatePath(os.path.join(USERDATA,'guifix.xml'))
INSTALL      =  xbmc.translatePath(os.path.join(USERDATA,'install.xml'))
FAVS         =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE       =  xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED     =  xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
PROFILES     =  xbmc.translatePath(os.path.join(USERDATA,'profiles.xml'))
RSS          =  xbmc.translatePath(os.path.join(USERDATA,'RssFeeds.xml'))
KEYMAPS      =  xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))
notifyart    =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'resources/'))
skin         =  xbmc.getSkinDir()


zip = 'special://home/addons/plugin.video.dimitv'





dialog = xbmcgui.Dialog()
urlupdate =  ""
updatename =  "elitetv_update"
backupdir    =  xbmc.translatePath(os.path.join('special://home/backupdir',''))
mybackuppath =  xbmc.translatePath(os.path.join('special://home',''))
EXCLUDESDATA    = ['guisettings.xml','backupdir','favourites.xml', 'sources.xml' , 'Thumbnails', 'guisettings.xml','backup','backup.zip','Database']
INCLUDEGUI = ['guisettings.xml', 'favourites.xml']
SKINSHORTCUTS = ['script.skinshortcuts']
CHECKVERSION  =  os.path.join(USERDATA,'version.txt')

EXCLUDES_ADDONS  = ['notification','packages']


backup_zip = xbmc.translatePath(os.path.join(backupdir,'backup_addon_data.zip'))
backup_fav = xbmc.translatePath(os.path.join(backupdir,'backup_fav.zip'))

installed_build = ''
if not os.path.exists(CHECKVERSION):
		file = open(CHECKVERSION,'w') 
		file.write("<version>None</version>")
		file.close()
vers = open(CHECKVERSION, "r")
regex = re.compile(r'<version>(.+?)</version>')



path   = xbmcaddon.Addon().getAddonInfo('path').decode("utf-8")
logfile = xbmcvfs.File(os.path.join(path, 'changelog.txt'))
text = logfile.read()
logfile.close()


myAddon = xbmcaddon.Addon(id='plugin.video.dimitv')
download_location = myAddon.getSetting('download_path')
download_path = unicode(download_location)

backgrounds_location = myAddon.getSetting('backgrounds_path')

def SETTINGS():
	xbmcaddon.Addon(id='plugin.video.dimitv').openSettings()
  
	
def REFRESHALL():
   
    # dialog.ok("BACKUP/RESTORE", "FORCE CLOSE/RESTART YOUR KODI", "","")
  killxbmc()
 
	
#Root menu of addon
def INDEX():
	if not os.path.exists(CHECKVERSION):
			file = open(CHECKVERSION,'w') 
			file.write("<version>None</version>")
			file.close()
	if not os.path.exists(packagedir): os.makedirs(packagedir)
	dialog = xbmcgui.Dialog()
	for line in vers:
		currversion = regex.findall(line)
		for vernumber in currversion:
			installed_build = vernumber
			
	try:
		url = "http://dimitrology.com/wizard.php?action=getstats&user=%s" % (U)
		link=OPEN_URL(url)
	except: pass
	try:
		data = json.loads(link)
	except: pass
	try: 
		for entry in data:
			
			status = entry['status']
			print status
			if int(status) > 0:
				status = '[COLOR gold]Elite[/COLOR]'
			else: 
				status = 'Free'
			
			addDir('[B]INSTALLED BUILD = [/B]' + '[COLOR lime]' + installed_build + '[/COLOR]','',1,ICON,FANART,'')
			addDir('[B]Account type = [/B]' + status,'',1,ICON,FANART,'')
			

	except:pass
	if not os.path.exists(backupdir):os.makedirs(backupdir)
# #### TEST#####
	# addLink('[COLOR red][B]TEST[/B][/COLOR]','url',600,ART+'freshstart.png',FANART,'')

	addLink('[COLOR red][B]FRESH START[/B][/COLOR]','url',6,ART+'freshstart.png',FANART,'')
	addDir('[COLOR lime][B]Install/Update[/B][/COLOR]','url',20,ART+'builds.png',FANART,'')
	addLink('[COLOR white][B]Settings[/B][/COLOR]','url',100,ART+'settings.png',FANART,'')
	addLink('[COLOR white][B]Backup/Restore[/B][/COLOR]','url',112,ART+'settings.png',FANART,'')
	
	addLink('[COLOR red][B]Enable All Addons[/B][/COLOR]  (Kodi 17 fix)','url',101,ART+'eye.png',FANART,'')
	addLink('[COLOR cyan][B]Get the code[/B][/COLOR]  [COLOR cyan] Visit http://dimitrology.com/getcode [/COLOR]','url',0,ART+'code.png',FANART,'')
		
		
def ENABLE_ADDONS():
	for root, dirs, files in os.walk(HOME_ADDONS,topdown=False):
		dirs[:] = [d for d in dirs]
		for addon_name in dirs:
				if not any(value in addon_name for value in EXCLUDES_ADDONS):
					# addLink(addon_name,'url',100,ART+'tool.png',FANART,'')
					try:
						query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}, "id":1}' % (addon_name)
						xbmc.executeJSONRPC(query)			
						
					except:
						pass
	dialog.ok("All Addons Are Enabled..", "All Addons Are Enabled... Please restart Kodi to make sure the settings will be applied correctly")
			# addLink(addon_name,'url',101,ART+'tool.png',FANART,'')
			
def ENABLE_ADDONS_SILENT():
	for root, dirs, files in os.walk(HOME_ADDONS,topdown=False):
		dirs[:] = [d for d in dirs]
		for addon_name in dirs:
				if not any(value in addon_name for value in EXCLUDES_ADDONS):
					# addLink(addon_name,'url',100,ART+'tool.png',FANART,'')
					try:
						query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}, "id":1}' % (addon_name)
						xbmc.executeJSONRPC(query)			
						
					except:
						pass
						
def ENABLE_WIZARD():
	try:
		query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}, "id":1}' % (addon_id)
		xbmc.executeJSONRPC(query)			
						
	except:
		pass		
	
	
def BACKUP_FAVOURITES():
    if os.path.exists(os.path.join(USERDATA,'favourites.xml')):
       to_backup = xbmc.translatePath(os.path.join('special://','home/userdata'))	
       rootlen = len(to_backup)
       zipobj = zipfile.ZipFile(backup_fav , 'w', zipfile.ZIP_DEFLATED)
       fn = os.path.join(USERDATA, 'favourites.xml')
       dp.create("BACKUP/RESTORE","Backing Up Favourites",'', 'Please Wait')
       zipobj.write(fn, fn[rootlen:])
       dp.close()
	   
def RESTOREFAV():
 if os.path.exists(os.path.join(backupdir,'backup_fav.zip')):
			import time
			dialog = xbmcgui.Dialog()

			
			addonfolder = xbmc.translatePath(os.path.join('special://','home/userdata'))
			time.sleep(2)
			dp.create("[COLOR=blue][B][/B][/COLOR]","Restoring",'', 'Please Wait')

			extract.all(backup_fav,addonfolder,dp)
			dp.close()
			
			
def ARCHIVE_CB(sourcefile, destfile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
    zipobj = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(sourcefile)
    for_progress = []
    ITEM =[]
    dp = xbmcgui.DialogProgress()
    dp.create(message_header, message1, message2, message3)
    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(sourcefile):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f not in exclude_files]
        for file in files:
            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(int(progress),"Backing Up",'[COLOR lime]%s[/COLOR]'%file, 'Please Wait')
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])  
    zipobj.close()
    dp.close()
	
	

def SILENT_FRESHSTART():


    dp.create("[COLOR purple][B]DIMITROLOGY[/B][/COLOR][COLOR white] Wizard[/COLOR]","Cleaning your Installation",'Please Wait...', '')
    try:
            for root, dirs, files in os.walk(HOME,topdown=True):
                dirs[:] = [d for d in dirs if d not in EXCLUDES]
                for name in files:
                    try:
                        os.remove(os.path.join(root,name))
                        os.rmdir(os.path.join(root,name))
                    except: pass
                        
                for name in dirs:
                    try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                    except: pass
    except: pass
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    dp.close()	
	
def SILENT_RESTORE():
	import extract
	dp.create("[COLOR=blue][B][/B][/COLOR]","Restoring",'', 'Please Wait')
	extract.all(backup_zip,ADDON_DATA,dp)
	dp.close()
	
def SILENT_BACKUP():

    if not os.path.exists(backupdir): os.makedirs(backupdir)
    exclude_dirs =  ['script.skinshortcuts','skin.estuary','Database','skin.','plugin.video.salts'] #ADD HERE TO EXCLUDE BACKUPS
    exclude_files = [""]
    message_header = "Creating full backup..."
    message_header2 = "Creating full backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""

    ARCHIVE_CB(ADDON_DATA, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)

 
def BUILDMENU():
	dialog = xbmcgui.Dialog()
	url = "http://dimitrology.com/wizard.php?action=getbuilds&user=%s" % (U)
		
	if U == "":
		dialog.ok("Uh oh..", "Please enter your code, then restart the addon. You can get the code by visiting www.dimitrology.com/getcode")
		ADDON.openSettings(sys.argv[0])
		return()
	link = OPEN_URL(url).replace('\n','').replace('\r','')

	try:
		data = json.loads(link)
	except:
		dialog.ok("Uh oh..", link)
		return()
	for entry in data:
		fc = entry['forceclose']
		trailer = entry['trailer']
		print("WIZARD TRAILER", trailer)
		if trailer == '' or trailer == None: trailer = '0'
		if int(fc) == 0:
		
			addLinkBuild(entry['name'] + '  - ver: ' + '[COLOR lime]'+ entry['version'] + '[/COLOR]',entry['zipurl'],90,entry['imgurl'],trailer)
		else:
			addLink(entry['name'] + '  - ver: ' + '[COLOR lime]'+ entry['version'] + '[/COLOR]',entry['zipurl'],91,entry['imgurl'],entry['fanart'],'')
    # link = OPEN_URL('https://archive.org/download/stv_wizard_rel/wizard_rel.txt').replace('\n','').replace('\r','')
    # match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
    # for name,url,iconimage,fanart,description in match:
        # addDir(name + " ver:" + description,url,90,iconimage,fanart,description)
	

	
def WIZARD(name,url,description):  
    if not os.path.exists(packagedir): os.makedirs(packagedir) 
	

    choice2 = xbmcgui.Dialog().yesno("[COLOR=purple]DIMITROLOGY[/COLOR] Wizard", 'Are you certain you want to proceed?', 'You can select to make a clean install or simply add content.', '', yeslabel='Yes',nolabel='No')
    if choice2 == 1:
		fresh = xbmcgui.Dialog().yesno("[COLOR=purple]DIMITROLOGY[/COLOR] Wizard", 'Please choose your installation type!', 'FULL = Performs a Clean Install making a Full Wipe but keeps settings, Debrid info and favourites', 'OVERWRITE = Add Content, Install on top of the Current Configuration', yeslabel='FULL',nolabel='OVERWRITE')
		
	   
		backuprestore.skinswap()
		BACKUP_FAVOURITES()
		SILENT_BACKUP()
		if fresh == 1: SILENT_FRESHSTART()	
		
		
		path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
		if not os.path.exists(path): os.makedirs(path) 
		name = "build"
		

		dp.create("[COLOR=purple][B]Dimitrology TV[/B][/COLOR][COLOR=white] Wizard[/COLOR]","Downloading ",'', 'Please Wait')
		lib=os.path.join(path, name+'.zip')
		try:
		   os.remove(lib)
		except:
		   pass
		
		downloader.download(url, lib, dp)
		addonfolder = xbmc.translatePath(os.path.join('special://','home'))
		time.sleep(2)
		dp.update(0,"", "Extracting Zip Please Wait")
		extract.all(lib,addonfolder,dp)
		time.sleep(1)
		TRIGGER()
		time.sleep(5)
		dp.close()
		SILENT_RESTORE()
		RESTOREFAV()
		# 
		try:os.remove(lib)
		except: pass
		FASTRESET()
    else: 
		return
	
	
	
def FASTRESET():
		dialog.ok("PROCESS COMPLETE", 'The skin will now be reset', 'To start using your new setup please switch the skin System > Interface > Skin to the desired one... if images are not showing, just restart Kodi', 'Click OK to Continue')
		xbmc.executebuiltin('LoadProfile(Master user)')	   

def killxbmc():
    choice = xbmcgui.Dialog().yesno('Force Close XBMC/Kodi', 'We will now attempt to force close Kodi, this is', 'to be used if having problems with guisettings.xml', 'sticking. Would you like to continue?', nolabel='No, Cancel',yeslabel='Yes, Close')
    if choice == 0:
        INDEX()
    elif choice == 1:
        pass
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass        
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")

def Addon_Settings():
    ADDON.openSettings(sys.argv[0])

def WipeXBMC():
    if skin!= "skin.estuary" and skin!="skin.confluence":
		backuprestore.skinswap()
    else:
        choice = xbmcgui.Dialog().yesno("VERY IMPORTANT", 'This will completely wipe your install.', 'Would you like to create a backup before proceeding?', '', yeslabel='Yes',nolabel='No')
        if choice == 1:
            mybackuppath = xbmc.translatePath(os.path.join(backupdir,'Dimitrology TV Builds','My Builds'))
            if not os.path.exists(mybackuppath):
                os.makedirs(mybackuppath)
            vq = _get_keyboard( heading="Enter a name for this backup" )
            if ( not vq ): return False, 0
            title = urllib.quote_plus(vq)
            backup_zip = xbmc.translatePath(os.path.join(mybackuppath,title+'.zip'))
            exclude_dirs_full =  ['Database','backupdir','plugin.video.dimitv','plugin.video.salts']
            exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf']
            message_header = "Creating full backup of existing build"
            message1 = "Archiving..."
            message2 = ""
            message3 = "Please Wait"
            ARCHIVE_CB(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
    choice2 = xbmcgui.Dialog().yesno("ABSOLUTELY CERTAIN?!!!", 'Are you absolutely certain you want to wipe this install?', '', 'All addons EXCLUDING THIS WIZARD will be completely wiped!', yeslabel='Yes',nolabel='No')
    if choice2 == 0:
        return
    elif choice2 == 1:
        dp.create("[COLOR=blue][B]Dimitrology TV[/B][/COLOR] Custom Builds Tool","Wiping Install",'', 'Please Wait')
        try:
            for root, dirs, files in os.walk(HOME,topdown=True):
                dirs[:] = [d for d in dirs if d not in EXCLUDES]
                for name in files:
                    try:
                        os.remove(os.path.join(root,name))
                        os.rmdir(os.path.join(root,name))
                    except: pass
                        
                for name in dirs:
                    try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                    except: pass
        except: pass
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    dialog.ok('[COLOR=blue][B]Dimitrology TV [/B][/COLOR] Custom Builds Tool','Wipe Successful, please restart XBMC/Kodi for changes to take effect.','','')

def REMOVE_EMPTY_FOLDERS():

    print"########### Start Removing Empty Folders #########"
    empty_count = 0
    used_count = 0
    for curdir, subdirs, files in os.walk(HOME):
        if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
            empty_count += 1 #increment empty_count
            os.rmdir(curdir) #delete the directory
            print "successfully removed: "+curdir
        elif len(subdirs) > 0 and len(files) > 0: #check for used directories
            used_count += 1 #increment used_count

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addDirectoryItem(handle, url, listitem, isFolder):
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder)


def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'
#---------------------------------------------------------------------------------------------------
# Addon starts here
params=get_params()
url=None
name=None
buildname=None
updated=None
author=None
version=None
mode=None
iconimage=None
description=None
video=None
link=None
skins=None
videoaddons=None
audioaddons=None
programaddons=None
audioaddons=None
sources=None
local=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        guisettingslink=urllib.unquote_plus(params["guisettingslink"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        mode=str(params["mode"])
except:
        pass
try:
        link=urllib.unquote_plus(params["link"])
except:
        pass
try:
        skins=urllib.unquote_plus(params["skins"])
except:
        pass
try:
        videoaddons=urllib.unquote_plus(params["videoaddons"])
except:
        pass
try:
        audioaddons=urllib.unquote_plus(params["audioaddons"])
except:
        pass
try:
        programaddons=urllib.unquote_plus(params["programaddons"])
except:
        pass
try:
        pictureaddons=urllib.unquote_plus(params["pictureaddons"])
except:
        pass
try:
        local=urllib.unquote_plus(params["local"])
except:
        pass
try:
        sources=urllib.unquote_plus(params["sources"])
except:
        pass
try:
        adult=urllib.unquote_plus(params["adult"])
except:
        pass
try:
        buildname=urllib.unquote_plus(params["buildname"])
except:
        pass
try:
        updated=urllib.unquote_plus(params["updated"])
except:
        pass
try:
        version=urllib.unquote_plus(params["version"])
except:
        pass
try:
        author=urllib.unquote_plus(params["author"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        video=urllib.unquote_plus(params["video"])
except:
        pass

def addLink(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok 
		

def WIZARDFC(name,url,description):  
    if not os.path.exists(packagedir): os.makedirs(packagedir) 
    if skin!= "skin.estuary" and skin!="skin.confluence":
	dialog = xbmcgui.Dialog()
        dialog.ok('[COLOR=purple][B]Dimitrology TV[/B][/COLOR][COLOR=white]  Wizard[/COLOR] ','Please remember to switch to the default Estuary (kodi 17) or Confluence (kodi 16) skin','before proceeding.','')

    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    name = "build"
    dp = xbmcgui.DialogProgress()

    dp.create("[COLOR=purple][B]Dimitrology TV[/B][/COLOR][COLOR=white] Wizard[/COLOR]","Downloading ",'', 'Please Wait')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
	
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", "Extracting Zip Please Wait")

    extract.all(lib,addonfolder,dp)
    xbmc.sleep(1000)
    TRIGGER()
    xbmc.sleep(5000)
    dp.close()
    try: os.remove(lib)
    except: pass
    
    dialog.ok('[COLOR=purple][B]Dimitrology TV[/B][/COLOR][COLOR=white]  Wizard[/COLOR] ','This Build require a Force Close... Click OK To proceed','','')
    killxbmc()

def TRIGGER():
	try:
		url = "http://dimitrology.com/wizard.php?action=logdl" 
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'schismopera')
		response = urllib2.urlopen(req, timeout=3)
		response.read()
		response.close()
	except:
		pass
        
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'schismopera')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
	
	
def OPEN_BROWSER(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


###############################################################
###FORCE CLOSE KODI - ANDROID ONLY WORKS IF ROOTED#############
#######LEE @ COMMUNITY BUILDS##################################

def killxbmc():
    choice = xbmcgui.Dialog().yesno('[COLOR=green]Force Close Kodi[/COLOR]', 'You are about to close Kodi', 'Would you like to continue?', nolabel='No, Cancel',yeslabel='[COLOR=green]Yes, Close[/COLOR]')
    if choice == 0:
        return
    elif choice == 1:
        pass
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am kill org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass        
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    

##########################
###DETERMINE PLATFORM#####
##########################
        
def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'
    
############################
###FRESH START##############
############################

def FRESHSTART(params):
    if os.path.exists(os.path.join(USERDATA,'favourites.xml')):
       to_backup = xbmc.translatePath(os.path.join('special://','home/userdata'))	
       rootlen = len(to_backup)
       backup_ui_zip = xbmc.translatePath(os.path.join(backupdir,'backup_fav.zip'))
       zipobj = zipfile.ZipFile(backup_ui_zip , 'w', zipfile.ZIP_DEFLATED)
       fn = os.path.join(USERDATA, 'favourites.xml')
       dp.create("BACKUP/RESTORE","Backing Up Favourites",'', 'Please Wait')
       zipobj.write(fn, fn[rootlen:])
       dp.close()
    choice2 = xbmcgui.Dialog().yesno("[COLOR=purple]DIMITROLOGY[/COLOR] Wizard", 'Are you absolutely certain you want to proceed?', '', 'All addons EXCLUDING THIS WIZARD will be completely wiped!', yeslabel='[COLOR=red]Yes[/COLOR]',nolabel='[COLOR=green]No[/COLOR]')
    if choice2 == 0:
        return
    elif choice2 == 1:
        dp.create("[COLOR purple][B]Dimitrology TV[/B][/COLOR][COLOR white]Wizard[/COLOR]","Wiping Install",'', 'Please Wait')
        try:
            for root, dirs, files in os.walk(HOME,topdown=True):
                dirs[:] = [d for d in dirs if d not in EXCLUDES]
                for name in files:
                    try:
                        os.remove(os.path.join(root,name))
                        os.rmdir(os.path.join(root,name))
                    except: pass
                        
                for name in dirs:
                    try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                    except: pass
        except: pass
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    dp.close()
    dialog.ok('[COLOR purple][B]Dimitrology TV[/B][/COLOR][COLOR white]Wizard[/COLOR]','Wipe Successful, The interface will now be reset...','','')
    ENABLE_WIZARD()
    xbmc.executebuiltin('LoadProfile(Master user)')	   

	
def REMOVE_EMPTY_FOLDERS():
#initialize the counters
    print"########### Start Removing Empty Folders #########"
    empty_count = 0
    used_count = 0
    for curdir, subdirs, files in os.walk(HOME):
        if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
            empty_count += 1 #increment empty_count
            os.rmdir(curdir) #delete the directory
            print "successfully removed: "+curdir
        elif len(subdirs) > 0 and len(files) > 0: #check for used directories
            used_count += 1 #increment used_count
#---------------------------------------------------------------------------------------------------

	
      
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param


def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==90 :
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		

def addLinkBuild(name, url, mode, iconimage, description):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png",
                           thumbnailImage=iconimage)
    liz.setProperty( "Fanart_Image", iconimage)
    cm = [] 
    # print ("WIZARD BUILD MENUS", sys.argv[0], description)
    # cm.append(('Preview Build', 'RunPlugin(%s?mode=111&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(description.encode('utf-8')), urllib.quote_plus(iconimage))))
    # liz.addContextMenuItems(cm)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz, isFolder=False)
    return ok

def PLAY_VIDEO(name,url,iconimage):
	stream_url = urlresolver.HostedMediaFile(url).resolve()
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
	infoLabels = { 'title': name }                                                                                                                
	liz.setInfo( type="video", infoLabels=infoLabels)
	xbmc.Player ().play(stream_url,liz,False)		
                      
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
        

def selectDialog(list, heading='Dimitrology TV'):
    return dialog.select(heading, list)

def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
        
        
if mode==None or url==None or len(url)<1:
        INDEX()
		
		
elif mode == 111:
	PLAY_VIDEO(name,url,iconimage)
elif mode == 112:
		labels =  ['Backup','Restore']
		select = selectDialog(labels)
		if select == -1: sys.exit(0) 
		elif select == 0: backuprestore.Backup()
		elif select == 1: backuprestore.Restore()

	
elif mode==20:
        BUILDMENU()

elif mode==4:
        RESTORE()
		
elif mode==3:
        BACKUPMENU()

		
elif mode==6:        
	FRESHSTART(params)
	
elif mode==7:
       DeletePackages(url)
		
elif mode==10:
        ADDONWIZARD(name,url,description)
		
		
elif mode==30:
       Wallpapers_Packs()	

elif mode==31:
       Wallpapers_Download(url)
	   

elif mode==32:
       Wallpapers_Clear()

elif mode==82:
        print "############   WIPE XBMC   #################"
        WipeXBMC()

elif mode==85:
        print "############   ATTEMPT TO KILL XBMC/KODI   #################"
        killxbmc()
		
elif mode==90:
        WIZARD(name,url,description)
elif mode==91:
        WIZARDFC(name,url,description)
elif mode==100:
        SETTINGS()
		
elif mode==101:
        ENABLE_ADDONS()		



elif mode==200:
        STORE(name,url,description)
elif mode==201:
        STORE_PAGE()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
