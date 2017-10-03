"""
    

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib2,urllib
import re

import time

import zipfile
import ntpath
import base64
from os import listdir
from os.path import isfile, join
from resources.modules import skinSwitch
from shutil import copyfile

dp           =  xbmcgui.DialogProgress()
AddonTitle="[COLOR purple]DIMITROLOGY[/COLOR] [COLOR white]Wizard[/COLOR]"
AddonID ='plugin.video.dimitv'

selfAddon = xbmcaddon.Addon(id=AddonID)
backupfull = selfAddon.getSetting('backup_database')
backupaddons = selfAddon.getSetting('backup_addon_data')
PACKAGES = xbmc.translatePath(os.path.join('special://home/addons/' + 'packages'))
dialog = xbmcgui.Dialog()  
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID, 'icon.png'))
mastercopy   =  selfAddon.getSetting('mastercopy')
HOME         =  xbmc.translatePath('special://home/')
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
zip = selfAddon.getSetting("remote_backup")
restore_from_zip = selfAddon.getSetting("remote_restore")
RESTORE_FROM = xbmc.translatePath(os.path.join(restore_from_zip))
USB          =  xbmc.translatePath(os.path.join(zip))
HOME         =  xbmc.translatePath('special://home/')
EXCLUDES_FOLDER     =  xbmc.translatePath(os.path.join(USERDATA,'BACKUP'))
ADDON_DATA   =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))

backupdir  =  xbmc.translatePath(os.path.join('special://home/backupdir',''))
backup_zip = xbmc.translatePath(os.path.join(backupdir,'bacup_addon_data.zip'))
dialog = xbmcgui.Dialog()
def open_Settings():
	open_Settings = xbmcaddon.Addon(id=AddonID).openSettings()
	
 
def check_path():
	if not "backupdir" in USB:
		if HOME in USB:
			dialog = xbmcgui.Dialog()
			dialog.ok(AddonTitle, "Invalid path selected for your backups. The path you have selected will be removed during backup and cause an error. Please pick another path that is not in the Kodi directory")
			open_Settings()
			sys.exit(0)
	if not os.path.exists(USB):
		try:
			os.makedirs(USB)
		except:
			dialog = xbmcgui.Dialog()
			dialog.ok(AddonTitle, "Invalid path selected for your backups. The directory specified does not exist or is not writable.")
			open_Settings()
			sys.exit(0)

def _get_keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default
	
def SILENT_BACKUP():

    if not os.path.exists(backupdir): os.makedirs(backupdir)
    choice = xbmcgui.Dialog().yesno('BACKUP SKIN', 'Do you want to include your skin shortcuts settings in the backup?','','', yeslabel='Yes',nolabel='No')
    exclude_dirs =  ['script.skinshortcuts','skin.estuary','Database','skin.tvOS-X','plugin.video.salts'] #ADD HERE TO EXCLUDE BACKUPS
    
    exclude_files = [""]
    message_header = "Creating full backup..."
    message_header2 = "Creating full backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""

    ARCHIVE_CB(ADDON_DATA, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)


def SILENT_RESTORE():
	try:
		import extract
		dp.create("[COLOR=blue][B][/B][/COLOR]","Restoring",'', 'Please Wait')

		extract.all(backup_zip,ADDON_DATA,'')
	except:
		pass
	
	
def Restore():
	try:
		import extract
		if RESTORE_FROM == '' or RESTORE_FROM == None: 
			dialog.ok('ATTENTION', "Invalid or No path selected for the zip file to restore from. Please check the settings and retry.")
			open_Settings()
			sys.exit(0)
		dp.create("[COLOR=blue][B][/B][/COLOR]","Restoring",'', 'Please Wait')
		extract.all(RESTORE_FROM,HOME,dp)
	except:
		pass
		
def Backup():
    guisuccess=1
    check_path()
    try:
		if os.path.exists(PACKAGES):
			shutil.rmtree(PACKAGES)
    except:
		pass
    vq = _get_keyboard(default="my_build", heading="Enter a name for this backup (NO SPACES)" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB,title+'_backup.zip'))
    exclude_dirs =  ['backupdir','cache', 'Thumbnails','temp','packages','Database','plugin.video.salts']
    exclude_files = ["spmc.log","spmc.old.log","xbmc.log","xbmc.old.log","kodi.log","kodi.old.log","Textures13.db"]
    message_header = "Creating full backup..."
    message_header2 = "Creating full backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    FIX_SPECIAL(USERDATA)
    ARCHIVE_CB(HOME, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
    dialog.ok("[COLOR lime][B]SUCCESS![/B][/COLOR]", 'The backup was completed successfully!.',"Backup Location: ",'[COLOR=lime]'+backup_zip+'[/COLOR]')

def FullBackup():
    guisuccess=1
    if not os.path.exists(USB):
        os.makedirs(USB)
    vq = _get_keyboard( heading="Enter a name for this backup" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB,title+'.zip'))
    exclude_dirs =  ['backupdir','cache','temp']
    exclude_files = ["spmc.log","spmc.old.log","xbmc.log","xbmc.old.log","kodi.log","kodi.old.log"]
    message_header = "Creating full backup..."
    message_header2 = "Creating full backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    FIX_SPECIAL(USERDATA)
    ARCHIVE_CB(HOME, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
    dialog.ok("[COLOR green][B]SUCCESS![/B][/COLOR]", 'The backup was completed successfully!.',"Backup Location: ",'[COLOR=yellow]'+backup_zip+'[/COLOR]')

def TV_GUIDE_BACKUP():
    guisuccess=1
    if not os.path.exists(USB):
        os.makedirs(USB)
    vq = _get_keyboard( heading="Enter a name for this backup" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB,title+'_tv_guide.zip'))
    exclude_dirs =  ['']
    exclude_files = [""]
    message_header = "Creating full backup..."
    message_header2 = "Creating full backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    ARCHIVE_CB(GUIDE, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
    dialog.ok("[COLOR green][B]SUCCESS![/B][/COLOR]", 'The backup was completed successfully!.',"Backup Location: ",'[COLOR=yellow]'+backup_zip+'[/COLOR]')

def ADDON_DATA_BACKUP():
    check_path()
    guisuccess=1
    if not os.path.exists(USB): os.makedirs(USB)
    exclude_dirs =  ['script.skinshortcuts','skin.estuary','skin.tvOS-X','Database','plugin.video.salts']

    vq = _get_keyboard(default='backup', heading= "Enter a name for this backup" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB,title+'_addon_data.zip'))

    exclude_files = [""]
    message_header = "Creating full backup..."
    message_header2 = "Creating full backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    FIX_SPECIAL(ADDON_DATA)
    ARCHIVE_CB(ADDON_DATA, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
    dialog.ok("[COLOR green][B]SUCCESS![/B][/COLOR]", 'The backup was completed successfully!.',"Backup Location: ",'[COLOR=lime]'+backup_zip+'[/COLOR]')




def ARCHIVE_CB(sourcefile, destfile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
    zipobj = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(sourcefile)
    for_progress = []
    ITEM =[]
    dp.create(message_header, message1, message2, message3)
    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(sourcefile):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f not in exclude_files]
        for file in files:
            try:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                dp.update(int(progress),"Backing Up",'[COLOR lime]%s[/COLOR]'%file, '')
                fn = os.path.join(base, file)
                zipobj.write(fn, fn[rootlen:]) 
            except: pass			
    zipobj.close()
    dp.close()

def FIX_SPECIAL(url):

    HOME =  xbmc.translatePath('special://home')
    dialog = xbmcgui.Dialog()
    dp.create(AddonTitle,"Renaming paths...",'', '')
    url = xbmc.translatePath('special://userdata')
    for root, dirs, files in os.walk(url):
        for file in files:
            if file.endswith(".xml"):
                 dp.update(0,"Fixing","[COLOR dodgerblue]" + file + "[/COLOR]", "Please wait.....")
                 a=open((os.path.join(root, file))).read()
                 b=a.replace(HOME, 'special://home/')
                 f= open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()


def skinswap():

	skin         =  xbmc.getSkinDir()
	KODIV        =  float(xbmc.getInfoLabel("System.BuildVersion")[:4])
	skinswapped = 0

	#SWITCH THE SKIN IF THE CURRENT SKIN IS NOT CONFLUENCE
	if skin not in ['skin.confluence','skin.estuary']:
		choice = xbmcgui.Dialog().yesno(AddonTitle, 'We can see that you are not using the default Kodi skin.','CLICK YES TO ATTEMPT TO AUTO SWITCH TO DEFAULT BEFORE INSTALLING','PLEASE DO NOT DO PRESS ANY BUTTONS OR MOVE THE MOUSE WHILE THIS PROCESS IS TAKING PLACE, IT IS AUTOMATIC', yeslabel='Yes',nolabel='No')
		if choice == 0:
			sys.exit(1)
		skin = 'skin.estuary' if KODIV >= 17 else 'skin.confluence'
		skinSwitch.swapSkins(skin)
		skinswapped = 1
		time.sleep(1)
	
	#IF A SKIN SWAP HAS HAPPENED CHECK IF AN OK DIALOG (CONFLUENCE INFO SCREEN) IS PRESENT, PRESS OK IF IT IS PRESENT
	if skinswapped == 1:
		if not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
			xbmc.executebuiltin( "Action(Select)" )
	
	#IF THERE IS NOT A YES NO DIALOG (THE SCREEN ASKING YOU TO SWITCH TO CONFLUENCE) THEN SLEEP UNTIL IT APPEARS
	if skinswapped == 1:
		while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
			time.sleep(1)
	
	#WHILE THE YES NO DIALOG IS PRESENT PRESS LEFT AND THEN SELECT TO CONFIRM THE SWITCH TO CONFLUENCE.
	if skinswapped == 1:
		while xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
			xbmc.executebuiltin( "Action(Left)" )
			xbmc.executebuiltin( "Action(Select)" )
			time.sleep(1)
	
	skin         =  xbmc.getSkinDir()

	#CHECK IF THE SKIN IS NOT CONFLUENCE
	if skin not in ['skin.confluence','skin.estuary']:
		choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR lightskyblue][B]ERROR: AUTOSWITCH WAS NOT SUCCESFULL[/B][/COLOR]','[COLOR lightskyblue][B]CLICK YES TO MANUALLY SWITCH TO CONFLUENCE NOW[/B][/COLOR]','[COLOR lightskyblue][B]YOU CAN PRESS NO AND ATTEMPT THE AUTO SWITCH AGAIN IF YOU WISH[/B][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
		if choice == 1:
			xbmc.executebuiltin("ActivateWindow(appearancesettings)")
			return
		else:
			sys.exit(1)

##############################    END    #########################################