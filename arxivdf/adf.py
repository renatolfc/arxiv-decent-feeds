#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse

import os
import model
import database
import feedwriter
import arxivreader

DBTYPE = 'sqlite:///'
DBPATH = os.path.join(
    os.path.expanduser('~'), '.arxiv-decent-feeds', 'db.sqlite'
)
DB = DBTYPE + DBPATH


def urljoin(*args):
    return '/'.join(s for s in args if s.strip() != '')


def parseOptions():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-d', '--database',
                        help='Database connection string (default: %s)' % DB,
                        default=DB, dest='database')

    subparsers = parser.add_subparsers(help='command help',
                                       metavar='<COMMAND>',
                                       dest='command')

    add = subparsers.add_parser('add',
                                help='add a new feed')
    add.add_argument('url')
    add.add_argument('target_file')

    update = subparsers.add_parser('update',
                                   help='updates the feeds')

    list_feeds = subparsers.add_parser('list',
                                       help='list existing feeds')

    remove = subparsers.add_parser('remove',
                                   help='remove a feed')
    remove.add_argument('id')

    edit = subparsers.add_parser('edit',
                                 help='edit a feed')

    generate = subparsers.add_parser('generate',
                                     help='outputs a feed of all data')
    generate.add_argument('base_url',
                          help='base url for generating feeds')
    generate.add_argument('id', nargs='?', default='all',
                          help='id of the source to read from ("all" for all)')
    generate.add_argument('n_entries', nargs='?', default='20',
                          help='number of entries per source feed')

    return parser.parse_args()


def rebuild_url(baseurl, feed):
    if baseurl:
        return urljoin(
            baseurl,
            os.path.basename(feed.target_file)
        )
    return ''


def main():
    configdir = os.path.dirname(DBPATH)
    if not os.path.exists(os.path.dirname(DBPATH)):
        os.makedirs(configdir)

    options = parseOptions()
    Session = database.connect(options.database, model.Base)
    db_session = Session()

    if options.command == 'add':
        arxivreader.fetch_feed(db_session, options.url, options.target_file)
    elif options.command == 'list':
        for feed in db_session.query(model.Feed).all():
            print('[%2d] %s' % (feed.id, feed.url))
    elif options.command == 'remove':
        feeds = db_session.query(model.Feed) \
                .filter(model.Feed.id==options.id).all()
        for feed in feeds:
            db_session.delete(feed)
            db_session.merge(feed)
    elif options.command == 'edit':
        raise SystemExit('Not implemented')
    elif options.command == 'generate':
        limit = int(options.n_entries)
        if options.id != 'all':
            feed = db_session.query(model.Feed) \
                    .filter(model.Feed.id==int(options.id)).all()
            if feed:
                with open(feed[0].target_file, 'w') as fp:
                    feedwriter.build_feed(
                        feed[0],
                        rebuild_url(options.base_url, feed),
                        limit,
                        fp
                    )
        else:
            for feed in db_session.query(model.Feed).all():
                with open(feed.target_file, 'w') as fp:
                    feedwriter.build_feed(
                        db_session,
                        feed,
                        rebuild_url(options.base_url, feed),
                        limit,
                        fp
                    )
    elif options.command == 'update':
        for feed in db_session.query(model.Feed).all():
            arxivreader.fetch_feed(db_session, feed.url)
    else:
        raise SystemExit('Impossible situation occurred')

    db_session.close()

if __name__ == '__main__':
    main()
