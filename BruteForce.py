# -*- coding: utf-8 -*-
"""
Created on Mon Sep  11 6:29:57 2023

@author: Amani Njoroge
"""

from SHA_1 import get_digest, show_time_taken
import time as t

#uses recursion
def brute_force(digest, p_len, rep, word, char_s, alph_len, **kwargs):

    # n = kwargs['n']
    
    def _brute_force(digest, p_len, rep, word, char_s, alph_len):
        
        count = kwargs['count']
        word_found = False
        
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
            if word_found == True:
                break
            
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
                # if count % n == 0: print(word)
        
                #get digest of that word with SHA-1 hashing
                #test if digests match
                if digest == get_digest(word):
                    print("Password is: %s" % word)
                    end = t.time()
                    show_time_taken(end-kwargs['start'])
                    return True
                    
                
            #recurse
            word_found = _brute_force(digest, p_len, rep, word, 
                        char_s, alph_len)
            
        return word_found
    
    return _brute_force(digest, p_len, rep, word, char_s, alph_len)

def BF(digest, p_len, rep, char_s, start_time):
    
    #digest = Digest of the very word being investigated
    
    count = 0
    
    #Show every '150i'th word where i is a +ve incrementing integer
    # n = 150 

    word = ''
    alph_len = len(char_s) #Alphabet length
    
    #start-up the brute force
    word_found = brute_force(digest, p_len, rep, word, char_s, alph_len, start = start_time
                , count = count)
    
    if word_found == False:
        print('No match Found') 