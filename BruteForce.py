# -*- coding: utf-8 -*-
"""
Created on Mon Sep  11 6:29:57 2023

@author: Amani Njoroge
"""

from SHA_1 import get_digest, show_time_taken
import time as t
import sys

#uses recursion
def brute_force(digest, p_len, rep, word, char_s, alph_len, **kwargs):

    n = kwargs['n']
    start = kwargs['start']
    
    def _brute_force(digest, p_len, rep, word, char_s, alph_len):
        
        count = kwargs['count']
        
        #if length isnt same as password length
        if len(word) != p_len: 
            
            #ASSUMPTION (to speed up processing)
            #a character cannot repeat itself more than 'rep' times
            for c in char_s:
                num = word.count(c) #number of times character appears so far
                if num > rep:
                    return
    
            #add another 'a'
            word += 'a' 
    
        else:
            return
    
        for i in range(alph_len):
            if word[-1] == char_s[-1]:
                return
    
            #if there is already a space bar in the word
            #And if you're about to change a character to a space
            if ' ' in word and char_s[i] == ' ':
                continue #go to next loop and forget furhter code
    
            #ASSUMPTION (to speed up processing)
            #a character cannot repeat itself more than 'rep' times
            num_1 = word.count(char_s[i])
            if num_1 > rep:
                continue #go to next loop and forget furhter code
    
            #As long as last character is not last alphabet
            #if last character != last alphabet
            count += 1
            #change last word to next alphabet
            #equivalent to saying word[-1] = char_s[i+1]
            word = word[:-1] + char_s[i]
            
            #only focus on words that are as long as the password
            if len(word) == p_len:
                #no need for heavy printing
                if count % n == 0: print(word)
        
                #get digest of that word with SHA-1 hashing
                #test if digests match
                if digest == get_digest(word):
                    print("Password is: %s" % word)
                    end = t.time()
                    show_time_taken(end-start)
                    sys.exit()
                
            #recurse
            brute_force(digest, p_len, rep, word, 
                        char_s, alph_len, **kwargs)
            
        return
    
    _brute_force(digest, p_len, rep, word, char_s, alph_len)

def BF(d, p_len, rep, char_s, start_time):
    
    #Digest of the very word being investigated
    digest = d.upper() 
    
    count = 0
    n = 150 #Show every output n where 0,1,2,...n... n+1...

    word = ''
    alph_len = len(char_s) #Alphabet length
    
    #start-up the brute force
    brute_force(digest, p_len, rep, word, char_s, alph_len,
                n = n, start = start_time, count = count)
    
    #if system exit doest take place due to finding a word:
    print('No match Found') 