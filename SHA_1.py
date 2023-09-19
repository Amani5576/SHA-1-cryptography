# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 17:50:19 2023

@author: Amani Njoroge
"""

#from https://realpython.com/lru-cache-python/ __________________________
#Allows me to use lru_cache in limitations of time rather than just space
#No maxsize, but expiration date to evict item in cache is 3 hours
from functools import lru_cache, wraps
from datetime import datetime, timedelta

def timed_lru_cache(seconds: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
# ____________________________________________________________

#Hexadecimal to Binary conversion
def hex2bin(s):
    
    #making sure all letter are uppercase
    s = s.upper() 
    mp = {'0': "0000",
          '1': "0001",
          '2': "0010",
          '3': "0011",
          '4': "0100",
          '5': "0101",
          '6': "0110",
          '7': "0111",
          '8': "1000",
          '9': "1001",
          'A': "1010",
          'B': "1011",
          'C': "1100",
          'D': "1101",
          'E': "1110",
          'F': "1111"}
    bin = ""
    for i in range(len(s)):
        bin = bin + mp[s[i]]
        
    return bin

# Binary to hexadecimal conversion
def bin2hex(s):
    
    #making sure all letter are uppercase
    s = s.upper()
    
    mp = {"0000": '0',
          "0001": '1',
          "0010": '2',
          "0011": '3',
          "0100": '4',
          "0101": '5',
          "0110": '6',
          "0111": '7',
          "1000": '8',
          "1001": '9',
          "1010": 'A',
          "1011": 'B',
          "1100": 'C',
          "1101": 'D',
          "1110": 'E',
          "1111": 'F'}
    hex = ""
    for i in range(0, len(s), 4):
        ch = ""
        ch = ch + s[i]
        ch = ch + s[i + 1]
        ch = ch + s[i + 2]
        ch = ch + s[i + 3]
        hex = hex + mp[ch]
 
    return hex
 
# Binary to decimal conversion
def bin2dec(binary):
    
    binary = int(binary) #Python version 3 allows longer values for int

    decimal, i, = 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
        
    return decimal
 
# Decimal to binary conversion
def dec2bin(num):
    
    #make sure arguement is of type int
    if type(num) != int:
        num = int(num)
        
    res = bin(num).replace("0b", "")
    if(len(res) % 4 != 0):
        div = len(res) / 4
        div = int(div)
        counter = (4 * (div + 1)) - len(res)
        for i in range(0, counter):
            res = '0' + res
    return res

# String to binary conversion
def string2bin(string):
    
    b_list= [] #List of binary values
    
    for s in string:
        dec = ord(s) #Convert character to ascii value
        b = dec2bin(dec) #Convert Ascii value to binary
        b_list.append(b) #Add it to list

    return ''.join(b_list)

def dec2hex(num):
    
    #make sure arguement is of type int
    if type(num) != int:
        num = int(num)
    return bin2hex(dec2bin(num))

def hex2dec(s):
    return bin2dec(hex2bin(s))

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
    last_32bits = dec2bin(bit_len).zfill(32)
    
    #finally add them to make total of 512 bits in the block
    return bits + last_32bits
    
def get_message_schedule(block):

    ms = [] # ms = Message Schedule
    
    for i in range(0,512,32): #for first 16 'words'
        
        # i = intial index of current sub-block
        # i+32 = final index of current sub-block
        sub_block = block[ i:i+32]

        ms.append(sub_block) #Add to schedule array
        
    # Processing the proceeding 64 W_s (80-16 = 64 words)
    for i in range(16,80,1): 

        new_W = XOR(ms[i-3], ms[i-8], ms[i-14], ms[i-16])
        #making sure to shift by 1 to the left
        #rotating it is what differentiates it from SHA-0
        ms.append(rotate('l', new_W, 1))
            
    return ms

def NOT(a):
    a = str(a)
    ans = ''
    for i in a:
        if i == '0':
            ans += '1' #invert 0 to 1
        else: #if i == '1' 
            ans += '0' #invert 1 to 0
    return ans

def OR(*args): 
    
    def _OR(a,b):#a and b are of same length
        
        max_len = max(len(a), len(b))
        a, b = a.zfill(max_len), b.zfill(max_len)
        
        ans= ''
        for i in range(len(a)): #or len(b). Doesn't matter...
            if a[i] == '0' and b[i] == '0':
                ans += '0'
            else: #if either have '1'
                ans += '1'
        return ans
    
    lst = [str(i) for i in args]
    for i in range(len(lst)):
        
        if lst[i] == lst[0]: #At beginning create the variable
            answer = _OR(lst[i], lst[i+1])
        
        if lst[i] == lst[-1]: #reaching last i causes index out of range error
            break
        
        if lst[i] != lst[0]: #Continue operation onto next binary number
            answer = _OR(answer, lst[i+1])
         
    return answer

def XOR(*args): #a and b are of same length
    
    def _XOR(a,b):
        
        max_len = max(len(a), len(b))
        a, b = a.zfill(max_len), b.zfill(max_len)
        
        ans = ''
        for i in range(len(a)): #or len(b). Doesn't matter...
            if (a[i] == '0' and b[i] == '1') or (a[i] == '1' and b[i] == '0'):
                ans += '1'
            else:
                ans += '0'
        return ans, max_len
    
    lst = [str(i) for i in args]
    lengths = [] #keep track of maximum length of bits
    for i in range(len(lst)):
        
        if lst[i] == lst[0]: #At beginning create the variable
            answer, max_length = _XOR(lst[i], lst[i+1])
        
        if lst[i] == lst[-1]: #reaching last i causes index out of range error
            break
        
        if lst[i] != lst[0]: #Continue operation onto next binary number
            answer, max_length = _XOR(answer, lst[i+1]) 
            
        lengths.append(max_length)
        
    if answer == '': #if comparing between 0 and 0 (in terms of decimal values)
        answer = '0'*max(lengths) #give value 0 with str_length of max_length
        
    return answer

#This binary operation is chronological; order matters.
#Binary operation on more than two ninary numbers is NOT commutative
def AND(*args):
        
    def _AND(a,b):#a and b are of same length
        
        a = str(a); b = str(b)
        max_len = max(len(a), len(b))
        a, b = a.zfill(max_len), b.zfill(max_len)
        ans = ''
        for i in range(len(a)): #or len(b). Doesn't matter...
            if (a[i] == '1' and b[i] == '1'):
                ans += '1'
            else:
                ans += '0'
        return ans
    
    lst = [str(i) for i in args] #make sure input is string
    l = len(lst)
    for i in range(l):
        
        if lst[i] == lst[0]: #At beginning create the variable
            answer = _AND(lst[i], lst[i+1])
        
        #reaching last i causes index out of range error
        if lst[i] == lst[-1]: 
            break
        #Continue operation onto next binary number
        if lst[i] != lst[0]: 
            answer = _AND(answer, lst[i+1])

    return answer

#t = stage
def function(t, B, C, D):   
    if t == 1:
        return  OR(AND(B,C), AND(NOT(B),D))
    elif t == 2 or t == 4:
        return XOR(B,C,D)
    else: #t == 3
        return OR(AND(B,C),AND(B,D),AND(C,D))

#rotates a array n-times to left or right
def rotate(typ, arr, n):
    
    #typ = left or right
    #arr = array used for rotation
    #n = number of times to rorate
    if typ == 'l':
        return arr[n:]+arr[:n]
    elif typ == 'r':
        return arr[-n:]+arr[:-n]

def ROUND(t, A, B, C, D, E, W_t, K):
    
    f = function(t, B, C, D)
    rot_A = rotate('l', A, 5)
    new_A = bin_sum(rot_A, f, E, W_t, K)
    rot_B = rotate('r', B, 2) #same as rotate('l', B, 30) 
    
    return new_A, A, rot_B, C, D

#For modulo 2^32 addition
def bin_sum(*args):# 32 bit + 32 bit: loss of 33 bit in process

    def _bin_sum(a,b): # Where len(a) = len(b)

        max_len = max(len(a), len(b))
        a, b = a.zfill(max_len), b.zfill(max_len)

        ans = ''
        carry = 0 #Variable for carrying in case of 1+1
         
        for i in range(max_len-1, -1, -1):
            r = carry
            if a[i] == '1':
                r += 1
            if b[i] == '1':
                r += 1
            if r % 2 == 1:
                ans = '1' + ans
            else:
                ans = '0' + ans
         
            # Compute the carry.
            carry = 0 if r < 2 else 1
            #During last step, the last carry will not be added
            
        return ans
    
    #make sure all arguement variables are strings
    lst = [str(i) for i in args] 
    for i in range(len(lst)):
        
        if lst[i] == lst[0]: #At beginning create the variable
            answer = _bin_sum(lst[i], lst[i+1])
        
        if lst[i] == lst[-1]: #reaching last i causes index out of range error
            break
        
        if lst[i] != lst[0]: #Continue operation onto next binary number
            answer = _bin_sum(answer, lst[i+1])
       
    return answer

#cache expiry is within 1 hour
@timed_lru_cache(seconds = 3600, maxsize = None)
def get_digest(message): #Basically doing SHA-1
    
    block = padding(message)
    W_s = get_message_schedule(block)

    #initialized hash-values according to SHA-1 hashing technique
    A = '01100111010001010010001100000001' #hex2bin('67452301')
    B = '11101111110011011010101110001001' #hex2bin('EFCDAB89')
    C = '10011000101110101101110011111110' #hex2bin('98BADCFE')
    D = '00010000001100100101010001110110' #hex2bin('10325476')
    E = '11000011110100101110000111110000' #hex2bin('C3D2E1F0')
    
    A_1, B_1, C_1, D_1, E_1 = A, B, C, D, E
    
    for Round in range(80): #from round 0 to round 79
        if Round < 20: 
            t = 1
            K = '01011010100000100111100110011001' #hex2bin('5A827999')
        elif Round < 40: 
            t = 2
            K = '01101110110110011110101110100001' #hex2bin('6ED9EBA1')
        elif Round < 60: 
            t = 3
            K = '10001111000110111011110011011100' #hex2bin('8F1BBCDC')
        else: 
            t = 4 #from t = 60 to t =79
            K = '11001010011000101100000111010110' #hex2bin('CA62C1D6')

        A_1,B_1,C_1,D_1,E_1 = ROUND(t, A_1, B_1, C_1, D_1, E_1, W_s[Round], K)
        
    A_1, B_1, C_1 = bin_sum(A_1,A), bin_sum(B_1,B), bin_sum(C_1,C)
    D_1, E_1 = bin_sum(D_1,D), bin_sum(E_1,E)
    
    #Give back final digest
    return bin2hex(A_1 + B_1 + C_1 + D_1 + E_1) 

def show_time_taken(secs):
    #From https://stackoverflow.com/questions/27779677/how-to-format-elapsed-ti
    #me-from-seconds-to-hours-minutes-seconds-and-milliseco
    hours, rem = divmod(secs, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Time taken: {:0>2}:{:0>2}:{:05.6f}".format(int(hours),int(minutes),seconds))
