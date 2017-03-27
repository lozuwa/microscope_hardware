from pymongo import *
import numpy as np
import gridfs

try:
 client = MongoClient()
 db = client.focus
 fs = gridfs.GridFS(db)
except:
 print('Failed to initialize db, maybe mongod is not executing?')

def insert_value(slide):
 """ Slide: int value  """
 db.focus.insert_one({'slide':slide})

def insert_image(path):
 """ path to image """
 fs.put(open(str(path)),filename='images')

def update(slide, samples, refocus):
 """ Slide: int value, samples: 1d-vector or list, refocus: 1d-vector or list """
 db.focus.update({'field':slide}, {'$push':{'samples':samples, 'refocus':refocus}})
