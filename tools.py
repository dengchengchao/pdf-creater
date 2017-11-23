#!/usr/bin/env python
import string
'''

Some common  algorithms
'''
def is_punctuation(char,pun_list=":，、。？《》：！（）【】“”‘’；"+string.punctuation):
    return char in pun_list

def get_average(list):
    list_len=len(list)
    if list_len!=0:
      return int(sum(list)/list_len)
    return  list_len