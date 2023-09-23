# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 19:20:04 2023

@author: Amani
"""

from SHA_1 import get_digest
from BruteForce import BF
from Random import R
import time as t
import string as STR

def rep_query():
    r = input('''
    _________________________________________
    
    How many times do you suspect a character 
    can appear in the message? ''')
    return int(r)

def digest_query():
    d = input('''
    _____________________________________________
    
    Insert digest: (e.g. 950bfe587a64c98e435d811a6c43097ec6d2546d)
        
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
    
    Choose Methodology:
    
    Brute Force words -> type 1
    Generate Random Words -> type 2
    
    then press enter.
    
    choice? """)
    
    if m not in ['1','2']:
        m = get_method()
    
    return int(m)
                
def get_char_s():
    
    choices = ["LC","UC","D","SP","P","ALL"]
    
    def _get_char_s(): #Getting users preference in what type of data to produce
        
        
        
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
        
        #Convert choice inputs into list array of those choices 
        #(if there are more than one)
        if ',' in p_choice:
            #Automatically splits every string element based 
            #on the specified arguement splitter
            p_choice = p_choice.split(",") 
        #If singular invalid choice made
        if type(p_choice) == str: 
            if p_choice.upper() not in choices: 
                print("%s was not one of the options" % p_choice)
                p_choice = _get_char_s()
                
        else: #If a list of choices were made with invalid inputs
            for i in p_choice:
                if i.upper() not in choices:
                    p_choice = _get_char_s()
                if i.upper() == "ALL": #if ALL is in the choices
                    print("Invalid input of 'ALL' with other choices")
                    p_choice == _get_char_s()
        return p_choice
    
    #tranlates users given characters into string of those characters
    def add_characters(p_choice, char_s):
        p_choice = p_choice.upper()
        ls = [STR.ascii_lowercase, STR.ascii_uppercase, 
                  STR.digits, ' ', STR.punctuation]
        for i in range(len(ls)):
            if p_choice == choices[i]: 
                char_s += ls[i]
                break
            elif p_choice == 'ALL':
                char_s = ''.join(ls)
                
        return char_s
        
    p_choice = _get_char_s()
    
    char_s = ''
    #if there are a list of choices
    if type(p_choice) == list:
        for p_c in p_choice:
            p_c = p_c.upper() #convert to uppercase
            char_s = add_characters(p_c, char_s)
            
    else: #if user only chose a singular choice
        p_choice = p_choice.upper() #convert to uppercase
        char_s = add_characters(p_choice, char_s)
    
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
        
        digest = digest_query() #Unreversable cryptography of message
        method = get_method() #choosing between methods provided
        rep = rep_query() #number of times a letter can repeat
        p_len = get_pw_len() #length of password
        char_s = get_char_s() #get list of possible charcaters
        start = t.time() #start timer
        
        if method == 1:
            
            print('please wait as messages of length %d are being tested via brute force method' % p_len)
            print()
            
            BF(digest, p_len, rep, char_s, start)
        
        elif method == 2:
            
            print('please wait as random messages of length %d are being tested via random method' % p_len)
            print()
            
            R(digest, p_len, rep, char_s, start)
            #end of time and time taken is handled within Random.py file.
        
main()
        