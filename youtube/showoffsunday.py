import sys
from youtube_transcript_api import YouTubeTranscriptApi
import csv
import requests
from bs4 import BeautifulSoup

url  = 'https://www.youtube.com/playlist?list=PLY9mgCQatPBxnxAxON7auy4mDjNpfrYgM'
prefix = 'https://www.youtube.com/watch?v='
s2 = 'index='
result = []

class videoInfo:
    def __init__(self, index, title, link):
        self.index = index
        self.title = title
        self.link  = link

# Usage: python showoffsunday.py video_list_url
if len(sys.argv) == 1:
    print('Using default url:', url)
else:
    url = sys.argv[1]

page = requests.get(url)
#soup = BeautifulSoup(page.content, 'html.parser')
soup = BeautifulSoup(page.content, 'html5lib')
#soup = BeautifulSoup(page.content, 'lxml')
#print(soup.prettify())

filename = soup.find('h1', class_='pl-header-title').text.strip().replace(" ", "_")

rows = soup.find_all('tr', class_='pl-video yt-uix-tile')

for elem in rows:
    s1 = elem.a['href']
    index = int(s1[(s1.index(s2) + len(s2)):-5]) - 1

    item = videoInfo(index, elem['data-title'].replace("’", "'").replace(",", ""), elem['data-video-id'])
    result.append(item)

result = sorted(result, key=lambda x: x.index)
[print(e.index, e.title, e.link) for e in result]


with open(filename+'.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for elem in result:
        writer.writerow([elem.index, elem.title, elem.link])

with open(filename+'.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
