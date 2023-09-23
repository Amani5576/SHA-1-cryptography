# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 04:23:34 2023

@author: Amani
"""
import string as STR

import time as t
from BruteForce import BF
from Random import R

methods = ['BF','R']
# methods = ['R', 'BF']

char_s = STR.ascii_letters
len_char_s = len(char_s)

# from random import random as rand
# word = [char_s[round(len_char_s*rand())-1] for i in range(1,6)]
# print(word)
# for i in range(len(word)):
#     if i != 0:
#         word[i] = word[i-1] + word[i]

word = ['f', 'fd', 'fdO', 'fdOE', 'fdOEG', 'fdOEGh', 'fdOEGha']
digests = ['4a0a19218e082a343a1b17e5333409af9d98f0f5', 
           '9f41a95cba557b2894771eed96e07a4ded82537f', 
           'cbea1424ea4e5f58d3cfa9bbaf1e6e1e8e235d72', 
           '7997de859fe7c4604051718d45dd72bef874416f', 
           'fd73930d1e12be7fe0330e1627cd13bcaba54e27',
           '5eb5ddce056265b2dcac38bb009dcba6d6ed52b1',
           '9a399d51000ba08d00a6f4c7f401a9fda86163bc']

def for_graphing(digest, method, rep, p_len, char_s):

        start = t.time() #start timer
        
        if method == 'BF':
            
            BF(digest, p_len, rep, char_s, start)
        
        elif method == 'R':
            
            R(digest, p_len, rep, char_s, start)
            #end of time and time taken is handled within Random.py file.
            
rep = 1

for ind, digest in enumerate(digests):
    for method in methods:
        print('type: ' + method)
        print('digest = ' + digest)
        p_len = len(word[ind])
        print('password length = ' + str(p_len))
        for_graphing(digest, method , rep, p_len, char_s)
        print()
        break