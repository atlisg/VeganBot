import re
import os
import csv
from pprint import pprint
from flask import Flask, render_template, request
from collections import Counter
from stemming.porter2 import stem
import argparse
from PyDictionary import PyDictionary
import datetime

parser = argparse.ArgumentParser(description="VeganBot : A chatty robot that supports veganism")
parser.add_argument("-v", "--key", help="write to file the key that had the most hits, the number of most hits and the list of keywords for that key, along with the user input", action="store_true")
parser.add_argument("-e", "--justifications", help="write to file the justifications list", action="store_true")
parser.add_argument("-g", "--justifications-dict", help="write to file the justifications dictionary", action="store_true")
parser.add_argument("-a", "--answers", help="write to file the answers list", action="store_true")
parser.add_argument("-n", "--answers-dict", help="write to file the answers dictionary", action="store_true")
parser.add_argument("-b", "--commons", help="write to file the commons list", action="store_true")
parser.add_argument("-o", "--synonyms", help="turn on synonyms for keyword lists. WARNING: Will take a while to process (couple of minutes)", action="store_true")
parser.add_argument("-t", "--synonyms-input", help="turn on synonyms for user input. WARNING: Replies from the bot might take a bit longer (few seconds)", action="store_true")
args = parser.parse_args()

app = Flask(__name__)

now = datetime.datetime.now().isoformat().split('T')
with open('log.txt', mode='a') as f:
    f.write('\n************ Running vegan_bot.py on ' + now[0] + ' at ' + now[1].split('.')[0] + ' ************\n\n')

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

def get_synonyms(w):
    if w not in syns:
        syns[w] = real_dict.synonym(w)
    ret = [ w ]
    if syns[w] != None:
        for x in syns[w]:
            if x not in commons:
                ret.append(stem(x))
    return ret

lines = []
with open('src.txt') as f:
    for x in f:
        line = x.strip()
        if line != '':
            lines.append(line)
jst_words = []
justifs = lines[2:71]
justifs_dict = {}
for j in justifs:
    spl = j.split(' ',maxsplit=1)
    l = process_sentence(spl[1])
    for x in l:
        if x not in keys:
            jst_words.append(x)
    justifs_dict[spl[0]] = l
c = Counter(jst_words)
c = c.most_common(33)
commons = [ x[0] for x in c ]

if args.synonyms:
    synonyms = 'synonyms.csv'
    if not os.path.isfile(synonyms):
        print('Generating synonyms, could take a couple of minutes...')
        j_dict = {}
        for x in justifs_dict:
            j_words = []
            for y in justifs_dict[x]:
                if y not in commons:
                    m = get_synonyms(y)
                    for i in m:
                        j_words.append(i)
            j_dict[x] = j_words
        writer =csv.writer(open(synonyms, 'w'))
        for key, val in j_dict.items():
            writer.writerow([key, val])
    else:
        j_dict = {}
        for key, val in csv.reader(open(synonyms)):
            j_dict[key] = val
    justifs_dict = j_dict

stoppers = [ "Yeah", "Kill", "You'", "If e", "It's" ]
answers = lines[72:]
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

if args.justifications:
    with open('log.txt', mode='a') as f:
        pprint('justifs:', f)
        pprint(justifs, f)
        f.write('\n')
if args.justifications_dict:
    with open('log.txt', mode='a') as f:
        pprint('justifs_dict:', f)
        pprint(justifs_dict, f)
        f.write('\n')
if args.answers:
    with open('log.txt', mode='a') as f:
        pprint('answers:', f)
        pprint(answers, f)
        f.write('\n')
if args.answers_dict:
    with open('log.txt', mode='a') as f:
        pprint('answers_dict:', f)
        pprint(answers_dict, f)
        f.write('\n')
if args.commons:
    with open('log.txt', mode='a') as f:
        pprint('most common (not keywords):', f)
        pprint(commons, f)
        f.write('\n')

conv_list = []

@app.route("/", methods=['GET', 'POST'])
def process_input():
    if request.method == 'POST':
        counter_dict = { x: 0 for x in justifs_dict }
        max_count = 0
        max_key = ''
        inp = request.form['justification']
        inp_list = process_sentence(inp)
        sx_whole = []

        for x in inp_list:
            if x not in commons:
                if args.synonyms_input:
                    sw = get_synonyms(x)
                    sx = []
                    for z in sw:
                        sx.append(z)
                        sx_whole.append(z)
                else:
                    sx = [ x ]
                for y in sx:
                    for j in justifs_dict:
                        if y in justifs_dict[j] and y not in commons:
                            counter_dict[j] += 1
                            if counter_dict[j] > max_count:
                                max_count = counter_dict[j]
                                max_key = j
                            if counter_dict[j] == max_count:
                                if len(justifs_dict[j]) < len(justifs_dict[max_key]):
                                    max_key = j

        if max_count == 0:
            bot = "I'm sorry, I didn't quite understand. Please rephrase."
            if args.key:
                with open('log.txt', mode='a') as f:
                    pprint('No matches found for ' + inp, f)
        else:
            bot = answers_dict[max_key]
            if args.key:
                with open('log.txt', mode='a') as f:
                    f.write('\nuser input: ' + inp + '\n')
                    f.write('max_key: ' + max_key + ' with ' + str(max_count) + ' hit(s)\n')
                    f.write('keywords for ' + max_key + ':\n')
                    pprint(justifs_dict[max_key], f)
                    if args.synonyms_input:
                        f.write('synonyms from user input:\n')
                        pprint(sx_whole, f)
                    else:
                        f.write('user input:')
                        pprint(inp_list, f)
        conv_list.append((inp, bot))
    return render_template('veganbot.html', conv_list=conv_list)

if __name__ == "__main__":
    app.run()


