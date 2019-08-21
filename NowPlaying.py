#!/usr/bin/env python
#===============================================================================
# title           :NowPlaying.py
# description     :This script will create a NowPlaying.txt file that contains
#                   the info for the song that is currently being played via VLC
# author          :Tipher88
# contributors    :AbyssHunted, Etuldan
# date            :20160708
# version         :1.5.0
# usage           :python NowPlaying.py
# notes           :For this script to work you need to follow the instructions
#                   in the included README.txt file
# python_version  :2.7.10 & 3.4.3
#===============================================================================

import os, time, datetime, requests, codecs
import xml.etree.ElementTree as ET
import vlc
from random import shuffle
from os import walk
import json, subprocess
from ffprobe3 import FFProbe
#import Popen
from urllib.parse import unquote
#from tinytag import TinyTag
#import eyed3
#import songdetails
#from glob import glob

try:
    # Python 2.6-2.7 
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser

# Global variable to keep track of song info being printed and check for changes
currentSongInfo = ''

def getInfo():
    # CUSTOM: Separator can be changed to whatever you want
    separator = '   |   '
    
##    nowPlaying = 'UNKNOWN'
##    songTitle = 'UNKNOWN'
##    songArtist = 'UNKNOWN'
    fileName = ''
    length = 0
    time = 0
    
    s = requests.Session()
    
    # CUSTOM: Username is blank, just provide the password
    s.auth = ('', '4chan')
    
    # Attempt to retrieve song info from the web interface
    try:
        r = s.get('http://localhost:8080/requests/status.xml', verify=False)
        
        if('401 Client error' in r.text):
            print('Web Interface Error: Do the passwords match as described in the README.txt?')
            return
    except:
        print('Web Interface Error: Is VLC running? Did you enable the Web Interface as described in the README.txt?')
        return
    
    # Okay, now we know we have a response with our xml data in it
    # Save the response data
    root = ET.fromstring(r.content)

    
##    vid_length = root.iter('length')
##    for i in vid_length:
##        length = i.text
##
##    vid_time = root.iter('time')
##    for i in vid_time:
##        time = i.text
    
    # Loop through all info nodes to find relevant metadata
    for info in root.iter('info'):
        # Save the name attribute of the info node
        name = info.get('name')
        
        # See if the info node we are looking at is now_playing
##        if(name == 'now_playing'):
##            nowPlaying = info.text
##        else:
            # See if the info node we are looking at is for the artist
##            if(name == 'artist'):
##                songArtist = info.text
            
        # See if the info node we are looking at is for the title
        if(name == 'title'):
            songTitle = info.text
        
        # See if the info node we are looking at is for the filename
        if(name == 'filename'):
            fileName = info.text
            print(fileName)
            fileName = os.path.splitext(fileName)[0]
    # END: for info in root.iter('info')
    
    # If the now_playing node exists we should use that and ignore the rest
##    if(nowPlaying != 'UNKNOWN'):
##        writeSongInfoToFile(nowPlaying, separator)
##    else:
        # Make sure a songTitle and songArtist was found in the metadata
##        if(songTitle != 'UNKNOWN' and
##           songArtist != 'UNKNOWN'):
##            # Both songTitle and song Artist have been set so use both
##            writeSongInfoToFile('%s - %s' % (songTitle, songArtist), separator)
##        elif( songTitle != 'UNKNOWN' ):
##            # Just use the songTitle
##            writeSongInfoToFile(songTitle, separator)
    if( fileName != '' ):
        # Use the fileName as a last resort
        writeSongInfoToFile(fileName, separator)
    else:
        # This should print 'UNKNOWN - UNKNOWN' because no relevant metadata was
        #   found
        writeSongInfoToFile('%s - %s' % (songTitle, songArtist), separator)
# END: getInfo()

def writeSongInfoToFile( songInfo, separator ):
    global currentSongInfo
    htmlParser = HTMLParser()
    
    if(currentSongInfo != songInfo):
        currentSongInfo = songInfo
        print(htmlParser.unescape(currentSongInfo))
    
        # CUSTOM: The output file name can be changed
        textFile = codecs.open('NowPlaying.txt', 'w', encoding='utf-8', errors='ignore')
        textFile.write(htmlParser.unescape(currentSongInfo + separator))
        textFile.close()
        
        timeStamp = '{:%H:%M:%S}:'.format(datetime.datetime.now())
    
        # CUSTOM: The output file name can be changed
        textFile = codecs.open('NowPlaying_History.txt', 'a', encoding='utf-8', errors='ignore')
        textFile.write(htmlParser.unescape(('%s %s%s') % (timeStamp, currentSongInfo, os.linesep)))
        textFile.close()
# END: writeSongInfoToFile( songInfo, separator )

if __name__ == '__main__':
    path = 'C:\\Users\\Vyourtchenko\\Desktop\\wsg'
    playing = set([1,2,3,4])
    Instance = vlc.Instance('--play-and-exit', '--video-on-top', '--mouse-hide-timeout=0')
    list_player = Instance.media_list_player_new()
    while 1:
        music_folder=[]
        if os.path.isdir(path):
            for folder in next(os.walk(path))[1]:
                music_folder.append(folder)
            shuffle(music_folder)

        for folder in music_folder:
            file_list=[]
            for (dirpath, dirnames, filenames) in walk(path):#files in folder:
                file_list.extend(filenames)

            webm_files=[]
            for file in file_list:
                if file.endswith('.webm'):
                    webm_files.append(path + '\\' + folder + '\\' + file)
            shuffle(webm_files)

