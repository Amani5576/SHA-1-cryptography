# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 01:16:50 2023

@author: Amani
"""
import matplotlib.pyplot as plt
 
# import winsound
# duration = 1000  # milliseconds
# freq = 440  # Hz

# sound = 
# winsound.PlaySound(sound, flags)    

from SHA_1 import bin_sum, show_time_taken, dec2bin
import time as t

def get_bitsize(*args):
    a = max(args) #get maximum value
    a = bin(a)[2:] #get binary value without the '0b' in it
    for l in [4, 8, 16, 32, 64]:
        if len(a) <= l : 
            return l

def bit_sum(a, b):
    # Perform the bit sum using bitwise operators
    bitsize = get_bitsize(a,b)
    hex_string = '0x' + 'f'*(int(bitsize/4))
    result = (a + b) & int(hex_string,base=16) # Take the sum and bitwise AND with 8-bit mask (0xff)
    return bin(result)[2:].zfill(bitsize) # Convert the result to binary and pad with leading zeros


def rotate(typ, n, rot, bitsize):
    # Normalize the rotation by taking modulo with the bit size
    rot = rot % bitsize
    if typ == 'l':
        # Perform the left rotation using bitwise shift operators
        n = (n << rot | n >> (bitsize - rot)) & ((1 << bitsize) - 1)
        return bin(n)[2:].zfill(bitsize)
    
    elif typ == 'r':
        # Perform the right rotation using bitwise shift operators 
        n = (n >> rot | n << (bitsize - rot)) & ((1 << bitsize) - 1)
        return bin(n)[2:].zfill(bitsize)

def add_then_rotate_left(a,b,rot = 5):

    bitsize = get_bitsize(i, i+1)
    
    num = bit_sum(i, i+1)
    
    num = int(num, base=2)
    
    rotated_num = rotate('l', num, rot, bitsize)
    
    return rotated_num.zfill(bitsize) # Output: 0b10110, equivalent to 22 in decimal


# # Example usage
# a = 0b11011011 # First 8-bit number
# b = 0b01010101 # Second 8-bit number

def my_add_then_rotate_left(a,b,rot = 5):
    h = bin_sum(dec2bin(i), dec2bin(i+1))
    res = h.zfill(get_bitsize(int('0b' + h,base =2)))
    from SHA_1 import rotate
    rot_res = rotate('l', res, rot)
    return rot_res
# =============================================================================
# 
# =============================================================================
new_t = []
max_range_new = []
old_t = []
max_range_old = []


for k in range(5000):
            
    n1= 0
    n2= k
    
    start_1 = t.time()
    for i in range(n1,n2):
        if i == n2-1:
            end_1 = t.time()
            new_t.append(end_1-start_1)
            max_range_new.append(k)
            break
        else:
            h = add_then_rotate_left(i, i+1)
            
    start_2 = t.time()
    for i in range(n1,n2):
        if i == n2-1:
            end_2 = t.time()
            old_t.append(end_2-start_2)
            max_range_old.append(k)
            break
        else:
            h = my_add_then_rotate_left(i, i+1)

m=20
plt.figure(figsize=(m,m))
plt.title('Difference between new and old method')
plt.ylabel('runtime')
plt.xlabel('max range')
plt.scatter(max_range_new, new_t, label = 'new')
plt.scatter(max_range_old, old_t, label = 'old')
plt.legend()
plt.show()