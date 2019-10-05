import sys
from youtube_transcript_api import YouTubeTranscriptApi

# video_id = 'md6E-wgq4Js&t=180s'
transcript = ''
language = []

try:
    video_id = sys.argv[1]
except:
    print('Wrong usage!!!')
    print('Correct usage: python gettranscript.py url ch')
    sys.exit(1)

if len(sys.argv) > 2:
    language.append(sys.argv[2])

if video_id[:32] == 'https://www.youtube.com/watch?v=':
    video_id = video_id[32:]
else:
    print(video_id, ' is incorrect. Exit now!')
    sys.exit(1)

print(list(language))
text = YouTubeTranscriptApi.get_transcript(video_id, languages=list(language))

for line in text:
    transcript += line['text'] + ' '

print(transcript)
