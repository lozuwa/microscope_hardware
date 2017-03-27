import numpy as np
import os, sys, time

def get_max(list):
 max = 0
 index = 0
 for i in range(len(list)):
  if list[i][0] > max:
   max = list[i][0]
   index = i
 return (max, index)

def get_min(list = []):
 min = 1e5
 for i in range(len(list)):
  if list[i][0] < min:
   min = list[i][0]
   index = i
 return (min, index)

def find_val(list = [], val = 0):
 found = np.nan
 for each in list:
  if each == val:
   found = each
 return found
