from flask import Flask
from flask import render_template, url_for, request, redirect
import re
import os

app = Flask(__name__)


@app.route('/')
def form():
    if request.args:
        name = request.args['file_name']
        text = request.args['file_text']
        text = re.sub('[/()<>\$\"«»№=1-90\']', '', text)
        text = re.sub('[\.\?,!-;:—]', ' ', text)
        text = text.lower()
        text_arr = text.split()
        text_set = set(text_arr)
        fl = open('forms.txt', 'w', encoding='UTF-8')
        for word in text_set:
            if word != ' ':
                if word != '':
                    fl.write(word + '\n')
        f = open('file_name.txt', 'w', encoding='UTF-8')
        f.write(name)
        f.close()
        fl.close()
        second = mystemer()
        third = insert_maker(dict_maker())
    return render_template('main.html')


def mystemer():
    f = open('lemms.txt', 'w', encoding='UTF-8')
    f.close()
    inp = 'forms.txt'
    out = 'lemms.txt'
    os.system('mystem -cd' + ' ' + inp + ' ' + out)


def dict_maker():
    f = open('lemms.txt', 'r', encoding='UTF-8')
    fl = open('file_name.txt', 'r', encoding='UTF-8')
    name = fl.read()
    arr = f.readlines()
    dic = {}
    dic['name_of_file'] = name
    for el in arr:
        el_arr = el.split('{')
        el_arr[1] = el_arr[1].strip('}?-\n')
        if el_arr[1] in dic:
            dic[el_arr[1]] = el_arr[0]
        else:
            dic[el_arr[1]] = el_arr[0]
    return dic


def insert_maker(d):
    cor = d.items()
    name = d['name_of_file']
    ind = 0
    file_name = name + '.txt'
    f = open(file_name, 'a', encoding='UTF-8')
    for el in cor:
        if 'name_of_file' in el:
            continue
        else:
            st = str(ind)
            string = 'insert into' + ' ' + name + ' ' \
                     + '(id, token, lemma) VALUES ("' + st + '","' + el[1] + '","' + el[0] + '");\n'
            f.write(string)
            ind += 1
    f.close()

if __name__ == '__main__':
    app.run()
    second = mystemer()
    third = insert_maker(dict_maker())