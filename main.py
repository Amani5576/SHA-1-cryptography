# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 19:20:04 2023

@author: Amani
"""

from SHA_1 import show_time_taken, get_digest
from BruteForce import BF
from Random import R
import time as t
import string as STR

def rep_query():
    r = input('''
    ______________________________________
    
    How many times do you suspect a letter 
    can appear in the message? ''')
    return int(r)

def digest_query():
    d = input('''
    _____________________________________________
    
    Please insert (or copy paste) digest below:
    e.g. 950bfe587a64c98e435d811a6c43097ec6d2546d
        
    ''')
    return d

def get_pw_len():
    pl = input('''
    _______________________________________
    
    Please guess the length of the message: ''')
    return int(pl)

def get_method():
    
    m = input("""
    __________________________________________________
    
    choose methodology below for acquring the message:
    
    Brute Force words = type 1
    Generate Random Words = type 2
    
    then press enter.
    
    choice? """)
    
    if m not in ['1','2']:
        m = get_method()
    
    return int(m)
                
def get_char_s():
    
    def _get_char_s(): #Getting users preference in what type of data to produce
        
        choices = ["LC","UC","D","SP", "ALL", "P"]
        
        p_choice = input("""
                           
        Possible elements in message:
        
        Lowercase -> "LC"
        Uppercase -> "UC"
        Digits -> "D"
        A possible space -> "SP"
        Punctuations - > "P"
        All the above -> "ALL"

        If multiple choices, then separate each by a comma (,)
        
        
        """)
        print()
        
        #Convert choice inputs into list array of those choices (if there are more than one)
        if ',' in p_choice:
            p_choice = p_choice.split(",") #Automatically splits every string element based on the specified arguement splitter
            #Overwriting "x" with its new list-form rather than remaining as string.

        #If singular invalid choice made
        if type(p_choice) == str: 
            if p_choice.upper() not in choices: 
                print("%s was not one of the options" % p_choice)
                p_choice = _get_char_s()
                
        else: #If a list of choices were made with invalid inputs
            for i in p_choice:
                if i.upper() not in choices:
                    p_choice = _get_char_s()
                    
        return p_choice
    
    p_choice = _get_char_s()
    ls = [STR.ascii_lowercase, STR.ascii_uppercase, 
              STR.digits, STR.punctuation]
    char_s = ''
    #if there are a list of choices
    if type(p_choice) == list:
        for p_c in p_choice:
            p_c = p_c.upper() #convert to uppercase
            if p_c == "LC": char_s += ls[0]
            elif p_c == "UC": char_s += ls[1]
            elif p_c == "D":  char_s += ls[2]
            elif p_c == "P": char_s += ls[3]
            elif p_c == "SP":  char_s += ' '
            elif p_c == "ALL": #incase user adds ALL within a list
                char_s = ''.join(ls) + ' '
                break #dont repeat adding unique characters
    else: #if user only chose a singular choice
        p_choice = p_choice.upper() #convert to uppercase
        if p_choice == "LC": char_s += ls[0]
        elif p_choice == "UC": char_s += ls[1]
        elif p_choice == "D":  char_s += ls[2]
        elif p_choice == "P": char_s += ls[3]
        elif p_choice == "SP":  char_s += ' '
        elif p_choice == "ALL": char_s = ''.join(ls) + ' '
    
    return char_s
    
    
def main():
    
    typ = int(input('''
    message to digest -> type 1
    digest to message -> type 2
    
    '''))
    
    if typ == 1:
        digest = get_digest(input('''
    insert message below:
    
    '''))
        
        print()
        print("digest = %s" % digest)
        print()
    elif typ == 2:
        #Unreversable cryptography of message
        digest = digest_query()
    
        #choosing between methods provided
        method = get_method()
        
        #number of times a letter can repeat
        rep = rep_query() 
        
        #length of password
        p_len = get_pw_len()
        
        #get list of possible charcaters that can be in message
        char_s = get_char_s()
        
        #start timer
        start = t.time() 
        
        if method == 1:
            
            print('please wait as messages of length %d are being tested via brute force method''' % p_len)
            print()
            
            BF(digest, p_len, rep, char_s, start)
        
        elif method == 2:
            
            print('''
        please wait as random messages of length %d are being tested''' % p_len)
            
            R(digest, p_len, rep, char_s, start)
            #end of time and time taken is handled within Random.py file.
        
main()
        