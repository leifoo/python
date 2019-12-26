import sys
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup

# video_id = 'md6E-wgq4Js&t=180s'
transcript = ''
language = ['en']
url  = 'https://www.youtube.com/user/scottykilmer/videos?view=0&sort=da&flow=grid'
url2 = 'https://www.youtube.com/user/scottykilmer/videos?view=0&sort=dd&flow=grid'

if len(sys.argv) == 1:
    print('Using default url:', url)
else:
    url = sys.argv[1]

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
#soup = BeautifulSoup(page.content, 'html5lib')
#soup = BeautifulSoup(page.content, 'lxml')

#print(soup.prettify())

header = soup.find_all('h3', class_='yt-lockup-title')
#header = soup.find_all('h3', class_=lambda value: value and value.startswith("watch"))[0]
for item in header:
    print(item.a['href'])

#for link in soup.find_all('a'):
#    print(link.get('href'))
#print(soup.find('strong', class_='watch-time-text').text)