##            textFile = codecs.open('media_playlist.m3u', 'w', encoding='utf-8', errors='ignore')
##            for webm in webm_files:
##                print(webm)
##                textFile.write(webm + '\n')
##            textFile.close()

##            while True:
##                state = list_player.get_state()
##                if state not in playing:
##                    break
##                continue

            Media_list = Instance.media_list_new(webm_files)
            list_player.set_media_list(Media_list)
            #list_player.set_fullscreen(True)
            list_player.play()

            started = list_player.get_state()
            t0 = time.time()
            while started not in playing:
                started = list_player.get_state()
                t1 = time.time()
                if((t1-t0)>3):
                    print('Something went wrong')
                    break

            while True:
                state = list_player.get_state()
                #time.sleep(9)
                #getInfo()
                print('\n')
                print(str(int(list_player.get_media_player().get_time()/1000)) + '/' + str(int(list_player.get_media_player().get_length()/1000)))
                #print(list_player.get_media_player().get_title())
                link = unquote(list_player.get_media_player().get_media().get_mrl())
                #print(link)
                #textFile = codecs.open('metadata.txt', 'a', encoding='utf-8', errors='ignore')
                #textFile.close()
                print(link[8:])
                #replaceStr = link[8:].replace('/', '//')
                #print(replaceStr)
                #print('C:\\Users\\Vyourtchenko\\Desktop\\VLC_NowPlaying_v1.5.0\\media_list\\metadata.txt')
                #subprocess.call(['ffmpeg', '-i', replaceStr, '-f', 'ffmetadata ', 'C:/Users/Vyourtchenko/Desktop/VLC_NowPlaying_v1.5.0/media_list/metadata.txt'], shell=True)
                #subprocess.call('ffmpeg -i ' + link[8:] + ' -f ffmetadata C:/Users/Vyourtchenko/Desktop/output.txt', shell=True)
                #time.sleep(1)
                #with open('C:/Users/Vyourtchenko/Desktop/output.txt', 'r') as f:
                #with open('C:/Users/Vyourtchenko/Desktop/VLC_NowPlaying_v1.5.0/media_list/metadata.txt', 'r') as f:
                #    lines = f.readlines()
                #    for line in lines:
                #        print(line)
                        #if 'title=' in line:
                            #print(line[5:])

                cmdFileStr = '"' + link[8:] + '"'
                cmd="ffprobe -v quiet -of json -show_format " + cmdFileStr
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=False)
                ffprobe_out, err = process.communicate()
                ffprobe_dict = json.loads(ffprobe_out)
                for tag in ffprobe_dict['format']['tags']:
                    if tag != 'encoder':
                        print(ffprobe_dict['format']['tags'][tag])
                time.sleep(1)
                

                
                #webm_file = TinyTag.get('C:\\Users\\Vyourtchenko\\Desktop\\wsg\\992673\\1454034775064.webm')#link[8:])
                #print(webm_file.title)

##                Instance2 = vlc.Instance()
##                player2 = Instance2.media_player_new()
##                webm_titled = Instance2.media_new(link)
##                player2.set_media(webm_titled)
##                webm_titled.parse()
                #player2.play()
##                time.sleep(1)
##                print(webm_titled.get_tracks_info())
##                print(player2.video_get_title_description())
##                print(player2.get_title())
                #print(player2.get_full_title_descriptions())
                
                

                #print(list_player.get_media_player().get_media().#get_user_data())#tracks_get())#video_get_title_description())
                #print(list_player.get_media_player().get_media().get_meta())
                #print(list_player.get_media_player().get_media().get_user_data())
                #print(Instance.vlm_get_media_instance_title(link, list_player.get_media_player().get_media()))
                #print(Instance.vlm_show_media(os.path.splitext(link)[0]))
                #print(list_player.get_media_player().get_media().get_tracks_info())
                #print(Media_list.media().)
                #print(list_player.get_media_player().get_media_details())
                #print(list_player.get_media_player().video_get_title_description())
                #print(list_player.get_media_player().video_get_track_description())
                if state not in playing:
                    break
                continue


##            for webm in webm_files:
##                media=Instance.media_new(file_path)
##
##                media.get_mrl()
##                player.set_media(media)
##                player.set_fullscreen(True)
##                player.play()
##                playing = set([1,2,3,4])
##                time.sleep(1)
##                duration = player.get_length() / 1000
##                mm, ss = divmod(duration, 60)
##                print(str(mm) + ':' + str(ss))
##
##                while True:
##                    state = player.get_state()
##                    if state not in playing:
##                        break
##                    continue

                #cmd = 'vlc.exe --started-from-file --playlist-enqueue "' + file_path + '"'
                #print(cmd)
                #p = Popen(cmd)
                #getInfo()
                #time.sleep(5)

        
##        for dirs in next(os.walk('C:\\Users\\Vyourtchenko\\Desktop\\wsg'))[1]:
        #for dirs in shuffle(glob('E:\\media\\USB\\YGYL\\wsg\\*/')):
##            for files in shuffle(dirs):
##                if files.endswith('.webm'):
##                    player = vlc.MediaPlayer(files)
##                    player.play()
##                    getInfo()
        
        # CUSTOM: Sleep for a number of seconds before checking again
        #time.sleep(5)
# END: if __name__ == '__main__'


#loop through all folders
#   add files
#   writeSongInfoToFile
#   

#getInfo runs each time a new file is made to play.
#getInfo will have a loop through the lines of the comment so it'll take the whole song to display.
