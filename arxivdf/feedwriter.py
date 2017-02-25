#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


FEED_HEADER = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        {1}
        <link>{0.url}</link>
        <title>{0.name}</title>
        <image>
            <title>{0.name}</title>
            <url>{0.imgurl}</url>
            <link>{0.imglink}</link>
        </image>
        <description><![CDATA[{0.description}]]></description>'''

FEED_ITEM = '''
            <item>
                <title>{0.title}</title>
                <link>{0.link}</link>
                <pubDate>{0.pubdate_rfc}</pubDate>
                <description><![CDATA[{0.summary}]]></description>
                <guid isPermaLink="{0.permalink_str}">{0.guid}</guid>
            </item>'''

FEED_FOOTER = '''
</channel>
</rss>'''

ATOM_LINK = '<atom:link href="{0}" rel="self" type="application/rss+xml"/>'

def build_feed(feed, final_url='', limit=None, stream=sys.stdout):
    if final_url:
        final_url = ATOM_LINK.format(final_url)
    stream.write(FEED_HEADER.format(feed, final_url))
    if not limit:
        limit = len(feed.items)
    for i in range(min(limit, len(feed.items))):
        item = feed.items[i]
        stream.write(FEED_ITEM.format(item))
    stream.write(FEED_FOOTER)
