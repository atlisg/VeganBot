#!/usr/bin/env python3
from pprint import pprint
import os
import csv
import json
from collections import Counter
from stemming.porter2 import stem
from PyDictionary import PyDictionary
import re

keys = [ 'anim', 'vegan', 'like', 'harm', 'dog', 'take', 'kill', 'suffer', 'cow', 'fine', 'cultur', 'cat', 'matter', 'right', 'meat', 'about', 'never', 'without', 'human', 'surviv', 'beef', 'some', 'bacon' ]
real_dict = PyDictionary()
syns = {}

def process_sentence(s):
    words = s.lower().split()
    l = []
    for w in words:
        r = re.findall('\w', w)
        r = ''.join(r)
        if r != '':
            l.append(stem(r))
    return l

# import data from guide
lines = []
with open('Guide.txt') as f:
    for x in f:
        line = x.strip()
        if line != '':
            lines.append(line)

# process justifications
jst_words = []
justifs = lines[2:68]
justifs_dict = {}
for j in justifs:
    spl = j.split(' ',maxsplit=1)
    l = process_sentence(spl[1])
    for x in l:
        if x not in keys:
        	jst_words.append(x)
    justifs_dict[spl[0]] = l

# process answers
stoppers = [ "Yeah", "Kill", "You'", "If e", "It's" ]
answers = lines[69:]
answers_dict = {}
for i,a in enumerate(answers):
    if a[0].isdigit():
        spl = a.split(' ',maxsplit=1)
        l = [ spl[0] ]
        i += 1
        while i < len(answers) and not answers[i][0].isdigit() and answers[i][:4] not in stoppers:
            l.append(answers[i])
            i += 1
            answers_dict[l[0]] = '\n'.join(l[1:])

# convert to json files
with open('justifs.json', encoding='utf-8', mode='w') as j:
	json.dump(justifs_dict, j)
with open('answers.json', encoding='utf-8', mode='w') as a:
	json.dump(answers_dict, a)