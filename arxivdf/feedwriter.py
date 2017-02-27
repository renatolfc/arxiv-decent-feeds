#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import model
from email.Utils import formatdate


FEED_HEADER = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        {1}
        <link>{0.url}</link>
        <title>{0.name}</title>
        <lastBuildDate>{2}</lastBuildDate>
        <pubDate>{3}</pubDate>
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

def build_feed(session, feed, final_url='', limit=None, stream=sys.stdout):
    if final_url:
        final_url = ATOM_LINK.format(final_url)
    if not limit:
        limit = len(feed.items)
    items = session.query(model.FeedItem) \
            .filter(model.FeedItem.feed_id==feed.id) \
            .order_by(model.FeedItem.pubdate.desc()) \
            .limit(min(limit, len(feed.items))).all()
    # FIXME: only makes sense if the channel is not empty
    stream.write(
        FEED_HEADER.format(
            feed,
            final_url,
            items[0].pubdate_rfc,
            formatdate()
        )
    )
    for item in items:
        stream.write(FEED_ITEM.format(item))
    stream.write(FEED_FOOTER)
