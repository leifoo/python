import sys
from youtube_transcript_api import YouTubeTranscriptApi
# from googletrans import Translator
from translate import Translator

# video_id = 'md6E-wgq4Js&t=180s'
transcript = ''
language = []

try:
    video_id = sys.argv[1]
except:
    print('Wrong usage!!!')
    print('Correct usage: python gettranscript.py url zh-CN')
    sys.exit(1)

if len(sys.argv) > 2:
    language.append(sys.argv[2])

if video_id[:32] == 'https://www.youtube.com/watch?v=':
    video_id = video_id[32:]
else:
    print(video_id, ' is incorrect. Exit now!')
    sys.exit(1)

words = YouTubeTranscriptApi.get_transcript(video_id, languages=list(language))

for line in words:
    transcript += line['text'] + ' '

transcript2 = [x['text'] for x in words]
print(transcript2)

# Translate
# translator = Translator(service_urls=[
#       'translate.google.com',
#       'translate.google.co.kr',
#       'translate.google.cn'
#     ])

# translator = Translator()
to_lang = 'zh'
secret = '<your secret from Microsoft>'
translator = Translator(to_lang=to_lang)

print(translator.translate('test now'))
print(transcript2[:4])
translations = translator.translate(transcript[:500])
print(translations)