**Why I did this**

I got bored one day and went onto 4chan because I wanted to see what was on that site.
I found out about recurring thread topics and I found one in particular that I liked a lot.
It was called 'YGYL' or 'You Groove, You Lose'.
It was a thread topic pertaining to webm files that had catchy groovy music in 30sec - 3min chunks.
I liked this a lot so I went about listening to all the music I could find on this thread.
I came back to the site a couple weeks later and couldn't find the thread anymore.
Apparently, 4chan deletes threads after a while. I felt defeated. I really liked this thread.
One day, I found out that there are sites that exist whose sole purpose is to catalog all the data from 4chan.
Once I found this archive site, I went about downloading all threads relevant to 'YGYL' manually.
That's when I realized that I'm a programmer.
I decided that this would be a good time to learn how to webscrape.
I picked up BeautifulSoup so that I could scrape the HTML off the pages.

**What this program does**

This program is a web scraper designed for a 4chan archive website.
It scrapes the HTML to find relevant threads pertaining to specific key terms.
Once it finds a relevant thread, it catalogs the comments and its hierarchy.
Alongside the comments, the program downloads all webm files related to the subject.
Then all files including comments and webms are organized neatly depending on the message board and thread.
This program combs through every message board on the archive site.
It does so by redirecting page by page until it has downloaded all the webm files and comments.
It also keeps check of the latest page that was left off.
There is also a record of links that is kept so that links aren't redownloaded multiple times.
All downloads are organized in a folder.

**UPDATE**

Apparently the person who owns the archive site has caught onto my scraping.
They have since restructured their website so that the data pertaining to the links of the files are now hidden in JS.
Now I do know a workaround for this. All I'd need to do is use Selenium to scrape the JS and extract the data.
However, I think I'm doing this person some stress so I won't do that.
I've scrapped hundreds of GB using this code so I think I'm happy.