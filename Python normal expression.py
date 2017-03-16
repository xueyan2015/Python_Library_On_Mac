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



'''
Mar05, 2016-- experiment with normal expression...
'''

col_names = ['log_var1', 'Log_var1', 'var1_log', 'var2_log_abc', 'var2_log_log_abc', 'var2_log3_log_abc', 'var2_2log3_log3_log_abc']

pattern0 = re.compile('log')
print(re.match(pattern0, col_names[0]))  #<_sre.SRE_Match object; span=(0, 3), match='log'>
print(re.match(pattern0, col_names[0]).group())  #log
print(re.match(pattern0, col_names[1]))  #None
print(re.match(pattern0, col_names[2]))  #None
print(re.match(pattern0, col_names[3]))  #None

pattern0b = re.compile('log', re.I)  
print(re.match(pattern0b, col_names[0]))  # <_sre.SRE_Match object; span=(0, 3), match='log'>
print(re.match(pattern0b, col_names[0]).group())  #log
print(re.match(pattern0b, col_names[1]))  # <_sre.SRE_Match object; span=(0, 3), match='Log'>
print(re.match(pattern0b, col_names[2]))  # None
print(re.match(pattern0b, col_names[3]))  # None

print(re.search(pattern0b, col_names[0]))  #  <_sre.SRE_Match object; span=(0, 3), match='log'>
print(re.search(pattern0b, col_names[0]).group())  # log
print(re.search(pattern0b, col_names[1]))  #  <_sre.SRE_Match object; span=(0, 3), match='Log'>
print(re.search(pattern0b, col_names[2]))  #  <_sre.SRE_Match object; span=(5, 8), match='log'>
print(re.search(pattern0b, col_names[3]))  #  <_sre.SRE_Match object; span=(5, 8), match='log'>

print(re.search(pattern0b, col_names[4]))  #  <_sre.SRE_Match object; span=(5, 8), match='log'>
print(re.findall(pattern0b, col_names[4]))
for m in re.finditer(pattern0b, col_names[4]):
    print(m.group())

pattern0c = re.compile('log\d+')
pattern0d = re.compile('log\d*') 
pattern0e = re.compile('\d+log\d+')
pattern0f = re.compile('\d*log\d*')

print(re.search(pattern0c, col_names[5]))  #<_sre.SRE_Match object; span=(5, 9), match='log3'>
print(re.findall(pattern0c, col_names[5]))  # ['log3']

print(re.search(pattern0d, col_names[5]))  #<_sre.SRE_Match object; span=(5, 9), match='log3'>
print(re.findall(pattern0d, col_names[5]))  # ['log3', 'log']

print(re.search(pattern0e, col_names[6]))   #<_sre.SRE_Match object; span=(5, 10), match='2log3'>
print(re.findall(pattern0e, col_names[6]))  #['2log3']

print(re.search(pattern0f, col_names[6]))
print(re.findall(pattern0f, col_names[6]))




pattern1 = re.compile('\Alog')
print(re.search(pattern1, col_names[0]))  #<_sre.SRE_Match object; span=(0, 3), match='log'>
print(re.search(pattern1, col_names[1]))  #None
print(re.search(pattern1, col_names[2]))  #None
print(re.search(pattern1, col_names[3]))  #None


pattern2 = re.compile('\Zlog')
print(re.search(pattern2, col_names[0]))
print(re.search(pattern2, col_names[1]))
print(re.search(pattern2, col_names[2]))
print(re.search(pattern2, col_names[3]))


'''
Mar-07, 2017
'''
#find string that ends with "log"
nojoke1 = re.findall("log$", col_names[0])
nojoke2 = re.findall("log$", col_names[2])

nojoke1c = re.search("log$", col_names[0])
nojoke2c = re.search("log$", col_names[2])

print(nojoke1)
print(nojoke2)

print(nojoke1c)
print(nojoke2c)

#find string that begins with "log"
nojoke3 = re.findall(r"^log", col_names[0])
nojoke4 = re.findall(r"^log", col_names[2])

nojoke3c = re.search(r"^log", col_names[0])
nojoke4c = re.search(r"^log", col_names[2])

print(nojoke3)
print(nojoke4)

print(nojoke3c)
print(nojoke4c)
















