# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 17:50:19 2023

@author: Amani Njoroge
"""

#from https://realpython.com/lru-cache-python/ __________________________
#Allows me to use lru_cache in limitations of time rather than just space
#No maxsize, but expiration date to evict item in cache is 3 hours
from functools import lru_cache
import hashlib

def get_bitsize(*args):
    a = max(args) #get maximum value
    a = bin(a)[2:] #get binary value without the '0b' in it
    for l in [4, 8, 16, 32, 64]:
        if len(a) <= l : 
            return l
 
# Decimal to binary conversion
def dec2bin(num):
    return bin(num)[2:].zfill(get_bitsize(num))
    
# String to binary conversion
def string2bin(string):
    
    b_list= [] #List of binary values
    
    for s in string:
        dec = ord(s) #Convert character to decimal ascii value
        b = dec2bin(dec) #Convert Ascii value to binary
        b_list.append(b) #Add it to list

    return ''.join(b_list)

def padding(string):
    
    bits = string2bin(string) #converting string to string of binary digits
    bit_len = len(bits) #length of those binary digits
    
    #step 1 of padding process
    bits = bits + '1'
        
# =============================================================================
#     The last 64 bits of the last 512-bit block are reserved 
#     for the bit description of the length of the original message
# =============================================================================
    bits += '0'*(448-bit_len-1) # -1 is added casue of adding the bit '1'
# =============================================================================
#     first 32 bits of the last 64 bits should be empty
#     if the bit_len < 2**32
# =============================================================================
    # becuase 28 character input gives bit_len = 223
    bits += '0'*32 
    
    #convert length of input string into 32 bits of binary code
    #by adding 0's in the beginning
    bits += dec2bin(bit_len).zfill(32)
    
    #finally add them to make total of 512 bits in the block
    return bits
    
def get_message_schedule(block):

    ms = [] # ms = Message Schedule
    
    for i in range(0,512,32): #for first 16 'words'
        
        # i = intial index of current sub-block
        # i+32 = final index of current sub-block
        sub_block = block[i:i+32]

        ms.append(sub_block) #Add to schedule array

    # Processing the proceeding 64 W_s (80-16 = 64 words)
    for i in range(16,80,1): 

        new_W = XOR(ms[i-3], ms[i-8], ms[i-14], ms[i-16])
        #making sure to shift by 1 to the left
        #rotating it is what differentiates it from SHA-0
        ms.append(rotate('l', new_W, 1))
            
    return ms

def OR(*args): 
    
    def _OR(a,b):#a and b are of same length
        return dec2bin(a | b)

    lst = [int('0b'+str(i),base=2) for i in args]
    first_done = False
    for i in range(len(lst)):
        if first_done == False: #At beginning create the variable
            answer = _OR(lst[i], lst[i+1])
            first_done = True
        #reaching last i causes index out of range error
        elif lst[i] == lst[-1]: break
        else: #Continue operation onto next binary number
            answer = _OR(int('0b'+answer,base=2), lst[i+1])
         
    return answer

def XOR(*args): #a and b are of same length
    
    def _XOR(a,b):
        return dec2bin(a ^ b)
        
    lst = [int('0b'+str(i),base=2) for i in args]
    first_done = False
    for i in range(len(lst)):
        
        if first_done == False: #At beginning create the variable
            answer = _XOR(lst[i], lst[i+1])
            first_done = True
        elif lst[i] == lst[-1]: #reaching last i causes index out of range error
            break
        else: #Continue operation onto next binary number
            answer = _XOR(int('0b'+answer,base=2), lst[i+1]) 
            
    if answer == '0': #if comparing between 0 and 0 (in terms of decimal values)
        answer = '0'*32 #give value 0 with str_length of 32 bits
        
    return answer

#Only takes in two values due to non-commutative property
def AND(a,b):
    a,b = int('0b'+a,base=2), int('0b'+b,base=2)
    return dec2bin(a & b)

#t = stage
def function(t, B, C, D): 
    if t == 1:
        return  OR(AND(B,C),dec2bin((~(int('0b'+B,base=2))) & int('0b'+D,base=2)))
    elif t == 2 or t == 4:
        return XOR(B,C,D)
    else: #t == 3
        return OR(AND(B,C),AND(B,D),AND(C,D))
    
#rotates the number 'n' by rot-times to left or right
def rotate(typ, n, rot):
    
    #converting string binary to decimal
    n = int('0b'+ n, base=2) 
    
    bitsize = get_bitsize(n) #get proper bit length where 512%length = 0
    # Normalize the rotation by taking modulo with the bit size
    rot = rot % bitsize
    if typ == 'l':
        # Perform the left rotation using bitwise shift operators
        n = (n << rot | n >> (bitsize - rot)) & ((1 << bitsize) - 1)

    elif typ == 'r':
        # Perform the right rotation using bitwise shift operators 
        n = (n >> rot | n << (bitsize - rot)) & ((1 << bitsize) - 1)
    
    return bin(n)[2:].zfill(bitsize)

def ROUND(t, A, B, C, D, E, W_t, K):
    
    f = function(t, B, C, D)
    rot_A = rotate('l', A, 5)
    new_A = bin_sum(rot_A, f, E, W_t, K)
    rot_B = rotate('r', B, 2) #same as rotate('l', B, 30) 
    
    return new_A, A, rot_B, C, D
        
#For modulo 2^32 addition
def bin_sum(*args):# 32 bit + 32 bit: loss of 33 bit in process

    def _bin_sum(a,b): # Where len(a) = len(b)

        # Perform the bit sum using bitwise operators
        bitsize = get_bitsize(a,b)
        hex_string = '0x' + 'f'*(int(bitsize/4))
        
        # Take the sum and bitwise AND with 8-bit mask (0xff)
        result = (a + b) & int(hex_string,base=16) 
        
        # Convert the result to binary and pad with leading zeros
        return bin(result)[2:].zfill(bitsize) 
    
    #make sure all arguement variables are strings
    lst = [int('0b'+str(i),base=2) for i in args] 
    for i in range(len(lst)):
        
        if lst[i] == lst[0]: #At beginning create the variable
            answer = _bin_sum(lst[i], lst[i+1])
        
        if lst[i] == lst[-1]: #reaching last i causes index out of range error
            break
        
        if lst[i] != lst[0]: #Continue operation onto next binary number
            answer = _bin_sum(int('0b'+str(answer),base=2), lst[i+1])
       
    return answer

def get_digest(message): #Basically doing SHA-1
    
    def my_get_digest(message):
        block = padding(message)
        W_s = get_message_schedule(block)
    
        #initialized hash-values according to SHA-1 hashing technique
        A = '01100111010001010010001100000001' #hex->'67452301'
        B = '11101111110011011010101110001001' #hex->'EFCDAB89'
        C = '10011000101110101101110011111110' #hex->'98BADCFE'
        D = '00010000001100100101010001110110' #hex->'10325476'
        E = '11000011110100101110000111110000' #hex->'C3D2E1F0'
        
        A_1, B_1, C_1, D_1, E_1 = A, B, C, D, E
        
        for Round in range(80): #from round 0 to round 79
            if Round < 20: 
                t = 1
                K = '01011010100000100111100110011001' #hex->'5A827999'
            elif Round < 40: 
                t = 2
                K = '01101110110110011110101110100001' #hex->'6ED9EBA1'
            elif Round < 60: 
                t = 3
                K = '10001111000110111011110011011100' #hex->'8F1BBCDC'
            else: 
                t = 4 #from t = 60 to t =79
                K = '11001010011000101100000111010110' #hex->'CA62C1D6'
    
            A_1,B_1,C_1,D_1,E_1 = ROUND(t, A_1, B_1, C_1, D_1, E_1, W_s[Round], K)
            
        A_1, B_1, C_1 = bin_sum(A_1,A), bin_sum(B_1,B), bin_sum(C_1,C)
        D_1, E_1 = bin_sum(D_1,D), bin_sum(E_1,E)
        
        #Give back final digest
        return hex(int('0b'+A_1 + B_1 + C_1 + D_1 + E_1,base=2))[2:]
    
    #From https://www.geeksforgeeks.org/sha-1-hash-in-java/ 
    #And converted into python code
    def get_digest_inbuilt(message):
        md = hashlib.sha1()
        md.update(message.encode())
        messageDigest = md.digest()
        no = int.from_bytes(messageDigest, byteorder='big')
        return hex(no)[2:].zfill(32)
    
    #for words with length 10 or shorter use pythons inbuilt version of sha_1
    if len(message) <= 10:
        return get_digest_inbuilt(message)
    else: #otherwise use my own version of sha_1
        return my_get_digest(message)

#Created only for usage in Random.py due 
#to replication of messages that are being tested
@lru_cache(maxsize = 100000)
def get_digest_R(message):
    return get_digest(message)

def show_time_taken(seconds, granularity=10):
    
    intervals = (
        ('Millenia', 60**2 * 24 * 7 * 4 * 12 * 10**3),
        ('Cents', 60**2 * 24 * 7 * 4 * 12 * 10**2),
        ('Decades', 60**2 * 24 * 7 * 4 * 12 * 10),
        ('Yrs', 60**2 * 24 * 7 * 4 * 12),
        ('Mths', 60**2 * 24 * 7 * 4),
        ('Wks', 60**2 * 24 * 7),
        ('Days', 60**2 * 24),
        ('hrs', 60**2), 
        ('mins', 60),
        ('secs', 1),
        ('ms', 1*10**-3),
        ('microsecs', 1*10**-6)
    )
    
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(int(value), name))
    if result == []:
        print("Time taken: Less than a microsecond")
    else:
        print('Time taken: ' + ', '.join(result[:granularity]))
    