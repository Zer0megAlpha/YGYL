import os
import re
import io
import requests
import urllib.request
import sys
import codecs
from pathlib import Path
import json, subprocess
from ffprobe3 import FFProbe
from bs4 import BeautifulSoup;

#things to do
#1. DONE setup loop over pages of board
#2. DONE setup loop over all boards
#3. DONE setup adjustment of folders for boards
#4. DONE setup adjustment of cuttoff i[22:] = 3 character board name /gif/
#5. DONE setup .txt log of all links used and all thread links in respective folders
#6. DONE download the comments for unknown source material
#7. NOT DOING THIS ask the user if they want to stop at a certain memory limit
#8. DONE update entire folder with new stuff
#9. NOT DOING THIS ask what file formats should be downloaded
#10. NOT DOING THIS ask what to search
#11. DONE Look up thread link to 4chan, if it's been catalogued then do it if not then don't
#12. DONE Setup txt for what the last checked page is
#13. NOT DOING THIS 4chan bans threads but yuki.la archives them anyway. How to mitigate this?
#14. DONE change download so that it can rename files that have already used names
#15. NOT DOING THIS Make a temporary switch to update the comments for every webm so that no duplicate comments show
#16. DONE Use full webm name in comments
#17. DONE Fix comments setup
#18. I THINK THIS IS DONE Fix the comments that don't post unicode.

#if thread folder already exists then alreadyExists = True
#do not make a new folder. BoardThreads.txt is not updated.
#comb over each link in html. if path exists for link.webm then don't add link to listOfLinks.txt
#if anon id exists in comments, don't add comment into Comment.txt


#YGYL {
#   gif {
#       BoardThreads.txt
#       1234567 {
#           threadLinkAndWebmLinks.txt
#           Comments.txt
#           1012345
#           1012346
#           ...
#       }
#       1234568
#       ...
#   }
#   wsg
#   ...
#}

def main():
    #findInBoard('wsg')
    findInAllBoards()
    
