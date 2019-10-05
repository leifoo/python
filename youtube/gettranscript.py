import sys
from youtube_transcript_api import YouTubeTranscriptApi

try:
    video_id = sys.argv[1]
except:
    print('Wrong usage!!!')
    print('Correct usage: python gettranscript.py url')
    sys.exit(1)

if video_id[:32] == 'https://www.youtube.com/watch?v=':
    video_id = video_id[32:]
else:
    print(video_id, ' is incorrect. Exit now!')
    sys.exit(1)

# video_id = 'md6E-wgq4Js&t=180s'
transcript = ''

text = YouTubeTranscriptApi.get_transcript(video_id)

for line in text:
    transcript += line['text'] + ' '

print(transcript)
