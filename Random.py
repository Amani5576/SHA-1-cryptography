# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 02:23:33 2023

@author: Amani
"""
from SHA_1 import get_digest_R, show_time_taken
from random import random as rand
# import string as STR
import time as t

def make_word(char_s, rep, len_char_s, p_len):
    
    #MAKE A WORD
    word = ''
    l = 0
    while l < p_len:
        
        #get random chracter or space from list 'char_s'
        c = char_s[round(len_char_s*rand())-1]
        
        #if there is already a space bar in the word
        #And if you're about to change a character to a space
        if ' ' in word and c == ' ':
            continue #go to next loop and forget further code
            
        #ASSUMPTION (to speed up processing)
        #a character cannot repeat itself more than 'rep' times
        num_1 = word.count(c)
        if num_1 > rep:
            continue #go to next loop and forget furhter code
        
        word += c #add new character to word
        l += 1 #increment length by one as word continues to be constructed
        
    return word

def R(digest, p_len, rep, char_s, start_time):
    start = start_time
    #digest = Digest of the very word being investigated
    #e.g. '950bfe587a64c98e435d811a6c43097ec6d2546d'
    
    # p_len#10 #password length 
    # char_s #all different character variables
    len_char_s = len(char_s)
    # rep #2
    
    found = False 
    while found == False:
        
        word = make_word(char_s, rep, len_char_s, p_len)
        # print(word)
        if get_digest_R(word) == digest:
            found = True
            print("Password is: %s" % word)
            end = t.time() #end timer
            show_time_taken(end-start)