#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import model

import requests
import feedparser
import dateutil.parser

from lxml import html
from time import mktime
from datetime import datetime

DATETIME_PAT = re.compile('(\w+, \d+ \w+ \d+ \d+:\d+:\d+ \w+)')


def get_pubdates(url):
    response = requests.get(url)
    if not response.ok:
        return None
    root = html.fromstring(response.text.encode('utf-8'))
    submissions = root.find_class('submission-history')
    if not submissions:
        # oops?
        return None
    datestr = DATETIME_PAT.findall(submissions[0].text_content())
    dates = sorted(dateutil.parser.parse(d) for d in datestr)
    return dates

def fetch_feed(session, url, target_file=None):
    new_entry = False
    feed = feedparser.parse(url)
    dbfeed = session.query(model.Feed).filter(model.Feed.url==url).all()
    if not dbfeed:
        # This is a new feed we have to build
        if not target_file:
            raise ValueError('missing a required argument (target_file)')
        dbfeed = model.Feed(url, feed['feed']['title'],
                            feed['feed']['subtitle'],
                            feed['feed']['image']['title'],
                            feed['feed']['image']['url'],
                            feed['feed']['image']['link'],
                            target_file)
        session.add(dbfeed)
    else:
        dbfeed = dbfeed[0]
        dbfeed = session.merge(dbfeed)
    if 'updated_parsed' in feed['feed'] and feed['feed']['updated_parsed']:
        dbfeed.updated = datetime.fromtimestamp(
            mktime(feed['feed']['updated_parsed'])
        )
    else:
        dbfeed.updated = datetime.now()
    for item in feed['entries']:
        dbitem = session.query(model.FeedItem).filter(
            model.FeedItem.link==item['link']
        ).all()
        if not dbitem:
            pubdate = get_pubdates(item['link'])
            if not pubdate:
                continue
            dbitem = model.FeedItem(
                dbfeed, item['link'], item['title'], item['summary'],
                pubdate[0], item['guid'], item['guidislink']
            )
            session.add(dbitem)



#def parse_feed(feed):
#    entries = feedparser.parse(feed.url)
#    feed.updated = entries.get('updated_parsed', datetime.now())
#    items = [FeedItem(
