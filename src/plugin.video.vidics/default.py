import httplib
import urlparse,urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
import json
import urlresolver
import time,datetime
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import SoupStrainer

from xml.dom.minidom import Document
from t0mm0.common.addon import Addon
import commands
import jsunpack

__settings__ = xbmcaddon.Addon(id='plugin.video.vidics')
home = __settings__.getAddonInfo('path')
#addon = Addon('plugin.video.1channel', sys.argv)
datapath = xbmc.translatePath(os.path.join(home, 'resources', ''))
#langfile = xbmc.translatePath(os.path.join(home, 'resources', 'lang.txt'))
strdomain ="http://www.vidics.ch"
AZ_DIRECTORIES = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y', 'Z']
playablehost=['daclips',
'happystreams',
'filehoot',
'cloudyvideos',
'realvid',
'letwatch',
'2gb-hostin..',
'playhd',
'dailymotion',
'divxstage',
'donevideo',
'ecostream',
'entroupload',
'exashare',
'facebook',
'filebox',
'filenuke',
'flashx',
'gorillavid',
'hostingbulk',
'hostingcup',
'hugefiles',
'jumbofiles',
'lemuploads',
'limevideo',
'megarelease',
'megavids',
'mightyupload',
'mooshare_biz',
'movdivx',
'movpod',
'movreel',
'movshare',
'movzap',
'mp4stream',
'mp4upload',
'mrfile',
'muchshare',
'nolimitvideo',
'nosvideo',
'novamov',
'nowvideo',
'ovfile',
'play44_net',
'played',
'playwire',
'premiumize_me',
'primeshare',
'promptfile',
'purevid',
'putlocker',
'rapidvideo',
'realdebrid',
'rpnet',
'seeon',
'sharedsx',
'sharefiles',
'sharerepo',
'sharesix',
'sharevid',
'skyload',
'slickvid',
'sockshare',
'stagevu',
'stream2k',
'streamcloud',
'teramixer',
'thefile',
'thevideo',
'trollvid',
'tubeplus',
'tunepk',
'ufliq',
'uploadc',
'uploadcrazynet',
'veeHD',
'veoh',
#'vidbull',
'vidcrazynet',
'video44',
'videobb',
'videoboxone',
'videofun',
'videomega',
'videoraj',
'videotanker',
'videovalley',
'videoweed',
'videozed',
'videozer',
'vidhog',
'vidpe',
'vidplay',
'vidspot',
'vidstream',
'vidto',
'vidup',
'vidxden',
'vidzi',
'vidzur',
'vimeo',
'vk',
'vodlocker',
'vureel',
'watchfreeinhd',
'watchfreei..',
'xvidstage',
'yourupload',
'youtube',
'youwatch',
'zalaa',
'zooupload',
'zshare',
'videobug'
'video.google.com',
'bestreams',
'vidx',
'streamin',
'vidpaid',
'uploadnetwork',
'divxpress',
'videopremium',
'faststream',
'v-vids',
'topvideo',
'gamovideo',
'bonanzashare',
'clicktoview',
'flashx.tv',
'speedvid',
'vreer',
'allmyvideos',
'cyberlocker',
'veervid',
'nowdownloa..',
'videoslasher',
'videoslash..',
'billionuploads',
'glumbouploads',
'sharebees',
'uploadorb',
'speedyshare',
'180upload',
'putlocker']

net = Net()
class InputWindow(xbmcgui.WindowDialog):# Cheers to Bastardsmkr code already done in Putlocker PRO resolver.
    def __init__(self, *args, **kwargs):
        self.cptloc = kwargs.get('captcha')
        self.img = xbmcgui.ControlImage(335,20,624,180,self.cptloc)
        self.addControl(self.img)
        self.kbd = xbmc.Keyboard()

    def get(self):
        self.show()
        self.kbd.doModal()
        if (self.kbd.isConfirmed()):
            text = self.kbd.getText()
            self.close()
            return text
        self.close()
        return False
		
