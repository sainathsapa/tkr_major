#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, re, string
#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from io import StringIO, BytesIO
import sys, re, string, logging
from collections import defaultdict
from datetime import datetime

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter

from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem import SnowballStemmer
import nltk.data

from network import download
from ssk import SSK

def timestr():
    return datetime.now().strftime('%H:%M:%S')

def decodepdf(fp, debug = False):
    with StringIO() as outfp:
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, outfp)
        logging.disable(logging.WARNING)
        if debug: print("processing pdf begin ({0})".format(timestr()))
        process_pdf(rsrcmgr, device, fp)
        if debug: print("processing pdf ended ({0})".format(timestr()))
        logging.disable(logging.NOTSET)
        return outfp.getvalue()

def decodetxt(fp):
    return fp.read()

def readfile(file, debug = False):
    try:
        if file.endswith('.txt'):
            with open(file, 'r') as fp:
                return fp.read()
        elif file.endswith('.pdf'):
            with open(file, 'rb') as fp:
                return decodepdf(fp, debug=debug)
    except KeyboardInterrupt:
        raise
    except:
        pass

def downloadfile(url, debug = False):
    data = download(url)
    try:
        if url.endswith('.txt'):
            return data.decode('utf-8')
        elif url.endswith('.pdf'):
            return decodepdf(BytesIO(data), debug=debug)
    except KeyboardInterrupt:
        raise
    except:
        pass

words_cache = {}

def getwords(text, langs=["english", "russian"], debug = False):
    key = (text, tuple(langs))
    if (key in words_cache):
        if debug: print("found words in cache")
        return words_cache[key]
    punct = re.compile('[%s0-9\–]' % re.escape(string.punctuation))
    
    if debug: print("tokenize begin ({0})".format(timestr()))
    words = TreebankWordTokenizer().tokenize(str(text));
    if debug: print("tokenize ended ({0})".format(timestr()))

    if debug: print("del short words begin ({0})".format(timestr()))
    words[:] = [word for word in words if len(word)>2]
    if debug: print("del short words ended ({0})".format(timestr()))

    if debug: print("punctuation begin ({0})".format(timestr()))
    words[:] = [word for word in words if punct.sub("", word) == word]
    if debug: print("punctuation ended ({0})".format(timestr()))

    if debug: print("stopwords begin ({0})".format(timestr()))
    words[:] = [word.lower() for word in words]
    stops = [stopwords.words(lang) for lang in langs]
    for stop in stops:
        words[:] = [word for word in words if word not in stop]
    if debug: print("stopwords ended ({0})".format(timestr()))

    if debug: print("stemming begin ({0})".format(timestr()))
    stemmers = [SnowballStemmer(lang) for lang in langs]
    for stemmer in stemmers:
        words[:] = [stemmer.stem(word) for word in words]
    if debug: print("stemming ended ({0})".format(timestr()))

    words_cache[key] = words
    return words

def getkeywords(text, langs=["english", "russian"], num = 10, debug = False):
    
    words = getwords(text, langs, debug=debug)
    
    wordsCount = defaultdict(int)
    for word in words:
        wordsCount[word] += 1
    
    if debug: print("sorting begin ({0})".format(timestr()))
    words = sorted(wordsCount.items(), key=lambda x: x[1], reverse=True)[:num]
    if debug: print("sorting ended ({0})".format(timestr()))
    
    words[:] = [word for (word, cnt) in words]
    
    return words

def evaluate(text1, text2, langs = ["english", "russian"], debug = False):
    text1 = getwords(text1, langs=langs, debug=debug)
    text2 = getwords(text2, langs=langs, debug=debug)

    block_sz = 100
    threshold = 0.1
    text1s = [text1[i:i+block_sz] for i in range(0, len(text1), block_sz)]
    text2s = [text2[i:i+block_sz] for i in range(0, len(text2), block_sz)]
    
    blocks = []
    for s in text1s:
        for t in text2s:
            res = SSK(s, t).solve(3)
            if res > threshold:
                blocks.append((res, s, t))
    
    return blocks
    
#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import random
from bs4 import BeautifulSoup
import urllib.parse
import re

browsers = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.6) Gecko/2009011912 Firefox/3.0.6',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6 (.NET CLR 3.5.30729)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) Gecko/2009020911 Ubuntu/8.10 (intrepid) Firefox/3.0.6',
            'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6',
            'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6 (.NET CLR 3.5.30729)',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.48 Safari/525.19',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)',
            'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.6) Gecko/2009020911 Ubuntu/8.10 (intrepid) Firefox/3.0.6',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.5) Gecko/2008121621 Ubuntu/8.04 (hardy) Firefox/3.0.5',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-us) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
            ]

