#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pymongo
import pprint
import json
from statistics import mean
from datetime import datetime


mongoCLient = pymongo.MongoClient('mongodb://localhost:27017/')
db = mongoCLient['election_reactions']

reactions = {}
for coll_name in db.list_collection_names():
  print('Collection:', coll_name)
  coll = db[coll_name]
  docs = coll.find()
  sample = 10
  count = 0
  reactions[coll_name] = {
    'positive': [],
    'neutral': [],
    'negative': [],
  }
  for doc in docs:
    count += 1
    print(doc['text'])
    reactions[coll_name]['positive'].append(float(input('positive: '))/100)
    reactions[coll_name]['neutral'] .append(float(input('neutral: '))/100)
    reactions[coll_name]['negative'].append(float(input('negative: '))/100)
    if count >= sample:
      break
  reactions[coll_name]['positive'] = mean(reactions[coll_name]['positive'])
  reactions[coll_name]['neutral'] = mean(reactions[coll_name]['neutral'])
  reactions[coll_name]['negative'] = mean(reactions[coll_name]['negative'])
  pprint.pprint(reactions)
print('\n\n\n')
pprint.pprint(reactions)