def GetContent(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       rcontent=second_response.content
       try:
            rcontent =rcontent.encode("UTF-8")
       except: pass
       return rcontent
    except:	
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')

try:

    DB_NAME = 	 ADDON.getSetting('db_name')
    DB_USER = 	 ADDON.getSetting('db_user')
    DB_PASS = 	 ADDON.getSetting('db_pass')
    DB_ADDRESS = ADDON.getSetting('db_address')

    if  ADDON.getSetting('use_remote_db')=='true' and DB_ADDRESS is not None and DB_USER is not None and DB_PASS is not None and DB_NAME is not None:
        import mysql.connector as database
        print 'Loading MySQL as DB engine'
        DB = 'mysql'
    else:
        print'MySQL not enabled or not setup correctly'
        raise ValueError('MySQL not enabled or not setup correctly')

except:

    try: 
        from sqlite3 import dbapi2 as database
        print 'Loading sqlite3 as DB engine'
    except: 
        from pysqlite2 import dbapi2 as database
        addon.log('pysqlite2 as DB engine')
    DB = 'sqlite'
    db_dir = os.path.join(xbmc.translatePath("special://database"), 'vidicsfav.db')

def initDatabase():
    if DB == 'mysql':
        db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
        cur = db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS favorites (type VARCHAR(10), name TEXT, url VARCHAR(255) UNIQUE, imgurl VARCHAR(255))')
    else:
        if not os.path.isdir(os.path.dirname(db_dir)):
            os.makedirs(os.path.dirname(db_dir))
        db = database.connect(db_dir)
        db.execute('CREATE TABLE IF NOT EXISTS favorites (type, name, url, imgurl)')
    db.commit()
    db.close()
	
def SaveData(SQLStatement): #8888
    if DB == 'mysql':
        db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
    else:
        db = database.connect( db_dir )
    cursor = db.cursor()
    cursor.execute(SQLStatement)
    db.commit()
    db.close()

def HostResolver(url):
		print "in HostResolver"
		parsed_uri = urlparse.urlparse(url)
		server=str(parsed_uri.netloc)
		server=server.split(".")
		if(len(server)>2):
			server=server[1]
		else:
			server=server[0]
		server=server.replace("180upload","one80upload")
		exec "from servers import "+server+" as server_connector"
		rtnstatus,msg = server_connector.test_video_exists( page_url=url )
		if(rtnstatus):
			video_urls = server_connector.get_video_url( page_url=url , video_password="" )
			return video_urls[0][1]
		else:
			return ""
		
def SaveFav(fav_type, name, url, img):
        if fav_type == '': fav_type = getVideotype(url)
        statement  = 'INSERT INTO favorites (type, name, url, imgurl) VALUES (%s,%s,%s,%s)'
        if DB == 'mysql':
            db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
        else:
            db = database.connect( db_dir )
            statement = statement.replace("%s","?")
        cursor = db.cursor()
        try: 
            cursor.execute(statement, (fav_type, urllib.unquote_plus(unicode(name,'latin1')), url, img))
            builtin = 'XBMC.Notification(Save Favorite,Added to Favorites,2000)'
            xbmc.executebuiltin(builtin)
        except database.IntegrityError: 
            builtin = 'XBMC.Notification(Save Favorite,Item already in Favorites,2000)'
            xbmc.executebuiltin(builtin)
        db.commit()
        db.close()
		
def AddFavContext(vidtype, vidurl, vidname, vidimg):
        runstring = 'RunScript(plugin.video.vidics,%s,?mode=22&vidtype=%s&name=%s&imageurl=%s&url=%s)' %(sys.argv[1],vidtype,vidname,vidimg,vidurl)
        #runstring = 'RunPlugin(%s)' % addon.build_plugin_url({'mode':22, 'vidtype':vidtype, 'name':vidname, 'url':vidurl, 'imageurl':vidimg})
        cm = add_contextsearchmenu(vidname,vidtype)
        cm.append(('Add to Vidics Favorites', runstring))
        return cm
def ListFavorites():
      addDir('TV','tv',25,'')
      addDir('Movies','movie',25,'')
def BrowseFavorites(section):
    sql = 'SELECT type, name, url, imgurl FROM favorites WHERE type = ? ORDER BY name'
    if DB == 'mysql':
        db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
        sql = sql.replace('?','%s')
    else: db = database.connect( db_dir )
    cur = db.cursor()
    cur.execute(sql, (section,))
    favs = cur.fetchall()
    for row in favs:
        title      = row[1]
        favurl      = row[2]
        img      = row[3]
        vtype= row[0]
        fanart = ''
        cm = add_contextsearchmenu(title,vtype)
        remfavstring = 'RunScript(plugin.video.vidics,%s,?mode=23&name=%s&url=%s)' %(sys.argv[1],urllib.quote_plus(title.encode("utf-8")),urllib.quote_plus(favurl))
        cm.append(('Remove from Favorites', remfavstring))
        nextmode=7
        if(vtype=="movie"):
              nextmode=4
        addDirContext(title,favurl,nextmode,img,"",vtype,cm)
    db.close()

def DeleteFav(name,url): 
    builtin = 'XBMC.Notification(Remove Favorite,Removed '+name+' from Favorites,2000)'
    xbmc.executebuiltin(builtin)
    sql_del = 'DELETE FROM favorites WHERE name=%s AND url=%s'
    if DB == 'mysql':
            db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
    else:
            db = database.connect( db_dir )
            sql_del = sql_del.replace('%s','?')
    cursor = db.cursor()
    cursor.execute(sql_del, (name, url))
    db.commit()
    db.close()
		
def HOME():
        addDir('Search Movies','search',9,'')
        addDir('Search TV Shows','search',10,'')
        addDir('Search Actors','search',15,'')
        addDir('Recently Added Movies','http://www.vidics.ch/Category-Movies/Genre-Any/Letter-Any/LatestFirst/1.htm',26,'')
        addDir('Recently Added TV Shows','http://www.vidics.ch/Category-TvShows/Genre-Any/Letter-Any/LatestFirst/1.htm',27,'')
        addDir('Favorites','Category-Movies',24,'')
        addDir('Movies A-Z','Category-Movies',16,'')
        addDir('TV Shows A-Z','Category-TvShows',17,'')
        addDir('Movies Genres','Category-Movies',18,'')
        addDir('TV Shows Genres','Category-TvShows',19,'')
        addDir('7 Day TV Schedule','TV Schedule',20,'')
        addDir('Top Movies','http://www.vidics.ch/top/films.html',5,'')
        addDir('Top TV Shows','http://www.vidics.ch/top/tvshows.html',6,'')
        addDir('Movies/TV Show by Actor','http://www.vidics.ch/Category-People/Genre-Any/Letter-Any/ByPopularity/1.htm',12,'')
def LangOption():
        addDir('Show Top Languages','Top',10,'')
        addDir('Show All Languages','All',10,'')
		
def CheckRedirect(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       cj = net.get_cookies()
       return (second_response,cj)
    except:
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')

def getSchedule(sched_date): 
        url="http://www.vidics.ch/calendar/"+sched_date+ ".html"
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        listcontent=re.compile('<div class="indexClanedarDay left" id="date_'+sched_date+'">(.+?)</div>').findall(newlink)
        if(len(listcontent)>0):
                latestepi=re.compile('<h3 itemscope itemtype="http://schema.org/TVSeries" class="CalTvshow" title="(.+?)">(.+?)</h3>').findall(listcontent[0])
                for vtmp,vcontent in latestepi:
                        (sUrl,stmp,sName)=re.compile('<a itemprop="url" class="CalTVshowName pukeGreen" href="(.+?)" title="(.+?)">(.+?)</a>').findall(vcontent)[0]
                        (eUrl,eName)=re.compile('<a itemprop="url" class="CalTVshowEpisode blue" href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(vcontent)[0]
                        addDirContext(RemoveHTML(sName),strdomain+sUrl,7,"","","tv")
                        addDir("  --"+RemoveHTML(eName),strdomain+eUrl,4,"")  
def List4Days():
        sched_date=str(datetime.date.today())
        date_name=time.strftime("%A", time.strptime(sched_date, "%Y-%m-%d"))
        addDir("Today's("+sched_date+") TV Schedule",sched_date,21,"episode")
        sched_date=str(datetime.date.today()-datetime.timedelta(days=1))
        date_name=time.strftime("%A", time.strptime(sched_date, "%Y-%m-%d"))
        addDir(date_name+"'s("+sched_date+") TV Schedule",sched_date,21,"episode")
        sched_date=str(datetime.date.today()-datetime.timedelta(days=2))
        date_name=time.strftime("%A", time.strptime(sched_date, "%Y-%m-%d"))
        addDir(date_name+"'s("+sched_date+") TV Schedule",sched_date,21,"episode")
        sched_date=str(datetime.date.today()-datetime.timedelta(days=3))
        date_name=time.strftime("%A", time.strptime(sched_date, "%Y-%m-%d"))
        addDir(date_name+"'s("+sched_date+") TV Schedule",sched_date,21,"episode")
        sched_date=str(datetime.date.today()-datetime.timedelta(days=4))
        date_name=time.strftime("%A", time.strptime(sched_date, "%Y-%m-%d"))
        addDir(date_name+"'s("+sched_date+") TV Schedule",sched_date,21,"episode")
        sched_date=str(datetime.date.today()-datetime.timedelta(days=5))
        date_name=time.strftime("%A", time.strptime(sched_date, "%Y-%m-%d"))
        addDir(date_name+"'s("+sched_date+") TV Schedule",sched_date,21,"episode")
        sched_date=str(datetime.date.today()-datetime.timedelta(days=6))
        date_name=time.strftime("%A", time.strptime(sched_date, "%Y-%m-%d"))
        addDir(date_name+"'s("+sched_date+") TV Schedule",sched_date,21,"episode")
		
def Mirrors(url,name):
  link = GetContent(url)
  link=''.join(link.splitlines()).replace('\'','"')
  soup = BeautifulSoup(link)
  listcontent=soup.findAll('a',{"href":re.compile("/Link/")})
  for item in listcontent:
			vname=item.contents[0]
			vurl=item["href"]
			if(str(vname).split('.')[0].lower() in playablehost):
				addLink(vname,strdomain+vurl,3,"",name)


def add_contextsearchmenu(title, video_type):
    title=urllib.quote(title)
    contextmenuitems = []
    if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.1channel'):
        contextmenuitems.append(('Search 1channel',
                                 'XBMC.Container.Update(%s?mode=%s&section=%s&query=%s)' % (
                                     'plugin://plugin.video.1channel/', '7000',video_type, title)))
    if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.icefilms'):
        contextmenuitems.append(('Search Icefilms',
                                 'XBMC.Container.Update(%s?mode=555&url=%s&search=%s&nextPage=%s)' % (
                                     'plugin://plugin.video.icefilms/', 'http://www.icefilms.info/', title, '1')))
    if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.movie25'):
        contextmenuitems.append(('Search Mash Up',
                                 'XBMC.Container.Update(%s?mode=%s&url=%s)' % (
                                     'plugin://plugin.video.movie25/', '4', title)))
    if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.tubeplus'):
        if video_type == 'tv':
            section = 'None'
            serurl='http://www.tubeplus.me/search/tv-shows/%s/'%(title)
        else:
            serurl='http://www.tubeplus.me/search/movies/"%s"/'%(title)
            section = 'movie'
       
        contextmenuitems.append(('Search tubeplus', 'XBMC.Container.Update(%s?mode=150&types=%s&url=%s&linkback=latesttv)' % (
            'plugin://plugin.video.tubeplus/', section, serurl)))
    if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.tvlinks'):
        if video_type == 'tv':
            contextmenuitems.append(('Search tvlinks', 'XBMC.Container.Update(%s?mode=Search&query=%s)' % (
                'plugin://plugin.video.tvlinks/', title)))
    if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.solarmovie'):
        if video_type == 'tv':
            section = 'tv-shows'
        else:
            section = 'movies'
        contextmenuitems.append(('Search solarmovie', 'XBMC.Container.Update(%s?mode=Search&section=%s&query=%s)' % (
            'plugin://plugin.video.solarmovie/', section, title)))

    return contextmenuitems


		
def GetParts(vicontent,vidname):
        dialog = xbmcgui.Dialog()
        titles = []
        urlcontent=re.compile('<div class="movie_link1">(.+?)</div>').findall(vicontent)
        urllist=[]
        for ucontent in urlcontent:
            titletext=re.compile('<h4>(.+?)</h4>').findall(ucontent)[0]
            url=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>').findall(ucontent)[0]
            titles.append(titletext)
            urllist.append(url)
        index = dialog.select('Choose your stream', titles)
        win = xbmcgui.Window(10000)
        win.setProperty('1ch.playing.episode', str(index))
        return CheckRedirect(urllist[index])
		
def ParseVideoLink(url,name,movieinfo):
    dialog = xbmcgui.DialogProgress()
    dialog.create('Resolving', 'Resolving video Link...')       
    dialog.update(0)
    (respon,cj) = CheckRedirect(url)
    link=respon.content
    tmpcontent=link
    redirlink = respon.get_url().lower()
    link = ''.join(link.splitlines()).replace('\'','"')
    # borrow from 1channel requires you to have 1channel
    win = xbmcgui.Window(10000)
    win.setProperty('1ch.playing.title', movieinfo)
    win.setProperty('1ch.playing.season', str(3))
    win.setProperty('1ch.playing.episode', str(4))
    if(redirlink.find("vidics") >-1):
            (respon,cj) = GetParts(link,name)
            link=respon.content
            tmpcontent=link
            redirlink = respon.get_url().lower()
            link = ''.join(link.splitlines()).replace('\'','"')
    # end 1channel code
    print redirlink
    #try:
    if True:

       sources = []
       label=name
       hosted_media = urlresolver.HostedMediaFile(url=redirlink, title=label)
       sources.append(hosted_media)
       source = urlresolver.choose_source(sources)
       print "inresolver=" + redirlink
       xbmc.log(str(source))
       if source:
        vidlink=source.resolve()
       else:
        if (redirlink.find("youtube") > -1):
                vidmatch=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(redirlink)
                vidlink=vidmatch[0][len(vidmatch[0])-1].replace('v/','')
                vidlink='plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid='+vidlink
        elif (redirlink.find("yourupload") > -1):
                media_url= ""
                media_url = re.compile('<meta property="og:video" content="(.+?)"/>').findall(link)[0]
                vidlink = media_url
        elif (redirlink.find("video44") > -1):
                media_url= ""
                media_url = re.compile('url:\s*"(.+?)"').findall(link)[0]
                vidlink = media_url
        elif (redirlink.find("videobug") > -1):
                media_url= ""
                media_url = re.compile('playlist:\s*\[\s*\{\s*url:\s*"(.+?)",').findall(link)[0]
                vidlink = urllib.unquote(media_url)
        elif (redirlink.find("letwatch") > -1):
                paccked= re.compile('<script type=(?:"|\')text/javascript(?:"|\')>(eval\(function\(p,a,c,k,e,d\).*?)</script>').findall(link)
                if(len(paccked) > 0):
                      link=jsunpack.unpack(paccked[0].replace('"','\''))
                else:
                      idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                      op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                      hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                      fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                      posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                      link=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                      link=''.join(link.splitlines()).replace('\'','"')
                      paccked= re.compile('<script type=(?:"|\')text/javascript(?:"|\')>(eval\(function\(p,a,c,k,e,d\).*?)</script>').findall(link)
                      if(len(paccked) > 0):
                             link=jsunpack.unpack(paccked[0].replace('"','\''))
                media_url = re.compile("sources:\s*\[\{file:\s*'(.+?)'").findall(link.replace('"','\''))[0]
                vidlink = urllib.unquote(media_url)
        elif (redirlink.find("video.google.com") > -1):
                match=redirlink.split("docid=")
                glink=""
                newlink=redirlink+"&dk"
                if(len(match) > 0):
                        glink = GetContent("http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid="+match[1].split("&")[0])
                else:
                        match=re.compile('http://video.google.com/googleplayer.swf.+?docId=(.+?)&dk').findall(newlink)
                        if(len(match) > 0):
                                glink = GetContent("http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid="+match[0])
                gcontent=re.compile('<div class="mod_download"><a href="(.+?)" title="Click to Download">').findall(glink)
                if(len(gcontent) > 0):
                        vidlink=gcontent[0]
                else:
                        vidlink=""
        elif (redirlink.find("movshare") > -1):
                fileid=re.compile('flashvars.file="(.+?)";').findall(link)[0]
                codeid=re.compile('flashvars.cid="(.+?)";').findall(link)[0]
                keycode=re.compile('flashvars.filekey="(.+?)";').findall(link)[0]
                vidcontent=GetContent("http://www.movshare.net/api/player.api.php?codes="+urllib.quote_plus(codeid) + "&key="+urllib.quote_plus(keycode) + "&file=" + urllib.quote_plus(fileid))
                vidlink = re.compile('url=(.+?)\&').findall(vidcontent)[0]
        elif (redirlink.find("nowvideo") > -1):
                fileid=re.compile('flashvars.file="(.+?)";').findall(link)[0]
                codeid=re.compile('flashvars.cid="(.+?)";').findall(link)[0]
                keycode=re.compile('flashvars.filekey=(.+?);').findall(link)[0]
                keycode=re.compile('var\s*'+keycode+'="(.+?)";').findall(link)[0]
                vidcontent=GetContent("http://www.nowvideo.sx/api/player.api.php?codes="+urllib.quote_plus(codeid) + "&key="+urllib.quote_plus(keycode) + "&file=" + urllib.quote_plus(fileid))
                vidlink = re.compile('url=(.+?)\&').findall(vidcontent)[0]
        elif (redirlink.find("bestreams") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 2)
                dialog.create('Resolving', 'Resolving bestreams Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('setup\(\{\s*file:\s*"(.+?)",\s*').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("vidx") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 10)
                dialog.create('Resolving', 'Resolving vidx Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Weiter+%2F+continue",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('setup\(\{\s*file:\s*"(.+?)",\s*').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("realvid") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                paccked= re.compile('<script type=(?:"|\')text/javascript(?:"|\')>(eval\(function\(p,a,c,k,e,d\).*?)</script>').findall(pcontent)
                if(len(paccked) > 0):
                      pcontent=jsunpack.unpack(paccked[0].replace('"','\''))
                vidlink = re.compile("file:\s*'(.+?)'").findall(pcontent.replace('"','\''))[0]
        elif (redirlink.find("happystreams") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                paccked= re.compile('<script type=(?:"|\')text/javascript(?:"|\')>(eval\(function\(p,a,c,k,e,d\).*?)</script>').findall(pcontent)
                if(len(paccked) > 0):
                      pcontent=jsunpack.unpack(paccked[0].replace('"','\''))
                vidlink = re.compile("file:\s*'(.+?)'").findall(pcontent)[0]
        elif (redirlink.find("streamin") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 5)
                dialog.create('Resolving', 'Resolving streamin Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                tmplink = re.compile('setup\(\{\s*file:\s*"(.+?)",\s*streamer:\s*"(.+?)"').findall(pcontent)
                vidlink = tmplink[0][1]+"/"+tmplink[0][0] + " playPath="+tmplink[0][0]
                if(tmplink[0][0].find("http:") > -1):
                        #vidlink = re.compile('setup\(\{\s*file:\s*"(.+?)",\s*').findall(pcontent)
                        vidlink = tmplink[0][0]
        elif (redirlink.find("playhd") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed%20to%20video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('file:\s*"(.+?)",').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("slickvid") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 5)
                dialog.create('Resolving', 'Resolving slickvid Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Watch",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('file:\s*"(.+?)",').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("vidpaid") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 1)
                dialog.create('Resolving', 'Resolving vidpaid Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Continue+to+Video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('setup\(\{\s*file:\s*"(.+?)",\s*').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("filehoot") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","fname":fname,"id":idkey,"referer":url,"method_free":"Continue+to+watch+your+Video","down_direct":"1"})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('file:\s*"(.+?)"').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("skyvid") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download2","rand":rand,"id":idkey,"referer":url,"method_free":"","method_premium":"","down_direct":"1"})
                dialog.close()
                do_wait('Waiting on link to activate', '', 5)
                dialog.create('Resolving', 'Resolving cloudyvideos Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                paccked= re.compile('<script type=(?:"|\')text/javascript(?:"|\')>(eval\(function\(p,a,c,k,e,d\).*?)</script>').findall(pcontent)
                if(len(paccked) > 1):
                      pcontent=jsunpack.unpack(paccked[1].replace('"','\''))
                vidlink = re.compile("file:\s*'(.+?)'").findall(pcontent.replace('"','\''))
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0] +"|"+urllib.urlencode( {'Referer':'http://skyvids.net/player/jw5.swf','User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12'} )
        elif (redirlink.find("cloudyvideos") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download2","rand":rand,"id":idkey,"referer":url,"method_free":"","method_premium":"","down_direct":"1"})
                dialog.close()
                do_wait('Waiting on link to activate', '', 2)
                dialog.create('Resolving', 'Resolving cloudyvideos Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('file:\s*"(.+?)"').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("uploadnetwork") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download2","rand":rand,"id":idkey,"referer":url,"method_free":"","method_premium":"","down_direct":"1"})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('"file":\s*"(.+?)"').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("divxpress") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download2","rand":rand,"id":idkey,"referer":url,"method_free":"","method_premium":"","down_direct":"1"})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('swfobject.js"></script><script type="text/javascript">(.+?)</script>').findall(pcontent)
                if(len(packed) == 0):
                      packed = re.compile('<div id="player_code"><script type="text/javascript">(.+?)</script>').findall(pcontent)[0]
                      sUnpacked = unpackjs4(packed).replace("\\","")
                      vidlink = re.compile('src="(.+?)"').findall(sUnpacked)[0]
                else:
                      packed=packed[0]
                      sUnpacked = unpackjs4(packed).replace("\\","")
                      vidlink = re.compile('addVariable\("file",\s*"(.+?)"\)').findall(sUnpacked)

        elif (redirlink.find("videopremium") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                mfree = re.compile('<input type="submit" name="method_free" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"referer":"","method_free":mfree})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('src="/swfobject.js"></script>\s*<script type="text/javascript">(.+?)</script>').findall(pcontent)[0]
                sUnpacked = unpackjs4(packed)  
                vidpart = re.compile('"file":"(.+?)",p2pkey:"(.+?)"').findall(sUnpacked)[0]
                vidswf = re.compile('embedSWF\("(.+?)",').findall(sUnpacked)[0]
                vidlink=""
                if(len(vidpart) > 0):
                        vidlink = "rtmp://e9.md.iplay.md/play/"+vidpart[1]+" swfUrl="+vidswf+" playPath="+vidpart[1] +" pageUrl=" + redirlink + " tcUrl=rtmp://e9.md.iplay.md/play"
                #vidlink="rtmp://e9.md.iplay.md/play/mp4:rx90tddtnfmc.f4v swfUrl=http://videopremium.tv/uplayer/uppod.swf pageUrl=http://videopremium.tv/rx90tddtnfmc playPath=mp4:rx90tddtnfmc.f4v tcUrl=rtmp://e9.md.iplay.md/play"
        elif (redirlink.find("faststream") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"fname":fname,"referer":url,"hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 3)
                dialog.create('Resolving', 'Resolving faststream Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Continue+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('file:\s*"(.+?)",').findall(pcontent)[0]
        elif (redirlink.find("videomega") > -1):
                refkey= re.compile('\?ref=(.+?)&dk').findall(redirlink+"&dk")[0]
                vidcontent="http://videomega.tv/iframe.php?ref="+refkey
                pcontent=GetContent(vidcontent)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                urlcode = re.compile('else\{\s*document.write\(unescape\("(.+?)"\)\);').findall(pcontent)[0]
                vidcontent=urllib.unquote_plus(urlcode)
                vidlink = re.compile('file:\s*"(.+?)"\s*,').findall(vidcontent)[0]
        elif (redirlink.find("v-vids") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download2","rand":rand,"id":idkey,"referer":url,"method_free":"","method_premium":"","down_direct":"1"})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('file:\s*"(.+?)",').findall(pcontent)[0]
        elif (redirlink.find("thefile") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download2","rand":rand,"id":idkey,"referer":url,"method_free":"","method_premium":"","down_direct":"1"})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('<span>\s*<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>\s*</span>').findall(pcontent)[0][0]
        elif (redirlink.find("topvideo") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"fname":fname,"referer":url,"hash":hash})
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('jwplayer.key="(.+?)";</script>\s*<script type="text/javascript">(.+?)</script>').findall(pcontent)[0][1]
                sUnpacked = unpackjs4(packed)
                unpacked = sUnpacked.replace("\\","")
                vidlink = re.compile('file:"(.+?)",').findall(unpacked)[0]
        elif (redirlink.find("gamovideo") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"fname":fname,"referer":url,"hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 5)
                dialog.create('Resolving', 'Resolving gamovideo Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('/jwplayer.js"></script>\s*<script type="text/javascript">(.+?)</script>').findall(pcontent)[0]
                sUnpacked = unpackjs4(packed)
                unpacked = sUnpacked.replace("\\","")
                vidlink = re.compile('file:"(.+?)",').findall(unpacked)[0]
        elif (redirlink.find("vodlocker") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"fname":fname,"referer":url,"hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 3)
                dialog.create('Resolving', 'Resolving bestreams Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = ""
                vidlink2 = re.compile('file:\s*"(.+?)",').findall(pcontent)
                if(len(vidlink2) > 0):
                        vidlink = vidlink2[0] #vidlink2[0][1]+"/mp4:"+vidlink2[0][0]+" swfUrl=http://vodlocker.com/player/player.swf playPath=mp4:"+vidlink2[0][0]
        elif (redirlink.find("exashare") > -1):
                packed = re.compile('/jwplayer.js"></script>\s*<script type="text/javascript">(.+?)</script>').findall(link)[0]
                sUnpacked = unpackjs4(packed)
                unpacked = sUnpacked.replace("\\","")
                vidlink = re.compile('file:"(.+?)",').findall(unpacked)[0]
        elif (redirlink.find("vidup.me") > -1):

                try:
                      link =link.encode("UTF-8")
                except: pass
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link.replace('"S',"'S"))[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"fname":fname,"referer":url})
                pcontent=postContent(redirlink,posdata+"&method_free_01=Proceed+To+Video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                paccked= re.compile('<script type=(?:"|\')text/javascript(?:"|\')>(eval\(function\(p,a,c,k,e,d\).*?)</script>').findall(pcontent)
                if(len(paccked) > 0):
                      pcontent=jsunpack.unpack(paccked[0].replace('"','\''))
                vidlink = re.compile("file:'(.+?)'").findall(pcontent)[0]
        elif (redirlink.find("sharesix") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"fname":fname,"referer":url})
                pcontent=postContent(redirlink,posdata+"&method_free=Free",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('swfobject.js"></script>\s*<script type="text/javascript">(.+?)</script>').findall(pcontent)[0]
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                        
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('.addVariable\("file",\s*"(.+?)"').findall(unpacked)[0]
        elif (redirlink.find("bonanzashare") > -1):
                capchacon =re.compile('<b>Enter code below:</b>(.+?)</table>').findall(link)
                capchar=re.compile('<span style="position:absolute;padding-left:(.+?);[^>]*>(.+?)</span>').findall(capchacon[0])
                capchar=sorted(capchar, key=lambda x: int(x[0].replace("px","")))
                capstring =""
                for tmp,aph in capchar:
                        capstring=capstring+chr(int(aph.replace("&#","").replace(";","")))
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                ddirect = re.compile('<input type="hidden" name="down_direct" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"id":idkey,"referer":url,"method_free":"","rand":rand,"method_premium":"","code":capstring,"down_direct":ddirect})
                newpcontent=postContent(redirlink,posdata,url)
                newpcontent=''.join(newpcontent.splitlines()).replace('\'','"')
                vidlink=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>Download the file</a>').findall(newpcontent)[0] 
        elif (redirlink.find("videozed") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                mfree = re.compile('<input type="submit" name="method_free"  value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":mfree})
                pcontent=postContent(redirlink,posdata,"http://www.vidics.ch/watch/120351/This-Is-40-2012.html")
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                capchacon =re.compile('<b>Enter code below:</b>(.+?)</table>').findall(pcontent)
                capchar=re.compile('<span style="position:absolute;padding-left:(.+?);[^>]*>(.+?)</span>').findall(capchacon[0])
                capchar=sorted(capchar, key=lambda x: int(x[0].replace("px","")))
                capstring =""
                for tmp,aph in capchar:
                        capstring=capstring+chr(int(aph.replace("&#","").replace(";","")))

                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(pcontent)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(pcontent)[0]
                mfree = re.compile('<input type="hidden" name="method_free" value="(.+?)">').findall(pcontent)[0]
                rand = re.compile('<input type="hidden" name="rand" value="(.+?)">').findall(pcontent)[0]
                ddirect = re.compile('<input type="hidden" name="down_direct" value="(.+?)">').findall(pcontent)[0]
                posdata=urllib.urlencode({"op":op,"id":idkey,"referer":url,"method_free":mfree,"rand":rand,"method_premium":"","code":capstring,"down_direct":ddirect})
                newpcontent=postContent(redirlink,posdata,url)
                newpcontent=''.join(newpcontent.splitlines()).replace('\'','"')
                packed = re.compile('<div id="player_code">(.+?)</div>').findall(newpcontent)[0]
                packed = packed.replace("</script>","")
                unpacked = unpackjs4(packed)  
                unpacked = unpacked.replace("\\","")
                vidsrc = re.compile('src="(.+?)"').findall(unpacked)
                if(len(vidsrc) == 0):
                         vidsrc=re.compile('"file","(.+?)"').findall(unpacked)
                vidlink=vidsrc[0]
        elif (redirlink.find("donevideo") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('action=""><input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                mfree = re.compile('<input type="submit" name="method_free"  value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":mfree})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('<div id="player_code">(.+?)</div>').findall(pcontent)[0]
                packed = packed.replace("</script>","")
                unpacked = unpackjs4(packed)  
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('src="(.+?)"').findall(unpacked)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(unpacked)
                vidlink=vidlink[0]
        elif (redirlink.find("clicktoview") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                mfree = re.compile('<input type="submit" name="method_free" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":mfree})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                capchacon =re.compile('another captcha</a>(.+?)</script>').findall(pcontent)[0]
                capchalink=re.compile('<script type="text/javascript" src="(.+?)">').findall(capchacon)
                strCodeInput="recaptcha_response_field"
                respfield=""
                if(len(capchalink)==0):
                         capchacon =re.compile('<b>Enter code below:</b>(.+?)</table>').findall(pcontent)
                         capchar=re.compile('<span style="position:absolute;padding-left:(.+?);[^>]*>(.+?)</span>').findall(capchacon[0])
                         capchar=sorted(capchar, key=lambda x: int(x[0].replace("px","")))
                         capstring =""
                         for tmp,aph in capchar:
                                  capstring=capstring+chr(int(aph.replace("&#","").replace(";","")))
                         puzzle=capstring
                         strCodeInput="code"
                else:
                         imgcontent=GetContent(capchalink[0])
                         respfield=re.compile("challenge : '(.+?)'").findall(imgcontent)[0]
                         imgurl="http://www.google.com/recaptcha/api/image?c="+respfield
                         solver = InputWindow(captcha=imgurl)
                         puzzle = solver.get()
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(pcontent)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(pcontent)[0]
                mfree = re.compile('<input type="hidden" name="method_free" value="(.+?)">').findall(pcontent)[0]
                rand = re.compile('<input type="hidden" name="rand" value="(.+?)">').findall(pcontent)[0]
                ddirect = re.compile('<input type="hidden" name="down_direct" value="(.+?)">').findall(pcontent)[0]
                #replace codevalue with capture screen
                posdata=urllib.urlencode({"op":op,"id":idkey,"referer":url,"method_free":mfree,"rand":rand,"method_premium":"","recaptcha_challenge_field":respfield,strCodeInput:puzzle,"down_direct":ddirect})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('<div id="player_code">(.+?)</div>').findall(pcontent)[0]
                packed = packed.split("</script>")[1]
                unpacked = unpackjs4(packed)  
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('"file","(.+?)"').findall(unpacked)[0]
        elif (redirlink.find("vidbull") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download2","rand":rand,"id":idkey,"referer":url,"method_free":"","method_premium":"","down_direct":"1"})
                #They need to wait for the link to activate in order to get the proper 2nd page
                dialog.close()
                do_wait('Waiting on link to activate', '', 3)
                dialog.create('Resolving', 'Resolving vidbull Link...') 
                dialog.update(50)
                pcontent=postContent2(redirlink,posdata,url)
                #pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink= re.compile('<!--RAM disable direct link<a href="(.+?)" target="_top">').findall(pcontent)
                if(len(vidlink) > 0):
                         filename = vidlink[0].split("/")[-1:][0]
                         vidlink=vidlink[0].replace(filename,"video.mp4")
                else:
                         sPattern =  '<script type=(?:"|\')text/javascript(?:"|\')>eval\(function\(p,a,c,k,e,[dr]\)(?!.+player_ads.+).+?</script>'
                         r = re.search(sPattern, pcontent, re.DOTALL + re.IGNORECASE)
                         if r:
                              sJavascript = r.group()
                              sUnpacked = jsunpack.unpack(sJavascript)
                              stream_url = re.search('[^\w\.]file[\"\']?\s*[:,]\s*[\"\']([^\"\']+)', sUnpacked)
                              if stream_url:
                                    vidlink= stream_url.group(1)

        elif (redirlink.find("nosvideo") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","fname":fname,"rand":"","id":idkey,"referer":url,"method_free":"Continue+to+Video","method_premium":"","down_script":"1"})
                pcontent=postContent2(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                scriptcontent=re.compile('<div name="placeholder" id="placeholder">(.+?)</div></div>').findall(pcontent)[0]
                packed = scriptcontent.split("</script>")[1]
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                        
                unpacked = unpacked.replace("\\","")

                xmlUrl=re.compile('"playlist=(.+?)&').findall(unpacked)[0]
                vidcontent = postContent2(xmlUrl,None,url)
                vidlink=re.compile('<file>(.+?)</file>').findall(vidcontent)[0]
        elif (redirlink.find("vidspot") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","method_free":"1"})
                pcontent=postContent(redirlink,posdata+"&x=83&y=15",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                media_url = re.compile('"sources"\s*:\s*\[\s*\{\s*"file"\s*:\s*"(.+?)"\s*\}').findall(pcontent)[0]
                finalcontent=GetContent(redirlink.replace(idkey,"")+media_url)
                finalcontent=''.join(finalcontent.splitlines()).replace('\'','"')
                dmlink=re.compile('<meta [^>]*base=["\']?([^>^"^\']+)["\']?[^>]*>').findall(finalcontent)
                fillink=re.compile('<video [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(finalcontent)
                vidlink=dmlink[0]+fillink[0]+" app="+dmlink[0].split("/")[-2]+"/ swfUrl=http://p.jwpcdn.com/6/10/jwplayer.flash.swf playPath="+fillink[0] +" pageUrl=" + redirlink + " tcUrl="+dmlink[0]
        elif (redirlink.find("flashx.tv") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                xbmc.log(str(posdata))
                dialog.close()
                do_wait('Waiting on link to activate', '', 5)
                dialog.create('Resolving', 'Resolving flashx Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed%20to%20video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                paccked= re.compile('<script type=(?:"|\')text/javascript(?:"|\')>(eval\(function\(p,a,c,k,e,d\).*?)</script>').findall(pcontent)
                if(len(paccked) > 0):
                      pcontent=jsunpack.unpack(paccked[0].replace('"','\''))
                media_url = re.compile('sources:\s*\[\{file:\s*"(.+?)"\}\]').findall(pcontent)[0]
                finalcontent=GetContent(media_url)
                finalcontent=''.join(finalcontent.splitlines()).replace('\'','"')
                dmlink=re.compile('<meta [^>]*base=["\']?([^>^"^\']+)["\']?[^>]*>').findall(finalcontent)
                fillink=re.compile('<video [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(finalcontent)
                vidlink=dmlink[0]+fillink[0]+" app="+dmlink[0].split("/")[-2]+"/ swfUrl=http://static.flashx.tv/player6/jwplayer.flash.swf playPath="+fillink[0] +" pageUrl=" + redirlink + " tcUrl="+dmlink[0]
        elif (redirlink.find("speedvid") > -1):
                keycode=re.compile('\|image\|(.+?)\|(.+?)\|file\|').findall(link)
                domainurl=re.compile('\[IMG\](.+?)\[/IMG\]').findall(link)[0]
                domainurl=domainurl.split("/i/")[0]
                vidlink=domainurl+"/"+keycode[0][1]+"/v."+keycode[0][0]
        elif (redirlink.find("vreer") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)" />').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)" />').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)" />').findall(link)[0]
                rand = re.compile('<input type="hidden" name="hash" value="(.+?)" />').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","fname":fname,"hash":rand,"id":idkey,"referer":"","method_free":"Free Download"})
                #They need to wait for the link to activate in order to get the proper 2nd page
                dialog.close()
                do_wait('Waiting on link to activate', '', 20)
                dialog.create('Resolving', 'Resolving vreer Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink=re.compile('file: "(.+?)",').findall(pcontent)[0]
        elif (redirlink.find("allmyvideos") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                mfree = re.compile('<input type="hidden" name="method_free" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":mfree})
                pcontent=postContent2(redirlink,posdata,url)
                packed = get_match( pcontent , "(<script type='text/javascript'>eval\(.*?function\(p,\s*a,\s*c,\s*k,\s*e,\s*d.*?)</script>",1)
                unpacked = unpackjs(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                        
                unpacked = unpacked.replace("\\","")
                try:
                    vidlink = get_match(unpacked,"'file'\s*\:\s*'([^']+)'")+"?start=0"+"|"+urllib.urlencode( {'Referer':'http://allmyvideos.net/player/player.swf','User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12'} )
                except:
                    vidlink = get_match(unpacked,'"file"\s*\:\s*"([^"]+)"')+"?start=0"+"|"+urllib.urlencode( {'Referer':'http://allmyvideos.net/player/player.swf','User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12'} )

        elif (redirlink.find("cyberlocker") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('action=""><input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":"Free Download"})
                pcontent=postContent2(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('<div id="player_code">(.+?)</div>').findall(pcontent)[0]
                packed = packed.replace("</script>","")
                unpacked = unpackjs4(packed)  
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('name="src"value="(.+?)"').findall(unpacked)[0]
        elif (redirlink.find("promptfile") > -1):
                chash = re.compile('<input type="hidden" name="chash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"chash":chash})
                pcontent=postContent2(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>Download File</a>').findall(pcontent)[0]
        elif (redirlink.find("veervid") > -1):
                posturl=re.compile('<form action="(.+?)" method="post">').findall(link)[0]
                pcontent=postContent(posturl,"continue+to+video=Continue+to+Video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink=re.compile('so.addVariable\("file","(.+?)"').findall(pcontent)[0]
        elif (redirlink.find("sharerepo") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                ddirect = re.compile('<input type="hidden" name="down_direct" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","fname":fname.encode('utf-8'),"id":idkey,"referer":url,"method_free":"Free Download","down_direct":ddirect})
                pcontent=postContent2(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('<div id="player_code">(.+?)</div>').findall(pcontent)[0]
                packed=packed.split("</script>")[1]
                unpacked = unpackjs4(packed)  
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('"file","(.+?)"').findall(unpacked)[0]
        elif (redirlink.find("nowdownloa") > -1):
                ddlpage = re.compile('<a class="btn btn-danger" href="(.+?)">Download your file !</a>').findall(link)[0]
                mainurl = redirlink.split("/dl/")[0]
                ddlpage= mainurl+ddlpage
                #They need to wait for the link to activate in order to get the proper 2nd page
                dialog.close()
                do_wait('Waiting on link to activate', '', 30)
                dialog.create('Resolving', 'Resolving nowdownloads Link...') 
                dialog.update(50)
                pcontent=GetContent(ddlpage)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                linkcontent =re.compile('Slow download</span>(.+?)</div>').findall(pcontent)[0]
                vidlink = re.compile('<a href="(.+?)" class="btn btn-success">').findall(linkcontent)[0]
        elif (redirlink.find("youwatch") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                rand = re.compile('<input type="hidden" name="hash" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","fname":fname,"hash":rand,"id":idkey,"referer":"","imhuman":"Slow Download","method_premium":""})
                #They need to wait for the link to activate in order to get the proper 2nd page
                dialog.close()
                do_wait('Waiting on link to activate', '', 10)
                dialog.create('Resolving', 'Resolving youwatch Link...') 
                dialog.update(50)
                pcontent=postContent2(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines())
                packed = re.compile("<span id='flvplayer'></span>(.+?)</script>").findall(pcontent)[0]
                unpacked = unpackjs5(packed)  
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('file:"(.+?)"').findall(unpacked)[0]
        elif (redirlink.find("videoslasher") > -1):
                user=re.compile('user: ([^"]+),').findall(link)[0]
                code=re.compile('code: "([^"]+)",').findall(link)[0]
                hash1=re.compile('hash: "([^"]+)"').findall(link)[0]
                formdata = { "user" : user, "code": code, "hash" : hash1}
                data_encoded = urllib.urlencode(formdata)
                request = urllib2.Request('http://www.videoslasher.com/service/player/on-start', data_encoded) 
                response = urllib2.urlopen(request)
                ccontent = response.read()
                ckStr = cj['.videoslasher.com']['/']['authsid'].name+'='+cj['.videoslasher.com']['/']['authsid'].value
                playlisturl = re.compile('playlist: "(.+?)",').findall(link)[0]
                playlisturl = redirlink.split("/video/")[0]+playlisturl
                pcontent=postContent2(playlisturl,"",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink= re.compile(':content url="([^"]+)" type="video/x-flv" [^>]*>').findall(pcontent)[0]
                vidlink= ( '%s|Cookie="%s"' % (vidlink,ckStr) )
        #elif (redirlink.find("billionuploads") > -1):
        #        vidlink=resolve_billionuploads(redirlink,tmpcontent)
        #elif (redirlink.find("movreel") > -1):
        #        vidlink=resolve_movreel(redirlink,tmpcontent)
        elif (redirlink.find("jumbofiles") > -1):
                vidlink=resolve_jumbofiles(redirlink,tmpcontent)
        elif (redirlink.find("glumbouploads") > -1):
                vidlink=resolve_glumbouploads(redirlink,tmpcontent)
        elif (redirlink.find("sharebees") > -1):
                vidlink=resolve_sharebees(redirlink,tmpcontent)
        elif (redirlink.find("uploadorb") > -1):
                vidlink=resolve_uploadorb(redirlink,tmpcontent)
        elif (redirlink.find("vidhog") > -1):
                vidlink=resolve_vidhog(redirlink,tmpcontent)
        elif (redirlink.find("speedyshare") > -1):
                vidlink=resolve_speedyshare(redirlink,tmpcontent)
        elif (redirlink.find("180upload") > -1):
                vidcode = re.compile('180upload.com/(.+?)dk').findall(redirlink+"dk")[0] 
                urlnew= 'http://180upload.com/embed-'+vidcode+'.html'
                link=GetContent(urlnew)
                file_code = re.compile('<input type="hidden" name="file_code" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                embed_width = re.compile('<input type="hidden" name="embed_width" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                embed_height = re.compile('<input type="hidden" name="embed_height" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                test34 = re.compile('<input type="hidden" name="nwknj3" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"file_code":file_code,"referer":url,"embed_width":embed_width,"embed_height":embed_height,"nwknj3":test34})
                pcontent=postContent2(urlnew,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('/swfobject.js"></script><script type="text/javascript">(.+?)</script>').findall(pcontent)[0]
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                unpacked=unpacked.replace("\\","")
                vidlink = re.compile('addVariable\("file",\s*"(.+?)"\)').findall(unpacked)[0]
				
        else:
                if(redirlink.find("putlocker.com") > -1 or redirlink.find("sockshare.com") > -1):
                        redir = redirlink.split("/file/")
                        redirlink = redir[0] +"/file/" + redir[1].upper()
                sources = []
                label=name
                hosted_media = urlresolver.HostedMediaFile(url=redirlink, title=label)
                sources.append(hosted_media)
                source = urlresolver.choose_source(sources)
                print "inresolver=" + redirlink
                if source:
                        vidlink = source.resolve()

    dialog.close()
    return vidlink
               
def ListAZ(catname,mode):
        for character in AZ_DIRECTORIES:
                addDir(character,"http://www.vidics.ch/"+catname+"/Genre-Any/Letter-"+character+"/ByPopularity/1.htm",mode,"")

def getVideotype(url):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        ssoninfo= re.compile('<h3 class="season_header">(.+?)</h3>').findall(link)
        if(len(ssoninfo) > 0):
                return "tv"
        else:
                return "movie"

def DetermineVideotype(url):
        if(getVideotype(url)=="tv"):
                Seasons(url)
        else:
                Mirrors(url,"Movie")
				
def SEARCHMOV():
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = keyb.getText()
        SearchResult("movie",searchText)
		
def SEARCHTV():
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = keyb.getText()
        SearchResult("tv",searchText)
		
def SEARCHactor():
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = keyb.getText()
        SearchResult("actor",searchText)

def SearchResult(searchType,Searchtext):
	Searchtext=urllib.quote_plus(Searchtext)
	if searchType=="movie":
			INDEX("http://www.vidics.ch/Category-Movies/Genre-Any/Letter-Any/Relevancy/1/Search-"+urllib.quote_plus(Searchtext)+".htm",4,26,"movie")
	elif searchType=="actor":
			INDEX("http://www.vidics.ch/Category-People/Genre-Any/Letter-Any/Relevancy/1/Search-"+urllib.quote_plus(Searchtext)+".htm",11,12,"")
	else:
			INDEX("http://www.vidics.ch/Category-TvShows/Genre-Any/Letter-Any/Relevancy/1/Search-"+urllib.quote_plus(Searchtext)+".htm",7,27,"tv")
			
def getstatic():
        f = open(langfile, "r")
        langs = f.read()
        return langs
def postContent(url,data,referr):
    opener = urllib2.build_opener()
    opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                         ('Accept-Encoding','gzip, deflate'),
                         ('Referer', referr),
                         ('Content-Type', 'application/x-www-form-urlencoded'),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'),
                         ('Connection','keep-alive'),
                         ('Accept-Language','en-us,en;q=0.5'),
                         ('Pragma','no-cache'),
                         ('Host','player.phim47.com')]
    usock=opener.open(url,data)
    if usock.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(usock.read())
        f = gzip.GzipFile(fileobj=buf)
        response = f.read()
    else:
        response = usock.read()
    usock.close()
    return response
	
def GenreList(catname,mode):
        url="http://www.vidics.ch/"+catname+"/Genre-Any/Letter-Any/LatestFirst/1.htm"
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        listcontent=re.compile('<span class="dir">Genre</span>(.+?)</ul>').findall(newlink)
        if(len(listcontent) > 0):
                glist=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(listcontent[0])
                for vurl,vname in glist:
                    addDir(vname.strip(),strdomain+vurl,mode,"")
					
def ProfileMovie(url,typename):
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        listcontent=re.compile('<h3 class="career_type_title" ?[^>]*>'+typename+'(.+?)<tr>').findall(newlink)
        html_re = re.compile(r'<[^>]+>')
        if(len(listcontent) > 0):
                movielist=re.compile('<a class="green" [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(listcontent[0])
                for vurl,vname in movielist:
                    vname=html_re.sub('', vname)
                    addDirContext(vname.strip(),strdomain+vurl,13,"",plot="",vidtype="")
					
def ActorProfile(url):
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        listcontent=re.compile('<h3 class="career_type_title" id="(.+?)" ?[^>]*>(.+?)</h3>').findall(newlink)
        for profid,vtype in listcontent:
            addDir(vtype,url,14,"")
			
def postContent2(url,data,referr):
    req = urllib2.Request(url,data)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    data=response.read()
    response.close()
    return data
		
def SearchChannelresults(url,searchtext):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        vidlist=re.compile('<div class="thumb-container big-thumb">        <a href="(.+?)">          <img alt="(.+?)" class="thumb-design" src="(.+?)" />').findall(link)
        for vurl,vname,vimg in vidlist:
            vurl = vurl.split("/videos/")[0]
            addDir(vname.lower().replace("<em>"+searchtext+"</em>",searchtext),strdomain+vurl+"/videos",7,vimg)
        pagelist=re.compile('<div class="pagination">(.+?)</li>').findall(link)
        if(len(pagelist) > 0):
                navlist=re.compile('<a[^>]* href="(.+?)">(.+?)</a>').findall(pagelist[0])
                for purl,pname in navlist:
                    addDir("page " + pname.decode("utf-8"),strdomain+purl,13,"")
					

def Episodes(url,name):
    #try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        listcontent=re.compile('<div class="season season_[0-9]">(.+?)<br clear="all"\s*/>').findall(newlink)
        for listcontent2 in listcontent:
            if (listcontent2.find(">"+name+"</a></h3>") > -1):
                listcontent2=re.compile('>'+name+'</a></h3>(.+?)</div>').findall(listcontent2)[0]
                episodelist=re.compile('<a class="episode" [^s][^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(listcontent2)
                for (vurl,vname) in episodelist:
                     html_re = re.compile(r'<[^>]+>')
                     vname=html_re.sub('', vname)
                     addDir(vname,strdomain+vurl,4,"")
                break 

    #except: pass
	
def Seasons(url):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        ssoninfo= re.compile('<h3 class="season_header">(.+?)</h3>').findall(link)
        for seas in ssoninfo:
                epsodlist=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(seas)[0]
                addDir(epsodlist[1],url,8,"")
def INDEX(url,modenum,curmode,vidtype):
    #try:
        xbmc.executebuiltin("Container.SetViewMode(52)")
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        vcontent=re.compile('<td id="searchResults" [^>]*>(.+?)</td>').findall(newlink)
        listcontent=re.compile('<div itemscope [^>]*class="searchResult">(.+?)}</div></div></div>').findall(vcontent[0])
        vpot=""
        for moveieinfo in listcontent:
            vtitle,vurl,vimg,vtmp1,vtmp2=re.compile('<a title="Watch(.+?)online free." href="(.+?)"><img itemprop="image" src="(.+?)" title="(.+?)" alt="(.+?)" /></a>').findall(moveieinfo)[0]
            vtitle=RemoveHTML(vtitle)
            vpot=re.compile('"description":"(.+?)"').findall(moveieinfo)[0] 
            vpot=urllib.unquote_plus(vpot)
            if(vidtype==""):
                 addDir(vtitle,strdomain+vurl,modenum,vimg,vpot)
            else:
                 addDirContext(vtitle,strdomain+vurl,modenum,vimg,vpot,vidtype)
        paginacontent=re.compile('<table class="pagination" ?[^>]*>(.+?)</table>').findall(newlink)
        
        if(len(paginacontent)>0):
                pagelist=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(paginacontent[0])
                for vurl,vname in pagelist:
                    addDir("page: " + vname.replace("&rsaquo;",">").replace("&lsaquo;","<"),strdomain+vurl.replace(" ","%20"),curmode,"")
					
def INDEXList(url,modenum,curmode,vidtype):
    #try:
        xbmc.executebuiltin("Container.SetViewMode(52)")
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        listcontent=re.compile('<div itemscope [^>]*class="tvshow">(.+?)</td>').findall(newlink)
        vpot=""
        for moveieinfo in listcontent:
            vimg=re.compile('<img [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(moveieinfo)[0]
            urlcontent =re.compile('<h3>(.+?)</h3>').findall(moveieinfo)[0]
            titleurl=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(urlcontent)
            if(len(titleurl)>0):
                  vurl=titleurl[0][0]
                  vtitle=titleurl[0][1]
                  sumcontent=re.compile('</h3>(.+?)<span>').findall(moveieinfo)[0]
                  vsummary=re.compile('<div ?[^>]*>(.+?)</div>').findall(sumcontent)
            if(len(vsummary)>0):
                 vpot=vsummary[0]
            vtitle=RemoveHTML(vtitle)
            if(vidtype==""):
                 
                 addDir(vtitle,strdomain+vurl.replace("/People/",strdomain+"/People/").replace("/Category-People/",strdomain+"/Category-People/"),modenum,vimg,vpot)
            else:
                 addDirContext(vtitle,strdomain+vurl.replace("/People/",strdomain+"/People/").replace("/Category-People/",strdomain+"/Category-People/"),modenum,vimg,vpot,vidtype)
        paginacontent=re.compile('<table class="pagination" ?[^>]*>(.+?)</table>').findall(newlink)
        
        if(len(paginacontent)>0):
                pagelist=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(paginacontent[0])
                for vurl,vname in pagelist:
                    addDir("page: " + vname.replace("&rsaquo;",">").replace("&lsaquo;","<"),strdomain+vurl.replace(" ","%20"),curmode,"")
    #except: pass


	
#borrowed from pelisalacarta
def get_match(data,patron,index=0):
    matches = re.findall( patron , data , flags=re.DOTALL )
    return matches[index]

def unpackjs(texto):

    # Extract the function body
    patron = "eval\(function\(p\,a\,c\,k\,e\,d\)\{[^\}]+\}(.*?)\.split\('\|'\)\)\)"
    matches = re.compile(patron,re.DOTALL).findall(texto)

    
    # Separate code conversion table
    if len(matches)>0:
        data = matches[0]

    else:
        return ""

    patron = "(.*)'([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    cifrado = matches[0][0]
    descifrado = ""
    
    # Create the Dictionary with the conversion table
    claves = []
    claves.extend(["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
    claves.extend(["10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","1g","1h","1i","1j","1k","1l","1m","1n","1o","1p","1q","1r","1s","1t","1u","1v","1w","1x","1y","1z"])
    claves.extend(["20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","2g","2h","2i","2j","2k","2l","2m","2n","2o","2p","2q","2r","2s","2t","2u","2v","2w","2x","2y","2z"])
    claves.extend(["30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","3g","3h","3i","3j","3k","3l","3m","3n","3o","3p","3q","3r","3s","3t","3u","3v","3w","3x","3y","3z"])
    palabras = matches[0][1].split("|")
    diccionario = {}

    i=0
    for palabra in palabras:
        if palabra!="":
            diccionario[claves[i]]=palabra
        else:
            diccionario[claves[i]]=claves[i]
        i=i+1

    # Substitute the words of the conversion table
    # Retrieved from http://rc98.net/multiple_replace
    def lookup(match):
        try:
            return diccionario[match.group(0)]
        except:
            return ""

    # Reverse key priority for having the longest
    claves.reverse()
    cadenapatron = '|'.join(claves)
    compiled = re.compile(cadenapatron)
    descifrado = compiled.sub(lookup, cifrado)


    return descifrado
	
def unpackjs5(texto):

    # Extrae el cuerpo de la funcion
    matches = texto.split("return p}")
    if len(matches)>0:
        data = matches[1].split(".split")[0]
    else:
        return ""

    patron = "(.*)\"([^\"]+)\""
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)<2:
        matches=data.split(",'")
        cifrado = matches[0]+","
        palabras = "'"+matches[1]
        palabras = palabras.split("|")
    else:
        cifrado = matches[0][0]
        palabras = matches[0][1].split("|")
    descifrado = ""
    
    # Crea el dicionario con la tabla de conversion
    claves = []
    tipoclaves=0
    claves.extend(["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
    claves.extend(["10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","1g","1h","1i","1j","1k","1l","1m","1n","1o","1p","1q","1r","1s","1t","1u","1v","1w","1x","1y","1z"])
    claves.extend(["20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","2g","2h","2i","2j","2k","2l","2m","2n","2o","2p","2q","2r","2s","2t","2u","2v","2w","2x","2y","2z"])
    claves.extend(["30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","3g","3h","3i","3j","3k","3l","3m","3n","3o","3p","3q","3r","3s","3t","3u","3v","3w","3x","3y","3z"])
    
    diccionario = {}
   
    i=0
    for palabra in palabras:
        if palabra!="":
            
            diccionario[claves[i]]=palabra
        else:
            diccionario[claves[i]]=claves[i]
        i=i+1

    def lookup(match):
        try:
               retval=diccionario[match.group(0)]
        except:
                retval=""
        return retval

    claves.reverse()
    cadenapatron = '|'.join(claves)
    compiled = re.compile(cadenapatron)
    descifrado = compiled.sub(lookup, cifrado)

    return descifrado
	
def unpackjs4(texto):

    matches = texto.split("return p}")
    if len(matches)>0:
        data = matches[1].replace(".split(\"|\")))","")
    else:
        return ""

    patron = "(.*)\"([^\"]+)\""
    matches = re.compile(patron,re.DOTALL).findall(data)
    cifrado = matches[0][0]
    
    descifrado = ""
    
    claves = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","1g","1h","1i","1j","1k","1l","1m","1n","1o","1p","1q","1r","1s","1t","1u","1v","1w","1x","1y","1z"]
    palabras = matches[0][1].split("|")
    diccionario = {}
    i=0
    for palabra in palabras:
      try:
        if palabra!="":
            diccionario[claves[i]]=palabra
        else:
            diccionario[claves[i]]=claves[i]
      except: pass
      i=i+1


    def lookup(match):
        return diccionario[match.group(0)]


    claves.reverse()
    cadenapatron = '|'.join(claves)
    compiled = re.compile(cadenapatron)
    descifrado = compiled.sub(lookup, cifrado)

    return descifrado

def unpackjs3(texto,tipoclaves=1):

    
    patron = "return p\}(.*?)\.split"
    matches = re.compile(patron,re.DOTALL).findall(texto)

    if len(matches)>0:
        data = matches[0]
    else:
        patron = "return p; }(.*?)\.split"
        matches = re.compile(patron,re.DOTALL).findall(texto)
        if len(matches)>0:
            data = matches[0]
        else:
            return ""

    patron = "(.*)'([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    cifrado = matches[0][0]

    descifrado = ""
    
    # Create the Dictionary with the conversion table
    claves = []
    if tipoclaves==1:
        claves.extend(["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
        claves.extend(["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"])
    else:
        claves.extend(["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
        claves.extend(["10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","1g","1h","1i","1j","1k","1l","1m","1n","1o","1p","1q","1r","1s","1t","1u","1v","1w","1x","1y","1z"])
        claves.extend(["20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","2g","2h","2i","2j","2k","2l","2m","2n","2o","2p","2q","2r","2s","2t","2u","2v","2w","2x","2y","2z"])
        claves.extend(["30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","3g","3h","3i","3j","3k","3l","3m","3n","3o","3p","3q","3r","3s","3t","3u","3v","3w","3x","3y","3z"])
        
    palabras = matches[0][1].split("|")
    diccionario = {}

    i=0
    for palabra in palabras:

        if palabra!="":
            diccionario[claves[i]]=palabra
        else:
            diccionario[claves[i]]=claves[i]
        i=i+1

     # Substitute the words of the conversion table
     # Retrieved from http://rc98.net/multiple_replace
    def lookup(match):
        try:
            return diccionario[match.group(0)]
        except:
            return ""

     # Reverse key priority for having the longest
    claves.reverse()
    cadenapatron = '|'.join(claves)

    compiled = re.compile(cadenapatron)
    descifrado = compiled.sub(lookup, cifrado)

    descifrado = descifrado.replace("\\","")


    return descifrado
	
#borrowed from icefilms
def do_wait(source, account, wait_time):
     # do the necessary wait, with  a nice notice and pre-set waiting time. I have found the below waiting times to never fail.
     
     if int(wait_time) == 0:
         wait_time = 1
         
     if account == 'platinum':    
          return handle_wait(int(wait_time),source,'Loading video with your *Platinum* account.')
               
     elif account == 'premium':    
          return handle_wait(int(wait_time),source,'Loading video with your *Premium* account.')
             
     elif account == 'free':
          return handle_wait(int(wait_time),source,'Loading video with your free account.')

     else:
          return handle_wait(int(wait_time),source,'Loading video.')

def handle_wait(time_to_wait,title,text):

    print 'waiting '+str(time_to_wait)+' secs'    

    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create(' '+title)

    secs=0
    percent=0
    increment = float(100) / time_to_wait
    increment = int(round(increment))

    cancelled = False
    while secs < time_to_wait:
        secs = secs + 1
        percent = increment*secs
        secs_left = str((time_to_wait - secs))
        remaining_display = ' Wait '+secs_left+' seconds for the video stream to activate...'
        pDialog.update(percent,' '+ text, remaining_display)
        xbmc.sleep(1000)
        if (pDialog.iscanceled()):
             cancelled = True
             break
    if cancelled == True:     
         print 'wait cancelled'
         return False
    else:
         print 'done waiting'
         return True

def resolve_billionuploads(url,inhtml=None):

    #try:

        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving BillionUploads Link...')       
        dialog.update(0)
        
        print 'BillionUploads - Requesting GET URL: %s' % url
        if(inhtml==None):
               html = net.http_GET(url).content
        else:
               html = inhtml
        #They need to wait for the link to activate in order to get the proper 2nd page
        dialog.close()
        do_wait('Waiting on link to activate', '', 3)
        dialog.create('Resolving', 'Resolving BillionUploads Link...') 
        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            print '***** BillionUploads - Site reported maintenance mode'
            raise Exception('File is currently unavailable on the host')

        # Check for file not found
        if re.search('File Not Found', html):
            print '***** BillionUploads - File Not Found'
            raise Exception('File Not Found - Likely Deleted')  

        #New CloudFlare checks
        jschl=re.compile('name="jschl_vc" value="(.+?)"/>').findall(html)
        if jschl:
            jschl = jschl[0]    
        
            maths=re.compile('value = (.+?);').findall(html)[0].replace('(','').replace(')','')

            domain_url = re.compile('(https?://.+?/)').findall(url)[0]
            domain = re.compile('https?://(.+?)/').findall(domain_url)[0]
            
            time.sleep(5)
            
            normal = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            normal.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')]
            link = domain_url+'cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s'%(jschl,eval(maths)+len(domain))
            print 'BillionUploads - Requesting GET URL: %s' % link
            final= normal.open(domain_url+'cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s'%(jschl,eval(maths)+len(domain))).read()
            html = normal.open(url).read()
                    
        #Set POST data values
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)
        for name, value in r:
            data[name] = value
        
        #Captcha
        captchaimg = re.search('<img src="(http://BillionUploads.com/captchas/.+?)"', html)
       
        #If Captcha image exists
        if captchaimg:
            
            dialog.close()
            #Grab Image and display it
            img = xbmcgui.ControlImage(550,15,240,100,captchaimg.group(1))
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
            
            #Small wait to let user see image
            time.sleep(3)
            
            #Prompt keyboard for user input
            kb = xbmc.Keyboard('', 'Type the letters in the image', False)
            kb.doModal()
            capcode = kb.getText()
            
            #Check input
            if (kb.isConfirmed()):
              userInput = kb.getText()
              if userInput != '':
                  capcode = kb.getText()
              elif userInput == '':
                   Notify('big', 'No text entered', 'You must enter text in the image to access video', '')
                   return None
            else:
                return None
            wdlg.close()
            
            #Add captcha code to post data
            data.update({'code':capcode})
            
            #Re-create progress dialog
            dialog.create('Resolving', 'Resolving BillionUploads Link...') 

        #Some new data values
        data.update({'submit_btn':''})
        data.update({'geekref':'yeahman'})
             
        dialog.update(50)
        
        print 'BillionUploads - Requesting POST URL: %s DATA: %s' % (url, data)
        html = net.http_POST(url, data).content
        dialog.update(100)
        
        def custom_range(start, end, step):
            while start <= end:
                yield start
                start += step

        def checkwmv(e):
            s = ""
            
            # Create an array containing A-Z,a-z,0-9,+,/
            i=[]
            u=[[65,91],[97,123],[48,58],[43,44],[47,48]]
            for z in range(0, len(u)):
                for n in range(u[z][0],u[z][1]):
                    i.append(chr(n))
            #print i

            # Create a dict with A=0, B=1, ...
            t = {}
            for n in range(0, 64):
                t[i[n]]=n
            #print t

            for n in custom_range(0, len(e), 72):

                a=0
                h=e[n:n+72]
                c=0

                #print h
                for l in range(0, len(h)):            
                    f = t.get(h[l], 'undefined')
                    if f == 'undefined':
                        continue
                    a= (a<<6) + f
                    c = c + 6

                    while c >= 8:
                        c = c - 8
                        s = s + chr( (a >> c) % 256 )
            return s
        dll = re.compile('<input type="hidden" id="dl" value="(.+?)">').findall(html)[0]
        dl = dll.split('GvaZu')[1]
        print dl
        dl = checkwmv(dl)
        dl = checkwmv(dl)
        print 'Link Found: %s' % dl                

        return dl


    #except Exception, e:
    #    print '**** BillionUploads Error occured: %s' % e
    #    raise


def resolve_speedyshare(url,inhtml=None):

    try:    
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving SpeedyShare Link...')
        dialog.update(50)
        
        print 'SpeedyShare - Requesting GET URL: %s' % url
        if(inhtml==None):
               html = net.http_GET(url).content
        else:
               html = inhtml
        
        dialog.close()
        
        host = 'http://speedy.sh'
        #host = re.search("<input value='(http://www[0-9]*.speedy.sh)/.+?'", html).group(1)
        link = re.search("<a class=downloadfilename href='(.+?)'>", html).group(1)
        return host + link
    except Exception, e:
        print '**** SpeedyShare Error occured: %s' % e
        raise


def resolve_vidhog(url,inhtml=None):

    try:
        
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving VidHog Link...')
        dialog.update(0)
        
        print 'VidHog - Requesting GET URL: %s' % url
        if(inhtml==None):
               html = net.http_GET(url).content
        else:
               html = inhtml

        dialog.update(33)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            print '***** VidHog - Site reported maintenance mode'
            raise Exception('File is currently unavailable on the host')
        
        #Set POST data values
        op = re.search('<input type="hidden" name="op" value="(.+?)">', html).group(1)
        usr_login = re.search('<input type="hidden" name="usr_login" value="(.*?)">', html).group(1)
        postid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
        fname = re.search('<input type="hidden" name="fname" value="(.+?)">', html).group(1)
        method_free = re.search('<input type="submit" name="method_free" value="(.+?)" class="freebtn right">', html).group(1)
        
        data = {'op': op, 'usr_login': usr_login, 'id': postid, 'fname': fname, 'referer': url, 'method_free': method_free}
        
        print 'VidHog - Requesting POST URL: %s DATA: %s' % (url, data)
        html = net.http_POST(url, data).content
        
        dialog.update(66)
                
        #Set POST data values
        op = re.search('<input type="hidden" name="op" value="(.+?)">', html).group(1)
        postid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
        rand = re.search('<input type="hidden" name="rand" value="(.+?)">', html).group(1)
        method_free = re.search('<input type="hidden" name="method_free" value="(.+?)">', html).group(1)
        down_direct = int(re.search('<input type="hidden" name="down_direct" value="(.+?)">', html).group(1))
        wait = int(re.search('<span id="countdown_str">Wait <span id=".+?">([0-9]*)</span>', html).group(1))
        
        data = {'op': op, 'id': postid, 'rand': rand, 'referer': url, 'method_free': method_free, 'down_direct': down_direct}
        
        dialog.close()
        
        #Do wait time for free accounts    
        finished = do_wait('VidHog', '', wait)

        if finished:
            print 'VidHog - Requesting POST URL: %s DATA: %s' % (url, data)
            
            dialog.create('Resolving', 'Resolving VidHog Link...')
            dialog.update(66)
            
            html = net.http_POST(url, data).content
            
            dialog.update(100)
            
            dialog.close()
        
            link = re.search('<strong><a href="(.+?)">Click Here to download this file</a></strong>', html).group(1)
            return link
        else:
            return None
        
    except Exception, e:
        print '**** VidHog Error occured: %s' % e
        raise


def resolve_uploadorb(url,inhtml=None):

    try:

        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving UploadOrb Link...')       
        dialog.update(0)
        
        print 'UploadOrb - Requesting GET URL: %s' % url
        if(inhtml==None):
               html = net.http_GET(url).content
        else:
               html = inhtml
        
        dialog.update(33)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            print '***** UploadOrb - Site reported maintenance mode'
            raise Exception('File is currently unavailable on the host')

        #Set POST data values
        op = re.search('<input type="hidden" name="op" value="(.+?)">', html).group(1)
        usr_login = re.search('<input type="hidden" name="usr_login" value="(.*?)">', html).group(1)
        postid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
        fname = re.search('<input type="hidden" name="fname" value="(.+?)">', html).group(1)
        method_free = re.search('<input type="submit" name="method_free" value="(.+?)" class="btn2">', html).group(1)
        
        data = {'op': op, 'usr_login': usr_login, 'id': postid, 'fname': fname, 'referer': url, 'method_free': method_free}
        
        print 'UploadOrb - Requesting POST URL: %s DATA: %s' % (url, data)
        html = net.http_POST(url, data).content

        dialog.update(66)
        
        #Set POST data values
        op = re.search('<input type="hidden" name="op" value="(.+?)">', html).group(1)
        postid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
        rand = re.search('<input type="hidden" name="rand" value="(.+?)">', html).group(1)
        method_free = re.search('<input type="hidden" name="method_free" value="(.+?)">', html).group(1)
        down_direct = int(re.search('<input type="hidden" name="down_direct" value="(.+?)">', html).group(1))
        
        data = {'op': op, 'id': postid, 'rand': rand, 'referer': url, 'method_free': method_free, 'down_direct': down_direct}
        print data
        
        print 'UploadOrb - Requesting POST URL: %s DATA: %s' % (url, data)
        html = net.http_POST(url, data).content
        
        dialog.update(100)
        link = re.search('ACTION="(.+?)">', html).group(1)
        dialog.close()
        
        return link

    except Exception, e:
        print '**** UploadOrb Error occured: %s' % e
        raise


def resolve_sharebees(url,inhtml=None):

    try:
        
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving ShareBees Link...')       
        dialog.update(0)
        
        print 'ShareBees - Requesting GET URL: %s' % url
        if(inhtml==None):
               html = net.http_GET(url).content
        else:
               html = inhtml
        
        dialog.update(50)
        
        #Set POST data values
        #op = re.search('''<input type="hidden" name="op" value="(.+?)">''', html, re.DOTALL).group(1)
        op = 'download1'
        usr_login = re.search('<input type="hidden" name="usr_login" value="(.*?)">', html).group(1)
        postid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
        fname = re.search('<input type="hidden" name="fname" value="(.+?)">', html).group(1)
        method_free = "method_free"
        
        data = {'op': op, 'usr_login': usr_login, 'id': postid, 'fname': fname, 'referer': url, 'method_free': method_free}
        
        print 'ShareBees - Requesting POST URL: %s DATA: %s' % (url, data)
        html = net.http_POST(url, data).content
        
        dialog.update(100)

        link = None
        sPattern = '''<div id="player_code">.*?<script type='text/javascript'>(eval.+?)</script>'''
        r = re.search(sPattern, html, re.DOTALL + re.IGNORECASE)
        
        if r:
            sJavascript = r.group(1)
            sUnpacked = jsunpack.unpack(sJavascript)
            print(sUnpacked)
            
            #Grab first portion of video link, excluding ending 'video.xxx' in order to swap with real file name
            #Note - you don't actually need the filename, but for purpose of downloading via Icefilms it's needed so download video has a name
            sPattern  = '''("video/divx"src="|addVariable\('file',')(.+?)video[.]'''
            r = re.search(sPattern, sUnpacked)              
            
            #Video link found
            if r:
                link = r.group(2) + fname
                dialog.close()
                return link

        if not link:
            print '***** ShareBees - Link Not Found'
            raise Exception("Unable to resolve ShareBees")

    except Exception, e:
        print '**** ShareBees Error occured: %s' % e
        raise


def resolve_glumbouploads(url,inhtml=None):

    try:

        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving GlumboUploads Link...')       
        dialog.update(0)
        
        print 'GlumboUploads - Requesting GET URL: %s' % url
        if(inhtml==None):
               html = net.http_GET(url).content
        else:
               html = inhtml
        
        dialog.update(33)
        
        #Set POST data values
        op = 'download1'
        usr_login = re.search('<input type="hidden" name="usr_login" value="(.*?)">', html).group(1)
        postid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
        fname = re.search("""input\[name="fname"\]'\).attr\('value', '(.+?)'""", html).group(1)
        method_free = 'Free Download'
        
        data = {'op': op, 'usr_login': usr_login, 'id': postid, 'fname': fname, 'referer': url, 'method_free': method_free}
        
        print 'GlumboUploads - Requesting POST URL: %s DATA: %s' % (url, data)
        html = net.http_POST(url, data).content

        dialog.update(66)
        
        countdown = re.search('var cdnum = ([0-9]+);', html).group(1)

        #They need to wait for the link to activate in order to get the proper 2nd page
        dialog.close()
        do_wait('Waiting on link to activate', '', int(countdown))
        dialog.create('Resolving', 'Resolving GlumboUploads Link...') 
        dialog.update(66)

        #Set POST data values
        op = 'download2'
        rand = re.search('<input type="hidden" name="rand" value="(.+?)">', html).group(1)
        
        data = {'op': op, 'rand': rand, 'id': postid, 'referer': url, 'method_free': method_free, 'down_direct': 1}
        
        print 'GlumboUploads - Requesting POST URL: %s DATA: %s' % (url, data)
        html = net.http_POST(url, data).content
        
        dialog.update(100)
        link = re.search('This download link will work for your IP for 24 hours<br><br>.+?<a href="(.+?)">', html, re.DOTALL).group(1)
        dialog.close()
        
        return link

    except Exception, e:
        print '**** GlumboUploads Error occured: %s' % e
        raise

def resolve_jumbofiles(url,inhtml=None):

    try:

        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving JumboFiles Link...')       
        dialog.update(0)
        
        print 'JumboFiles - Requesting GET URL: %s' % url
        if(inhtml==None):
               html = net.http_GET(url).content
        else:
               html = inhtml
        
        dialog.update(33)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            print '***** JumboFiles - Site reported maintenance mode'
            raise Exception('File is currently unavailable on the host')

        #Set POST data values
        #op = re.search('<input type="hidden" name="op" value="(.+?)">', html).group(1)
        op = 'download1'
        postid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
        fname = re.search('<input type="hidden" name="fname" value="(.+?)">', html).group(1)
        #method_free = re.search('<input type="hidden" name="method_free" value="(.*?)">', html).group(1)
        method_free = 'method_free'
                
        data = {'op': op, 'id': postid, 'referer': url, 'method_free': method_free}
        
        print 'JumboFiles - Requesting POST URL: %s DATA: %s' % (url, data)
        html = net.http_POST(url, data).content

        dialog.update(66)

        #Set POST data values
        #op = re.search('<input type="hidden" name="op" value="(.+?)">', html).group(1)
        op = 'download2'
        postid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
        rand = re.search('<input type="hidden" name="rand" value="(.+?)">', html).group(1)
        method_free = 'method_free'
                
        data = {'op': op, 'id': postid, 'rand': rand, 'method_free': method_free}
        
        print 'JumboFiles - Requesting POST URL: %s DATA: %s' % (url, data)
        html = net.http_POST(url, data).content        

        dialog.update(100)        
        link = re.search('<FORM METHOD="LINK" ACTION="(.+?)">', html).group(1)
        dialog.close()
        
        return link

    except Exception, e:
        print '**** JumboFiles Error occured: %s' % e
        raise


def resolve_movreel(url,inhtml=None):

    try:

        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Movreel Link...')       
        dialog.update(0)
        
        print 'Movreel - Requesting GET URL: %s' % url
        if(inhtml==None):
               html = net.http_GET(url).content
        else:
               html = inhtml
        
        dialog.update(33)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            print '***** Movreel - Site reported maintenance mode'
            raise Exception('File is currently unavailable on the host')

        #Set POST data values
        op = re.search('<input type="hidden" name="op" value="(.+?)">', html).group(1)
        usr_login = re.search('<input type="hidden" name="usr_login" value="(.*?)">', html).group(1)
        postid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
        fname = re.search('<input type="hidden" name="fname" value="(.+?)">', html).group(1)
        method_free = re.search('<input type="submit" name="method_free" style=".+?" value="(.+?)">', html).group(1)
        
        data = {'op': op, 'usr_login': usr_login, 'id': postid, 'referer': url, 'fname': fname, 'method_free': method_free}
        
        print 'Movreel - Requesting POST URL: %s DATA: %s' % (url, data)
        html = net.http_POST(url, data).content

        #Check for download limit error msg
        if re.search('<p class="err">.+?</p>', html):
            print '***** Download limit reached'
            errortxt = re.search('<p class="err">(.+?)</p>', html).group(1)
            raise Exception(errortxt)

        dialog.update(66)
        
        #Set POST data values
        op = re.search('<input type="hidden" name="op" value="(.+?)">', html).group(1)
        postid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
        rand = re.search('<input type="hidden" name="rand" value="(.+?)">', html).group(1)
        method_free = re.search('<input type="hidden" name="method_free" value="(.+?)">', html).group(1)
        
        data = {'op': op, 'id': postid, 'rand': rand, 'referer': url, 'method_free': method_free, 'down_direct': 1}

        print 'Movreel - Requesting POST URL: %s DATA: %s' % (url, data)
        html = net.http_POST(url, data).content
        
        dialog.update(100)
        link = re.search('<a id="lnk_download" href="(.+?)">Download Original Video</a>', html, re.DOTALL).group(1)
        dialog.close()
        
        return link

    except Exception, e:
        print '**** Movreel Error occured: %s' % e
        raise
		
if os.path.isfile(db_dir)==False:
     initDatabase()
	 
def playVideo(url,name,movieinfo):
        vidurl=ParseVideoLink(url,name,movieinfo);
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(vidurl)
		
def RemoveHTML(strhtml):
            html_re = re.compile(r'<[^>]+>')
            strhtml=html_re.sub('', strhtml)
            return strhtml

def addDirContext(name,url,mode,iconimage,plot="",vidtype="", cm=[]):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&vidtype="+vidtype
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot": plot} )
        if(len(cm)==0):
                contextMenuItems = AddFavContext(vidtype, url, name, iconimage)
        else:
                contextMenuItems=cm
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    	
def addLink(name,url,mode,iconimage,movieinfo=""):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&movieinfo="+urllib.quote_plus(movieinfo)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
		
def addNext(formvar,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&formvar="+str(formvar)+"&name="+urllib.quote_plus('Next >')
        ok=True
        liz=xbmcgui.ListItem('Next >', iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": 'Next >' } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDir(name,url,mode,iconimage,plot=""):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot": plot} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

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



params=get_params()
url=None
name=None
mode=None
formvar=None
subtitleurl=None
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        formvar=int(params["formvar"])
except:
        pass		
try:
        subtitleurl=urllib.unquote_plus(params["suburl"])
except:
        pass
try:
        vidtype=urllib.unquote_plus(params["vidtype"])
except:
        pass
try:
        imageurl=urllib.unquote_plus(params["imageurl"])
except:
        pass
try:
        movieinfo=urllib.unquote_plus(params["movieinfo"])
except:
        pass
		
sysarg=str(sys.argv[1]) 

print "currentmode" + str(mode)
if mode==None or url==None or len(url)<1:
        HOME()
elif mode==2:

        ListGenres(url,name) 
elif mode==3:
        playVideo(url,name,movieinfo)
elif mode==4:
        Mirrors(url,name) 
elif mode==5:
        INDEXList(url,4,5,"movie")
elif mode==6:
        INDEXList(url,7,6,"tv")
elif mode==7:
        Seasons(url)
elif mode==8:
        Episodes(url,name)
elif mode==9:
        SEARCHMOV()
elif mode==10:
        SEARCHTV()
elif mode==11:
        ActorProfile(url)
elif mode==12:
        INDEX(url,11,12,"")
elif mode==13:
        DetermineVideotype(url)
elif mode==14:
        ProfileMovie(url,name)
elif mode==15:
        SEARCHactor()
elif mode==16:
        ListAZ(url,26)
elif mode==17:
        ListAZ(url,27)
elif mode==18:
        GenreList(url,26)
elif mode==19:
        GenreList(url,27)
elif mode==20:
        List4Days()
elif mode==21:
        getSchedule(url)
elif mode==22:
        SaveFav(vidtype, name, url, imageurl)
elif mode==23:
        DeleteFav(name,url)
elif mode==24:
        ListFavorites()
elif mode==25:
        BrowseFavorites(url)
elif mode==26:
        INDEX(url,4,26,"movie")
elif mode==27:
        INDEX(url,7,27,"tv")
elif mode==28:
        SearchResult(url,name)

xbmcplugin.endOfDirectory(int(sysarg))
