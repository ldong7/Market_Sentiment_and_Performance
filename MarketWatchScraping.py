# Litong "Leighton" Dong
# Market Watch Scraping

from bs4 import BeautifulSoup
import urllib2
import re
import os
import time
import random
import csv
import sys
from datetime import datetime


def extractArticle(url):                                # function that extract the text given the url
    request = urllib2.Request(url)                      # request url
    try:
        page = urllib2.urlopen(request)                 # load page
    except urllib2.URLError, e:                         # error handling
        if hasattr(e, 'reason'):
            print 'Failed to reach url_extractArticle'
            print 'Reason: ', e.reason
            return ['','','']

        elif hasattr(e, 'code'):                         # error handling
            if e.code == 404:
                print 'Error: ', e.code
                return ['','','']

    content = page.read()                                # extract content
    soup = BeautifulSoup(content,'lxml')                 # parse content into beautiful soup object
    results = soup.find_all(id='article-body')           # search for the article content
    if len(results) != 0:                                # check article content if there is any
        title = soup.title.text                          # extract title
        title = title.strip()                            # strip leading and trailing whitespace
        title = re.sub('\W', '_', title)                 # replace any non words(space and symbols) with '_'

        results2 = soup.find_all(id='date-created')      # extract date
        for result2 in results2:
            date = result2['content']
            date = re.sub('\s', '_', date)               # replace white space with '_'
            break                                        # stop after first found

        info_list = []
        for result in results:
            for info in result.contents:
                if info.name == 'p':
                    word = info.text                      # extract article content
                    word = re.sub('\r', '', word)         # clean text
                    word = re.sub('\n', '', word)
                    word = re.sub('\s\s+', '', word)
                    word = re.sub('\t', '', word)
                    word.strip()                          # strip leading and trailing whitespace
                    info_list.append(word)                # append to list

        article = ' '.join(info_list)                     # join articles together
        return [article, title, date]
    else:
        return ['','','']                                 # return empty text if none


def extractUrl(main_url):                                 # function to extract article url from main page
    request = urllib2.Request(main_url)
    try:
        page = urllib2.urlopen(request)                   # request url
    except urllib2.URLError, e:                           # error handling
        if hasattr(e, 'reason'):
            print 'Failed to reach url_extractURL'
            print 'Reason: ', e.reason
            sys.exit()
        elif hasattr(e, 'code'):
            if e.code == 404:
                print 'Error: ', e.code
                sys.exit()

    content = page.read()
    soup = BeautifulSoup(content,'lxml')                   # beautiful soup object with url content
    urls = []                                              # url list
    results = soup.find_all(href=re.compile('/story'))     # find url for articles
    for result in results:
        if result['href'].startswith('http://www.marketwatch.com'):     # check url content
            url = result['href']                                        # extract url
            urls.append(url)                                            # append url to list
        elif result['href'].startswith('http://stream'):                # exclude live streams
            continue
        else:
            url = 'http://www.marketwatch.com' + result['href']         # extract and modify url
            urls.append(url)                                            # append url to list

    results2 = soup.find_all(href=re.compile('/column'))             # same function as above for second type of article
    for result2 in results2:
        if result2['href'].startswith('http://www.marketwatch.com'):
            url = result2['href']
            urls.append(url)
        else:
            url = 'http://www.marketwatch.com' + result2['href']
            urls.append(url)

    return urls


def saveTxt(article, name, date):                                           # function that export article texts
    text_file = open("./marketwatch_story/%s_%s.txt" % (name, date), "w")   # open text file with specific name
    text_file.write(article.encode('utf8'))
    text_file.close()


main_url = "http://www.marketwatch.com"                                     # main page of market watch
urls = extractUrl(main_url)                                                 # obtain urls from main page

for url in urls:
    print url
    [article, title, date] = extractArticle(url)                            # extract text from url
    if len(article) != 0:                                                   # if text exist
        saveTxt(article, title, date)                                       # write to txt file
        wait_time = round(max(0, 1 + random.gauss(0,0.5)), 2)
                                                    # Generate a random waiting time to avoid being detected and banned
        time.sleep(wait_time)

# debugging codes:
# url = 'http://www.marketwatch.com/column/Tech%20Stocks'
# [article, title, date] = extractArticle(url)
# if len(article) != 0:
#     print article
#     print title
#     print date
#     saveTxt(article, title, date)