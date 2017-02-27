#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pytz
import model

from feedgen.feed import FeedGenerator


def build_feed(session, feed, final_url='', limit=None, stream=sys.stdout):
    items = session.query(model.FeedItem) \
            .filter(model.FeedItem.feed_id==feed.id) \
            .order_by(model.FeedItem.pubdate.desc()) \
            .limit(min(limit, len(feed.items))).all()

    fg = FeedGenerator()
    fg.title(feed.name)
    fg.link(href=feed.url, rel='alternate')
    fg.image(feed.imgurl, feed.name, final_url)
    fg.description(feed.description)
    fg.link(href=final_url, rel='self')
    fg.language('en')
    fg.ttl(60)
    fg.generator('arxiv-decent-feeds')

    if not items:
        stream.write(fg.rss_str(pretty=True))
        return

    for item in items:
        if not item.pubdate.tzinfo:
            # Add UTC to a naive datetime
            session.expunge(item)
            item.pubdate = pytz.utc.localize(item.pubdate)
        fe = fg.add_entry()
        fe.title(item.title)
        fe.link(href=item.link)
        fe.pubdate(item.pubdate)
        fe.description(item.summary)
        fe.guid(item.guid)

    stream.write(fg.rss_str(pretty=True))
