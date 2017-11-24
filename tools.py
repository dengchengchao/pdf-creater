#!/usr/bin/python
# -*-coding:utf-8-*-
# Author:Citron
import string
'''
Some common  algorithms
'''
def is_punctuation(char,pun_list=":，、。？《》：！（）【】“”‘’；"+string.punctuation):
    return char in pun_list

def is_digit(char,digit_list="1234567890"):
    return char in digit_list

def get_average(list):
    list_len=len(list)
    if list_len!=0:
      print(sum(list),list_len,sum(list)/list_len)
      return int(sum(list)/list_len)
    return  list_len

