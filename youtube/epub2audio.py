
import string 
import argparse
from curses.ascii import isalpha
import sys
import os
import re
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

'''
0. copy epub2audio.py to ~/util; make it excutable
cp ~/project/python/youtube/epub2audio.py ~/util/; chmod u+x ~/util/epub2audio.py
1. Activate venv
source ~/venv/text2audio/bin/activate
2. Convert epub file to txt files (one for each chapter)
python ~/project/python/youtube/epub2audio.py /home/lxf470/Documents/Books/Outlive.epub
3. Go to PriorGrad-acoustic
cd ~/git/NeuralSpeech/PriorGrad-acoustic
4. TTS
CUDA_VISIBLE_DEVICES=0 PYTHONPATH=. python tasks/priorgrad_inference.py --config configs/tts/lj/priorgrad.yaml --exp_name priorgrad --reset --inference_text ~/Documents/Books/Outlive_text/c001.txt --fast --fast_iter 12 
5.  
cd checkpoints/priorgrad/inference_fast12_1000000/
6. Create a txt file contains all the wav file names
rm -f file_names.txt; for FILE in *.wav; do echo file $FILE >> file_names.txt; done
7. Concatenate all wav files into one 
ffmpeg -f concat -safe 0 -i file_names.txt -c copy ~/Documents/Books/Outlive_audio/chp01.wav; rm *
8. Convert wav to mp3
for f in *.wav; do ffmpeg -i "$f" -vn -ar 22050 -ac 2 -b:a 192k "${f%.*}.mp3"; done
for f in *.wav; do if [ ! -f "${f%.*}.mp3" ]; then ffmpeg -i "$f" -vn -ar 22050 -ac 2 -b:a 192k "${f%.*}.mp3"; fi; done
'''

# Arguments from the console are parsed
parser = argparse.ArgumentParser(description=("Convert epub to audio. Example: epub2audio"))
parser.add_argument('input', nargs=1, type=str,
                   help='Input epub file')
parser.add_argument('-s', '--seperate', nargs=1, type=bool, default=True,
                   help='Seperate output file for each chapter or not (default = True)')
parser.add_argument('output', nargs='?', type=str,
                   help='Output file name (default = input_chp1.mp3)')

args = parser.parse_args()
print(args)

# Input
if not os.path.exists(args.input[0]):
    sys.exit(f'{args.input[0]} does not exist!')

ifile = args.input[0]
dir = os.path.dirname(args.input[0])
base = os.path.basename(args.input[0])
name_list = os.path.splitext(base)
input_name = ''.join(name_list[:-1])

# Output
ofile_name = args.output if args.output else input_name + '.mp3'

# read the epub file
book = epub.read_epub(ifile)

class metadata:
    """ metadata contains all metadata from the EpubBook
    """

    def __init__(self, book):
        self.identifier = book.get_metadata('DC', 'identifier')
        self.title = book.get_metadata('DC', 'title')
        self.language = book.get_metadata('DC', 'language')
        self.creator = book.get_metadata('DC', 'creator')
        self.contributor = book.get_metadata('DC', 'contributor')
        self.publisher = book.get_metadata('DC', 'publisher')
        self.rights = book.get_metadata('DC', 'rights')
        self.coverage = book.get_metadata('DC', 'coverage')
        self.date = book.get_metadata('DC', 'date')
        self.description = book.get_metadata('DC', 'description')

# Main part
metadat = metadata(book)

print(f'Title: {metadat.title[0][0]}') #, metadat.description)

items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

chapters = []
 
regex = r'c0[0-1]\d'
# regex = 'c002'

for item in items:
    print(item.get_name())
    regexp = re.compile(regex)
    if regexp.search(item.get_name()):
        chapters.append(item)

for c in chapters:
    print(f'chapter = {c.get_name()}')

def tag_is_p_or_h(tag):
    return tag.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']

def chapter_to_str(chapter):
    soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
    # soup = BeautifulSoup(chapter.get_content(), 'html.parser')
    # print(soup)
    text = []
    for para in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if para.name == 'p':
            text.append(para.get_text())
        elif para.get_text().rstrip(' ')[-1] not in string.punctuation:
            text.append(para.get_text() + '. ')

    # text = [para.get_text() for para in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']) if ]
    # text = [para.get_text() for para in soup.find_all(tag_is_p_or_h)]
    # text = [para.get_text() for para in soup.find_all('p')]

    return '\n'.join(text)

texts = {}
text_dir = dir + '/' + input_name + '_text/'
os.makedirs(text_dir, exist_ok=True)

for c in chapters:
    texts[c.get_name()] = chapter_to_str(c)

    # Save texts to indivial .txt file
    regexp = re.compile(regex)
    
    chp_name = regexp.search(c.get_name())
    chp_name = chp_name.group(0)

    if chp_name:
        fname = text_dir + chp_name + '.txt'
        print(fname)
        with open(fname, "w", encoding='utf-8') as f:
            f.write(texts[c.get_name()])


# print(f'texts={texts}')
# print(texts[list(texts.keys())[0]])
# print(f'texts.keys() = {texts.keys()}')
# print(f"texts['xhtml/Atti_9780593236604_epub3_c001_r1.xhtml'][:200] = {texts['xhtml/Atti_9780593236604_epub3_c001_r1.xhtml'][:2000]}")

# for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
#     print(image)