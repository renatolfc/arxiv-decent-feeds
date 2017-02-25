#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def connect(dbpath, base, verbose=False, autocommit=True, autoflush=True):
    engine = create_engine(dbpath, echo=verbose)
    base.metadata.create_all(engine, checkfirst=True)
    session = scoped_session(sessionmaker(autocommit=autocommit,
                                          autoflush=autoflush,
                                          bind=engine))
    return session
