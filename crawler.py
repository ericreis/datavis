#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from twython import Twython
import pymongo
import pprint
import json


# Setup twitter api
TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
TWITTER_API_KEY_SECRET = os.environ['TWITTER_API_KEY_SECRET']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

t = Twython(app_key=TWITTER_API_KEY, 
            app_secret=TWITTER_API_KEY_SECRET, 
            oauth_token=TWITTER_ACCESS_TOKEN, 
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

coords = [
  { 'state': 'AC', 'lat': '-9.0238', 'lon': '-70.8120', 'rad': '100' },
  { 'state': 'AL', 'lat': '-9.5713', 'lon': '-36.7820', 'rad': '100' },
  { 'state': 'AM', 'lat': '-3.4168', 'lon': '-65.8561', 'rad': '100' },
  { 'state': 'AP', 'lat': '0.9020', 'lon': '-52.0030', 'rad': '100' },
  { 'state': 'BA', 'lat': '-12.5797', 'lon': '-41.7007', 'rad': '100' },
  { 'state': 'CE', 'lat': '-5.4984', 'lon': '-39.3206', 'rad': '100' },
  { 'state': 'DF', 'lat': '-15.7998', 'lon': '-47.8645', 'rad': '50' },
  { 'state': 'ES', 'lat': '-19.1834', 'lon': '-40.3089', 'rad': '100' },
  { 'state': 'GO', 'lat': '-15.8270', 'lon': '-49.8362', 'rad': '100' },
  { 'state': 'MA', 'lat': '-4.9609', 'lon': '-45.2744', 'rad': '100' },
  { 'state': 'MG', 'lat': '-18.5122', 'lon': '-44.5550', 'rad': '100' },
  { 'state': 'MS', 'lat': '-20.7722', 'lon': '-54.7852', 'rad': '100' },
  { 'state': 'MT', 'lat': '-12.6819', 'lon': '-56.9211', 'rad': '100' },
  { 'state': 'PA', 'lat': '-1.9981', 'lon': '-54.9306', 'rad': '100' },
  { 'state': 'PB', 'lat': '-7.2400', 'lon': '-36.7820', 'rad': '100' },
  { 'state': 'PE', 'lat': '-8.8137', 'lon': '-36.9541', 'rad': '100' },
  { 'state': 'PI', 'lat': '-7.7183', 'lon': '-42.7289', 'rad': '100' },
  { 'state': 'PR', 'lat': '-25.2521', 'lon': '-52.0215', 'rad': '100' },
  { 'state': 'RJ', 'lat': '-22.9099', 'lon': '-43.2095', 'rad': '100' },
  { 'state': 'RN', 'lat': '-5.4026', 'lon': '-36.9541', 'rad': '100' },
  { 'state': 'RO', 'lat': '-11.5057', 'lon': '-63.5806', 'rad': '100' },
  { 'state': 'RR', 'lat': '2.7376', 'lon': '-62.0751', 'rad': '100' },
  { 'state': 'RS', 'lat': '-30.0346', 'lon': '-51.2177', 'rad': '100' },
  { 'state': 'SC', 'lat': '-27.2423', 'lon': '-50.2189', 'rad': '100' },
  { 'state': 'SE', 'lat': '-10.5741', 'lon': '-37.3857', 'rad': '100' },
  { 'state': 'SP', 'lat': '-24.5432', 'lon': '-46.6292', 'rad': '100' },
  { 'state': 'TO', 'lat': '-10.1753', 'lon': '-48.2982', 'rad': '100' }
]


mongoCLient = pymongo.MongoClient('mongodb://localhost:27017/')
db = mongoCLient['election_reactions']

query = 'bolsonaro -filter:retweets'

for coord in coords:
  coll = db[coord['state']]
  coll.create_index(
      [("tweet_id", 1)],
      unique=True
  )

  geocode = '{},{},{}km'.format(coord['lat'], coord['lon'], coord['rad'])

  cursor = coll.find().sort('tweet_id', -1)
  last_tweet_doc = next(cursor, None)
  since_id = -1
  if last_tweet_doc is not None:
    since_id = last_tweet_doc['tweet_id']
    tweets = t.search(q=query, tweet_mode='extended', geocode=geocode, result_type='recent', count=100, since_id=since_id)['statuses']
  else:
    tweets = t.search(q=query, tweet_mode='extended', geocode=geocode, result_type='recent', count=100)['statuses']

  tweet_docs = []
  for tweet in tweets:
    tweet_doc = {
      'tweet_id': tweet['id_str'],
      'text': tweet['full_text'],
      'date': tweet['created_at'],
      'coords': tweet['coordinates'],
      'geo': tweet['geo'],
      'place': tweet['place'],
      'lang': tweet['lang'],
      'state': coord['state']
    }
    tweet_docs.append(tweet_doc)

  if len(tweet_docs) > 0:
    coll.insert_many(tweet_docs)
  # pprint.pprint('Found {0} new tweets since {1}'.format(len(tweet_docs), since_id))
  print('Found {} new tweets for {}'.format(len(tweet_docs), coord['state']))

# # Creating query from command-line args
# query = ""
# for htag in args.htags:
#     if query == "":
#         query += "#" + htag
#     else:
#         query += " OR #" + htag

# if args.nort:
#     query += "-filter:retweets"

# print 'query:', query

# with open('since_id.dat', 'r') as f_read:
#     since_id = f_read.readline()

# # Searching
# if (since_id == ''):
#     search = t.search(q=query, count=args.count)
# else:
#     search = t.search(q=query, count=args.count, since_id=since_id)



# tweets = search['statuses']

# tweet_docs = []

# # Inserting mongo
# for tweet in tweets:

#     tweet_doc = {
#         'tweet_id': tweet['id_str'],
#         'text': tweet['text'].encode('utf-8'),
#         'date': tweet['created_at'],
#         'rt': tweet['retweeted']
#     }

#     tweet_docs.append(tweet_doc)

#     if tweet_doc['tweet_id'] > since_id:
#         since_id = tweet_doc['tweet_id']

# collection.insert_many(tweet_docs)
# print 'Found {0} new tweets'.format(len(tweet_docs))

# with open('since_id.dat', 'w') as f_write:
#     f_write.write(since_id)