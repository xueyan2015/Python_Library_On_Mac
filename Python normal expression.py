#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 21:02:21 2017

@author: xueyan
"""



import re

key = r"javapythonhtmlvhdl"#这是源文本
p1 = r"python"#这是我们写的正则表达式
pattern1 = re.compile(p1)#同样是编译
matcher1 = re.search(pattern1,key)#同样是查询
print(matcher1.group(0))

p = re.compile('[a-z]+')
p.match("")
print(p.match(""))

m = p.match( 'tempo')
print(m)
m.start()
m.end()
m.span()
m.group(0)

try:
    m.group(1)
except EOFError:
    print('Error 1')
except:
    print('Error 2')
    

p = re.compile('ab*')
m2 = p.match('ab123')
m2.span()


str_list = ['ab123', 'abc345', "345abc"]
store = []
for obj in str_list:
    print(obj)
    #print(p.match(obj).span())
    s=p.match(obj)
    print(s)
    #print(s.span())
    print(type(s))
    if(s!= None):   #this one works
        store.append(True)
    else:
        store.append(False)
print(store)  
 
type(str_list)

''' another approach -- this code seems compact than above'''
p = re.compile('ab*')
store2 = []
str_list = ['ab123',  "345abc" , 'abc345']

for i, obj in enumerate(str_list):
    
    temp_matched = p.match(obj)
    
    if temp_matched:
        
        store2.append(str_list[i])
        
print(store2)
        

''' ========= '''

a=2
if(a!=1):
    print("Unequal")
    
'''
'''

[ "t"n"r"f"v]

p = re.compile('\d+')
p.findall('12 drummers drumming, 11 pipers piping, 10 lords a-leaping')

print(re.match(r'From\s+', 'Fromage amk'))

print(re.match(r'Fromage\s+', 'Fromage amk'))

print(re.match(r'From\s+', 'From amk Thu May 14 19:12:10 1998'))

p2 = re.compile(r'\d+')
p2.findall('12 drummers drumming, 11 pipers piping, 10 lords a-leaping')

m = re.match('hello', 'hello world!')
print(m.group())


p = re.compile('\d+')
print(p.split('one1two2three3four4'))

p = re.compile(r'(\w+) (\w+)')
s = 'i say, hello world!'
print(p.subn(r'\2 \1', s))























