import sys
import urllib2
import urllib
 
from BeautifulSoup import BeautifulSoup # available at: http://www.crummy.com/software/BeautifulSoup/
 
def translate(sl, tl, text):
    """ Translates a given text from source language (sl) to
        target language (tl) """
 
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)')]
 
    translated_page = opener.open(
        "http://translate.google.com/translate_t?" + 
        urllib.urlencode({'sl': sl, 'tl': tl}),
        data=urllib.urlencode({'hl': 'en',
                               'ie': 'UTF8',
                               'text': text.encode('utf-8'),
                               'sl': sl, 'tl': tl})
    )
 
    translated_soup = BeautifulSoup(translated_page)
 
    return translated_soup('div', id='result_box')[0].string
 
if __name__=='__main__':
    print(translate('en', 'fr', u'hello'))