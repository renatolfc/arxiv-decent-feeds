#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from datetime import datetime
from email.Utils import formatdate

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Feed(Base):
    __tablename__ = 'feeds'
    id = Column(Integer, primary_key=True)
    url = Column(String(1024), unique=True)
    name = Column(String(1024))
    description = Column(String(4096))
    imgtitle = Column(String(1024))
    imgurl = Column(String(1024))
    imglink = Column(String(1024))
    updated = Column(DateTime(timezone=True))
    items = relationship('FeedItem', back_populates='feed',
                         cascade="all, delete-orphan")
    target_file = Column(String(1024))

    def __init__(self, url, name, description, imgtitle, imgurl,
                 imglink, target_file):
        self.url = url
        self.name = name
        self.description = description
        self.imgtitle = imgtitle
        self.imgurl = imgurl
        self.imglink = imglink
        self.target_file = target_file

class FeedItem(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    feed_id = Column(Integer, ForeignKey('feeds.id'))
    feed = relationship(Feed, back_populates='items')
    link = Column(String(1024), unique=True)
    title = Column(String(1024))
    summary = Column(String(4096))
    pubdate = Column(DateTime(timezone=True))
    guid_is_permalink = Column(Boolean)
    guid = Column(String(1024))

    def __init__(self, feed, link, title, summary, pubdate, guid,
                 guid_is_permalink=False):
        self.feed = feed
        self.link = link
        self.title = title
        self.summary = summary
        self.pubdate = pubdate
        self.guid = guid
        self.guid_is_permalink = guid_is_permalink

    @property
    def pubdate_rfc(self):
        if self.pubdate:
            return formatdate(time.mktime(self.pubdate.timetuple()))
        return formatdate(time.mktime(datetime.now()))

    @property
    def permalink_str(self):
        return str(self.guid_is_permalink).lower()

#    updates = relationship('Update', back_populates='items')

#class Update(Base):
#    __tablename__ = 'updates'
#    id = Column(Integer, primary_key=True)
#    item_id = Column(Integer, ForeignKey('items.id'))
#    item = relationship('FeedItem', back_populates='updates')
#    link = Column(String(1024))
#    pubdate = Column(DateTime)