def download(url):
    if (len(url) < 3):
        return None
    headers = {
        'User-Agent': browsers[random.randint(0, len(browsers) - 1)],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5'
    }
    try:
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request, timeout = 5)
        data = response.read()
        return data
    except:
        pass
        return None

class google:
    SEARCH_URL = "http://www.google.%(tld)s/search?hl=%(lang)s&newwindow=1&output=search&sclient=psy-ab&q=%(query)s"
    NEXT_PAGE = "http://www.google.%(tld)s/search?hl=%(lang)s&newwindow=1&q=%(query)s&start=%(start)d&sa=N"
    
    def __init__(self, query, lang="en", tld="com"):
        self.query = query
        self.lang = lang
        self.tld = tld
        self.num = 10
    
    def __fetch_page(self, page):
        pattern = google.SEARCH_URL
        if page > 0:
            pattern = google.NEXT_PAGE
        
        url = pattern % {
               'query': urllib.parse.quote_plus(self.query),
               'start': page * self.num,
               'tld' : self.tld,
                'lang' : self.lang
        }
        
        return download(url)
    
    def get_results(self, page):
        text = self.__fetch_page(page)
        soup = BeautifulSoup(text)
        
        res = []
        results = soup.findAll('li', {'class': 'g'})
        
        for result in results:
            try:
                a = result.find('a')
                name = a.text
                match = re.match(r'/url\?q=(http[^&]+)&', a['href'])
                url = urllib.parse.unquote(match.group(1))
                res.append({"name" : name, "url" : url})
            except:
                pass
                continue
        
        return res    

langs = ["english", "russian"]

def writelog(log, file1, keywords1, file2, keywords2, blocks, local = False):
    log.write("=" * 30 + "\n")
    log.write("Source file: " + file1 + "\n")
    log.write("Keywords 1: " + ", ".join(keywords1) + "\n")
    if local:
        log.write("Source file 2: " + file2 + "\n")
    else:
        log.write("Googled file: " + file2 + "\n")
    log.write("Keywords 2: " + ", ".join(keywords2) + "\n")
    for ssk, s, t in blocks:
        log.write("-" * 30 + "\n")
        log.write("Plagiated block with ssk: " + "%0.5f\n" % ssk)
        log.write("Source: " + " ".join(s) + "\n")
        log.write("Googled: " + " ".join(t) + "\n")

def main(argc, argv):
    if argc < 2:
        print("No input file specified")
        return
    
    if argv[1].startswith('http://') or argv[1].startswith('ftp://'):
        text = downloadfile(argv[1])
    else:
        text = readfile(argv[1])
    if text == None:
        print("File don't exist or do not have .pdf or .txt extension")
        return

    log = open("log.txt", 'w')

    if (argc == 3):
        if argv[2].startswith('http://') or argv[2].startswith('ftp://'):
            text2 = downloadfile(argv[2])
        else:
            text2 = readfile(argv[2])
            keywords = getkeywords(text, langs=langs)
            keywords2 = getkeywords(text2, langs=langs)
            print("Keywords for text 1: ", ", ".join(keywords))
            print("Keywords for text 2: ", ", ".join(keywords2))
            print("Searching for plagiated blocks ({0})".format(timestr()))
            blocks = evaluate(text, text2, langs=langs, debug=False)
            print("Search ended, found {0} plagiated blocks ({1})".format(len(blocks), timestr()))
            if len(blocks) > 0:
                writelog(log, argv[1], keywords, argv[2], keywords2, blocks, local=True)
                print("\nAll plagiated blocks were written to log.txt")
        log.close()
        return

    keywords = getkeywords(text, langs=langs)
    print("Keywords for source: " + ", ".join(keywords))
    query = "filetype:pdf " + " ".join(keywords)
    print("Googling: ", query)
    g = google(query)
    results = g.get_results(0)
    if len(results) == 0:
        print("Sorry, googling failed, maybe we are banned")
        return
    print("Google'd ", len(results), " documents:")
    for i, result in enumerate(results):
        print(str(i+1) + ": " + result['url'])

    for i, result in enumerate(results):
        try:
            print("\nProcessing file " + str(i+1) + ": " + result['url'])
            text2 = downloadfile(result['url'])
            if text2 == None:
                print("This file appears to be invalid .pdf file")
                continue
            keywords2 = getkeywords(text2, langs=langs)
            print("Keywords: ", ", ".join(keywords2))
            print("Searching for plagiated blocks ({0})".format(timestr()))
            blocks = evaluate(text, text2, langs=langs, debug=False)
            print("Search ended, found {0} plagiated blocks ({1})".format(len(blocks), timestr()))
        except KeyboardInterrupt:
            print("Interrupted by User")
            pass
            continue
        if len(blocks) > 0:
             writelog(log, argv[1], keywords, result['url'], keywords2, blocks)
    print("\nAll plagiated blocks were written to log.txt")
    log.close()

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)