#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pymongo
import pprint
import json
from datetime import datetime


mongoCLient = pymongo.MongoClient('mongodb://localhost:27017/')
db = mongoCLient['election_reactions']

for coll_name in db.list_collection_names():
  coll = db[coll_name]
  docs = coll.find()
  for doc in docs:
    doc['datetime'] = datetime.strptime(doc['date'], '%a %b %d %H:%M:%S +0000 %Y')
    coll.save(doc)