#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pymongo
import pprint
import json
from datetime import datetime


mongoCLient = pymongo.MongoClient('mongodb://localhost:27017/')
db = mongoCLient['election_reactions']

coll_names = db.list_collection_names()
coll_names = sorted(coll_names)
for coll_name in coll_names:
  coll = db[coll_name]
  print('{}: {}'.format(coll_name, coll.count()))