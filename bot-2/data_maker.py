from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()
import re

def full_data():
    f = open('1grams-3.txt', 'r', encoding='UTF-8')
    text = f.read()
    f.close()
    lemms = re.findall('[1-90]+\t(.+)', text)
    print(lemms)
    fl = open('full_data.txt', 'a', encoding='UTF-8')
    d = {}
    d['NOUN, anim, femn'] = []
    d['NOUN, inan, femn'] = []
    d['NOUN, anim, masc'] = []
    d['NOUN, inan, masc'] = []
    d['NOUN, anim, neut'] = []
    d['NOUN, inan, neut'] = []
    d['ADJF'] = []
    d['ADJS'] = []
    d['COMP'] = []
    d['VERB, perf, tran'] = []
    d['VERB, impf, tran'] = []
    d['VERB, perf, intr'] = []
    d['VERB, impf, intr'] = []
    d['INFN, perf, tran'] = []
    d['INFN, impf, tran'] = []
    d['INFN, perf, intr'] = []
    d['INFN, impf, intr'] = []
    d['PRTF'] = []
    d['PRTS'] = []
    d['GRND'] = []
    d['NUMR'] = []
    d['ADVB'] = []
    d['NPRO'] = []
    d['PRED'] = []
    d['PREP'] = []
    d['CONJ'] = []
    d['PRCL'] = []
    d['INTJ'] = []
    d['NUMB'] = []
    d['ROMN'] = []
    for lem in lemms:
        ana = morph.parse(lem)
        i = len(ana)
        ind = 0
        while ind < i:
            p = ana[ind]
            ind += 1
            PofS = p.tag.POS
            if PofS == None:
                if 'NUMB' in p.tag:
                    d['NUMB'].append(lem)
                elif 'ROMN' in p.tag:
                    d['ROMN'].append(lem)
                else:
                    print(p)
            elif PofS == 'NOUN':
                if 'anim' in p.tag:
                    if 'femn' in p.tag:
                        d['NOUN, anim, femn'].append(lem)
                    elif 'masc' in p.tag:
                        d['NOUN, anim, masc'].append(lem)
                    elif 'neut' in p.tag:
                        d['NOUN, anim, neut'].append(lem)
                else:
                    if 'femn' in p.tag:
                        d['NOUN, inan, femn'].append(lem)
                    elif 'masc' in p.tag:
                        d['NOUN, inan, masc'].append(lem)
                    elif 'neut' in p.tag:
                        d['NOUN, inan, neut'].append(lem)
            elif PofS == 'VERB':
                if 'perf' in p.tag:
                    if 'intr' in p.tag:
                        d['VERB, perf, intr'].append(lem)
                    elif 'tran' in p.tag:
                        d['VERB, perf, tran'].append(lem)
                elif 'impf' in p.tag:
                    if 'intr' in p.tag:
                        d['VERB, impf, intr'].append(lem)
                    elif 'tran' in p.tag:
                        d['VERB, impf, tran'].append(lem)
            elif PofS == 'INFN':
                if 'perf' in p.tag:
                    if 'intr' in p.tag:
                        d['INFN, perf, intr'].append(lem)
                    elif 'tran' in p.tag:
                        d['INFN, perf, tran'].append(lem)
                elif 'impf' in p.tag:
                    if 'intr' in p.tag:
                        d['INFN, impf, intr'].append(lem)
                    elif 'tran' in p.tag:
                        d['INFN, impf, tran'].append(lem)
            else:
                d[PofS].append(lem)
    print(d)
    keys = d.keys()
    print(keys)
    for key in keys:
        string = key + ':' + ','.join(d[key]) + '\n'
        fl.write(string)
    fl.close()

if __name__ == '__main__':
    s = full_data()