def findInBoard(msgboard):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    path = '/media/USB'
    path = path + '/YGYL'
    
    if not os.path.exists(path):
        try:
            os.mkdir(path)
            print('Made new directory to save YGYL.')
        except:
            print("Unable to create path\nIt may already exist.")


    boardFolder = path + '/' + msgboard
    if not os.path.exists(boardFolder):
        try:
            os.makedirs(boardFolder)
            print('Made new directory to save YGYL board.')
        except:
            print("Unable to create path\nIt may already exist.")

    lastPage = boardFolder + '/LastPage.txt'
    if(os.path.exists(lastPage)):
        o = io.open(lastPage, 'r')
        num = int(o.read())
        o.close()
    else:
       #623 for testing
       num = 1
    print('Starting from ' + str(num))

    g = io.open(boardFolder + '/' + msgboard + 'Threads.txt','a')

    sub_url = 'https://yuki.la/' + msgboard + '/page/' + str(num)
    print(sub_url)
    webm_request = requests.get(sub_url);
    webm_instance = BeautifulSoup(webm_request.text, 'html.parser');    

    while(webm_instance.find("div", class_="paging") != None):

        for foo in webm_instance.find_all('div', attrs={'class': 'post op'}):
            openLink = 0

            postID = (foo.find('a', attrs={'title': 'Reply to this post'})).text
            print('\n\nPostID: ' + postID)

            foosub = foo.find('div', attrs={'class': 'postInfo desktop'})
            name = (foo.find('span', attrs={'class': 'name'})).text
            print('Username: ' + name)
            name = name.upper()

            foosub = foo.find('div', attrs={'class': 'postInfo desktop'})
            subject = (foosub.find('span', attrs={'class': 'subject'})).text
            if subject is not None:
                print('Subject: ' + subject)
            subject = subject.upper()
                
            quote = (foo.find('blockquote', attrs={'class': 'postMessage'})).text
            if quote is not None:
                print('Blockquote: ' + quote)
            quote = quote.upper()


            if(findInNameSubjectQuote(name) or findInNameSubjectQuote(subject) or findInNameSubjectQuote(quote)):
                openLink = 1
            
            if(openLink == 1):
                print('\nFound another YGYL thread.')
                sub_url = 'https://yuki.la/' + msgboard + '/' + postID

                isSubURL = False
                with io.open(boardFolder + '/' + msgboard + 'Threads.txt') as subURLTester:
                    subURLTest = subURLTester.readlines()
                    for line in subURLTest:
                        if sub_url in line:
                            isSubURL = True

                new_webm_request = requests.get(sub_url);
                new_webm_instance = BeautifulSoup(new_webm_request.text, 'html.parser');

                isArchived = False
                
                sub_url_4chan = 'https://boards.4chan.org/' + msgboard + '/thread/' + postID
                
                webm_request_4chan = requests.get(sub_url_4chan);
                webm_instance_4chan = BeautifulSoup(webm_request_4chan.text, 'html.parser');    

                if isSubURL == False:
                    g.write(sub_url + '\n\n')
                else:
                    print('Not a new thread.\n')
                print(sub_url)
                
                #change find to findAll for both parts
                if(webm_instance_4chan.find(text='404 Not Found') != None):
                    print('Thread is archived.\n')
                    isArchived = True
                elif(webm_instance_4chan.find("div", class_="closed") != None):
                    print('Thread is closed.\n')
                    isArchived = True
                

                if(isArchived == True):
                    newFolder = boardFolder + '/' + postID
                    if not os.path.exists(newFolder):
                        try:
                            os.makedirs(newFolder)

                            print('Made new directory to save YGYL thread.')
                        except:
                            print('Unable to create path\nIt may already exist.')

                    print(newFolder)


                    f = io.open(newFolder + '/Links.txt','a',encoding='utf8')
                    initialExists = False
                    with io.open(newFolder + '/Links.txt',encoding='utf8') as initalTester:
                        initialTest = initalTester.readlines()
                        for line in initialTest:
                            if sub_url in line:
                                initialExists = True
                    if initialExists == False:
                        f.write(sub_url + '\n\n')
                    f.close()

                    if not os.path.exists(newFolder + '/Comments.txt'):                        
                        w = io.open(newFolder + '/Comments.txt','w',encoding='utf8')

                        op = new_webm_instance.find('div', attrs={'class': 'post op'})
                        opFile = op.find('a', attrs={'target': '_blank'})
                        if(opFile.has_attr('title')):
                            opFileText = opFile['title'].translate(non_bmp_map)
                        else:
                            opFileText = opFile.text.translate(non_bmp_map)

                        opTitle = op.find('span', class_='subject')
                        opTitleText = opTitle.text.translate(non_bmp_map)
                        if(opTitleText != ''):
                            opTitleText += '\n'

                        opName = op.find('span', class_='name')
                        opNameText = opName.text.translate(non_bmp_map)
                        opID = op.find('a', attrs={'title': 'Reply to this post'})
                        opIDText = opID.text
                        opPost = op.find('blockquote', class_='postMessage')
                        opPostText = replaceBr(opPost).translate(non_bmp_map)

                            
                        w.write(str(opFileText + '\n' + opTitleText + opNameText + ' No.' + opIDText + '\n' + opPostText + '\n\n'))


                        for rep in new_webm_instance.find_all('div', attrs={'class': 'post reply'}):
                            repFindFile = rep.find('div', class_='fileText')
                            if repFindFile != None:
                                repFile = repFindFile.find('a', attrs={'target': '_blank'})
                                if(repFile.has_attr('title')):
                                    repFileText = repFile['title'].translate(non_bmp_map) + '\n'
                                else:
                                    repFileText = repFile.text.translate(non_bmp_map) + '\n'
                            else:
                                repFileText = ''
                            repName = rep.find('span', class_='name')
                            repNameText = repName.text.translate(non_bmp_map)
                            repID = rep.find('a', attrs={'title': 'Reply to this post'})
                            repIDText = repID.text
                            repPost = rep.find('blockquote', class_='postMessage')
                            repPostText = replaceBr(repPost).translate(non_bmp_map)
                            if(repPostText != ''):
                                repPostText = '\n' + repPostText

                            w.write(str(repFileText + repNameText + ' No.' + repIDText + repPostText + '\n\n'))

                        w.close()
                                        
                    for webm in new_webm_instance.find_all("div", class_="fileText"):

                        with io.open(newFolder + '/Links.txt',encoding='utf8') as tester:
                            testerRead = tester.readlines()
                        
                        
                        title = webm.find('a', attrs={'target': '_blank'})
                        if(title.has_attr('title')):
                            titleText = title['title'].translate(non_bmp_map)
                        else:
                            titleText = title.text.translate(non_bmp_map)
                        
                        link = ('https:' + title['href'])

                        if(link.endswith('.webm')):
                            fullFilename = os.path.join(newFolder, titleText)

                            foundInLinks = False
                            for line in testerRead:
                                if link in line:
                                    foundInLinks = True
                            if foundInLinks == False:
                                print('\n' + str(titleText))

                                #individual comment string
                                c = io.open(newFolder + '/' + titleText + '.txt','w',encoding='utf8')

                                opCom = new_webm_instance.find('div', attrs={'class': 'post op'})
                                opComID = opCom.find('a', attrs={'title': 'Reply to this post'})
                                opComIDText = opComID.text

                                
                                commentID = webm['id'][2:]
                                commentIDText = commentID

                                if commentIDText == opComIDText:

                                    opComFileText = titleText.translate(non_bmp_map)

                                        
                                    opComTitle = opCom.find('span', class_='subject')
                                    opComTitleText = opComTitle.text.translate(non_bmp_map)
                                    opComName = opCom.find('span', class_='name')
                                    opComNameText = opComName.text.translate(non_bmp_map)

                                    opComPost = opCom.find('blockquote', class_='postMessage')
                                    if opComPost != None:
                                        opComPostText = '\n' + replaceBr(opComPost).translate(non_bmp_map)
                                    else:
                                        opComPost = ''
                                    if opComTitleText != '':
                                        opComTitleText += '\n'

                                    #print(str(opComFileText) + ' TESTING')
                                    c.write(str(opComFileText + ' = ' + link + '\n' + opComTitleText + opComNameText + ' No.' + opComIDText + opComPostText + '\n\n'))
                                    d = io.open(newFolder + '/threadTopic.txt','w',encoding='utf8')
                                    d.write(str(opComTitleText + opComNameText + opComPostText))
                                    d.close()

                                else:

                                    repPostInfoCommMes = 'm' + commentIDText
                                    repPostInfoCommName = 'pi' + commentIDText

                                    repCommMes = new_webm_instance.find('blockquote', attrs={'id': repPostInfoCommMes})
                                    repCommName = new_webm_instance.find('div', attrs={'id': repPostInfoCommName})

                                    repComFileText = titleText.translate(non_bmp_map)

                                    repComName = repCommName.find('span', class_='name')
                                    repComNameText = repComName.text.translate(non_bmp_map)

                                    repComIDText = commentIDText
                                    repComPost = repCommMes
                                    if repComPost != None:
                                        repComPostText = '\n' + replaceBr(repComPost).translate(non_bmp_map)
                                    else:
                                        repComPostText = ''

                                    #print(repComFileText + ' TESTING')
                                    c.write(str(repComFileText + ' = ' + link + '\n' + repComNameText + ' No.' + repComIDText + repComPostText + '\n\n'))


                                global commentIDs
                                commentIDs = []
                                c.write(str(returnComments(commentIDText, new_webm_instance, non_bmp_map)))
                                c.close()


                                print('Downloading ' + fullFilename)
                                if os.path.exists(fullFilename):
                                    print('\nAlready exists, so renaming it.')
                                    difNum = 1
                                    while(os.path.exists(fullFilename[:-5] + ' (' + str(difNum) + ').webm')):
                                        difNum += 1
                                    
                                    fullFilename = fullFilename[:-5] + ' (' + str(difNum) + ')' + '.webm'
                                    print(fullFilename)
                                ifCanDownload = True
                                try:
                                    urllib.request.urlretrieve(link, fullFilename)
                                except Exception:
                                    print('Failed first try.')
                                    try:
                                        urllib.request.urlretrieve(link, fullFilename)
                                    except Exception:
                                        print('Failed second try.')
                                        try:
                                            urllib.request.urlretrieve(link, fullFilename)
                                        except Exception:
                                            print('Failed third try. Moving on.')
                                            ifCanDownload = False
                                            try:
                                                testConnection = requests.get(sub_url);
                                            except Exception:
                                                print('Connection failed.')
                                                return
                                if ifCanDownload == True:
                                    s = io.open(newFolder + '/Links.txt','a',encoding='utf8')
                                    s.write(str(titleText + ' = ' + link + '\n\n'))
                                    s.close()
                                
                                
                            else:
                                print(fullFilename + ' is already downloaded. Moving on.')

                            filePath = newFolder + '/' + titleText    
                            fileMetadataPath = filePath + '.metadata.txt'
                            if not os.path.exists(fileMetadataPath):
                                
                                #write metadata into file
                                cmd='ffprobe -v quiet -of json -show_format "' + filePath + '"'
                                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=False)
                                ffprobe_out, err = process.communicate()
                                ffprobe_dict = json.loads(ffprobe_out)
                                metaData = ''
                                for tag in ffprobe_dict['format']['tags']:
                                    if tag != 'encoder' and tag != 'creation_time':
                                        metaData += ffprobe_dict['format']['tags'][tag] + '\n'
                                if(metaData != ''):
                                    c = io.open(fileMetadataPath,'w',encoding='utf8')
                                    c.write(str(metaData));
                                    c.close()
                    
                else:
                    print('Thread is not archived, thus will stop.\nThread is not archived, thus will stop.\nThread is not archived, thus will stop.\nThread is not archived, thus will stop.\nThread is not archived, thus will stop.\n')

                    print('Ended on page ' + str(num))
                    g.close()
                    return

        num += 1
        i = io.open(lastPage,'w',encoding='utf8')
        i.truncate()

        i.write(str(num))
        i.close()

        sub_url = 'https://yuki.la/' + msgboard + '/page/' + str(num)
        print('\n\n\n' + sub_url + '\n\n\n')
        webm_request = requests.get(sub_url);
        webm_instance = BeautifulSoup(webm_request.text, 'html.parser');

    g.close()

