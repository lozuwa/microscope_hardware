from pymongo import *
import numpy as np

try:
 client = MongoClient()
 db = client.focus
except:
 print('Failed to initialize db, maybe mongod is not executing?')

def insert_one(slide):
 """ Slide: int value  """
 db.client.insert_one({'slide':slide})

def update(slide, samples, refocus):
 """ Slide: int value, samples: 1d-vector or list, refocus: 1d-vector or list """
 db.client.update({'field':slide}, {'$push':{'samples':{samples}, 'refocus':{refocus} }})
