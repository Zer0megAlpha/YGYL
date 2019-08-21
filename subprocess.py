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

if __name__ == '__main__':
##    textFile = codecs.open('metadata.txt', 'a', encoding='utf-8', errors='ignore')
##    textFile.close()
##    subprocess.call(['ffmpeg', '-i', 'C:/Users/Vyourtchenko/Desktop/wsg/992673/1454034775064.webm', '-f', 'ffmetadata ', 'C:/Users/Vyourtchenko/Desktop/VLC_NowPlaying_v1.5.0/media_list/metadata.txt'], shell=True)
##    with open('C:/Users/Vyourtchenko/Desktop/VLC_NowPlaying_v1.5.0/media_list/metadata.txt', 'r') as f:
##        lines = f.readlines()
##    for line in lines:
##        print(line)

    #cmd="ffmpeg -i C:/Users/Vyourtchenko/Desktop/wsg/992673/1454034775064.webm -f ffmetadata C:/Users/Vyourtchenko/Desktop/VLC_NowPlaying_v1.5.0/media_list/metadata.txt"
    #path = 'ffprobe -v quiet -of json -show_format "C:/Users/Vyourtchenko/Desktop/wsg/992673/'
    #for
    cmd='ffprobe -v quiet -of json -show_format "C:/Users/Vyourtchenko/Desktop/wsg/992673/Trump can can make america great again.webm"'
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=False)
##    print(process.stdout)
    ffprobe_out, err = process.communicate()
    ffprobe_dict = json.loads(ffprobe_out)
    print(ffprobe_dict['format']['tags'])
    for tag in ffprobe_dict['format']['tags']:
        if tag != 'encoder' and tag != 'creation_time':
            print(ffprobe_dict['format']['tags'][tag])
##        if tag != ffprobe_dict['format']['tags']['encoder']:
##            print(tag)
##    print(ffprobe_dict['format']['tags'])
    #for line in process.stdout:
        #print(line)

##    ffprobe_cmd = 'ffprobe C:/Users/Vyourtchenko/Desktop/wsg/992673/1454034775064.webm -v quiet -print_format json -show_format -show_streams'
    # print ffprobe_cmd        
##    s = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
##    ffprobe_out, err = s.communicate()
##    ffprobe_dict = json.loads(ffprobe_out)
##    print(ffprobe_dict)

    #metadata=FFProbe('C:/Users/Vyourtchenko/Desktop/wsg/992673/1454034775064.webm')
    #for stream in metadata.streams:
        


#ffmpeg -i C:\Users\Vyourtchenko\Desktop\wsg\992673\1454034775064.webm -f ffmetadata C:\Users\Vyourtchenko\Desktop\VLC_NowPlaying_v1.5.0\media_list\metadata.txt