def findInAllBoards():
    boards = ['wsg', 'gif']
    #['3', 'a', 'aco', 'adv', 'an', 'asp', 'bant', 'biz', 'c', 'cgl', 'ck', 'cm', 'co', 'con', 'd', 'diy', 'e', 'fa', 'fit', 'g', 'gd', 'gif', 'h', 'hc', 'his', 'hm', 'hr', 'i', 'ic', 'int', 'jp', 'k', 'lgbt', 'lit', 'm', 'mlp', 'mu', 'n', 'news', 'o', 'out', 'p', 'po', 'pol', 'q', 'qa', 'qst', 'r', 'r9k', 's', 's4s', 'sci', 'soc', 'sp', 't', 'tg', 'toy', 'trv', 'tv', 'u', 'v', 'vg', 'vip', 'vp', 'vr', 'w', 'wg', 'wsg', 'wsr', 'x', 'y']
    #['/3/', '/a/', '/aco/', '/adv/', '/an/', '/asp/', '/bant/', '/biz/', '/c/', '/cgl/', '/ck/', '/cm/', '/co/', '/con/', '/d/', '/diy/', '/e/', '/fa/', '/fit/', '/g/', '/gd/', '/gif/', '/h/', '/hc/', '/his/', '/hm/', '/hr/', '/i/', '/ic/', '/int/', '/jp/', '/k/', '/lgbt/', '/lit/', '/m/', '/mlp/', '/mu/', '/n/', '/news/', '/o/', '/out/', '/p/', '/po/', '/pol/', '/q/', '/qa/', '/qst/', '/r/', '/r9k/', '/s/', '/s4s/', '/sci/', '/soc/', '/sp/', '/t/', '/tg/', '/toy/', '/trv/', '/tv/', '/u/', '/v/', '/vg/', '/vip/', '/vp/', '/vr/', '/w/', '/wg/','/wsg/', '/wsr/', '/x/', '/y/']	
    for i in boards:
        findInBoard(i)
    
def findInNameSubjectQuote(segment):
    if('YGYL' in segment or 'Y G Y L' in segment or 'Y GY L' in segment or
           'YG,YL' in segment or 'YG, YL' in segment or 'YG YL' in segment or
           'YOUGROOVEYOULOSE' in segment or 'YOU GROOVE YOU LOSE' in segment or
           'YOU GROOVEYOU LOSE' in segment or 'YOUGROOVE,YOULOSE' in segment or
           'YOUGROOVE, YOULOSE' in segment or 'YOUGROOVE YOULOSE' in segment):
        return True

def replaceBr(element):
    text = ''
    for elem in element.recursiveChildGenerator():
        if isinstance(elem, str):
            text += elem.strip()
        elif elem.name == 'br':
            text += '\n'
    return text

def returnComments(postID, new_webm_instance, non_bmp_map):
    global commentIDs
    comments = ''

    for i in new_webm_instance.find_all('div', attrs={'class': 'post reply'}):
        iPost = i.find('blockquote', class_='postMessage')
        iPostText = iPost.text.translate(non_bmp_map)
        if postID in iPostText:
            iID = i.find('a', attrs={'title': 'Reply to this post'})
            iIDText = iID.text


            repFindFile = i.find('div', class_='fileText')
            if repFindFile != None:
                repFile = repFindFile.find('a', attrs={'target': '_blank'})

                if(repFile.has_attr('title')):
                    repFileText = repFile['title'].translate(non_bmp_map) + '\n'
                else:
                    repFileText = repFile.text.translate(non_bmp_map) + '\n'

            else:
                repFileText = ''
            repName = i.find('span', class_='name')
            repNameText = repName.text.translate(non_bmp_map)
            repID = i.find('a', attrs={'title': 'Reply to this post'})
            repIDText = repID.text
            repPost = i.find('blockquote', class_='postMessage')
            if repPost != None:
                repPostText = '\n' + replaceBr(repPost).translate(non_bmp_map)
            else:
                repPostText = ''


            if repIDText not in commentIDs:
                reply = repFileText + repNameText + ' No.' + repIDText + repPostText + '\n\n'
                comments += reply

                commentIDs.append(repIDText)

                if iIDText != postID:
                    comments += returnComments(iIDText, new_webm_instance, non_bmp_map)
    return comments
        
if __name__ == "__main__":
    
    main();
