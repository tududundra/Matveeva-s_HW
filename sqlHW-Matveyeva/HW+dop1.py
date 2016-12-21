import re
import os


def file_opener():
    f = open('pushkin.txt', 'r', encoding='UTF-8')
    text = f.read()
    f.close()
    text = re.sub('[/()<>\$\"«»№=1-90\']', '', text)
    text = re.sub('[\.\?,!-;:—\n]', ' ', text)
    text = text.lower()
    text_arr = text.split()
    return text_arr


def file_writer(text_arr):
    fl = open('forms.txt', 'w', encoding='UTF-8')
    text = []
    for word in text_arr:
        if word != ' ':
            if word != '':
                text.append(word)
    string = ' '.join(text)
    fl.write(string)
    fl.close()


def mystemer():
    f = open('lemms.txt', 'w', encoding='UTF-8')
    f.close()
    inp = 'forms.txt'
    out = 'lemms.txt'
    os.system('mystem -cdn' + ' ' + inp + ' ' + out)


def dict_maker():
    f = open('lemms.txt', 'r', encoding='UTF-8')
    arr = f.readlines()
    dic = {}
    for el in arr:
        el = el.strip('\n')
        if '}' in el:
            print(el)
            el_arr = el.split('{')
            el_arr[1] = el_arr[1].strip('}?-\n\r')
            if el_arr[1] in dic:
                dic[el_arr[1]] = el_arr[0]
            else:
                dic[el_arr[1]] = el_arr[0]
    return dic


def insert_maker(d):
    f = open('words.txt', 'a', encoding='UTF-8')
    cor = d.items()
    ind = 0
    for el in cor:
        if 'name_of_file' in el:
            continue
        else:
            st = str(ind)
            string = 'insert into' + ' ' + 'table2' + ' ' \
                     + '(id, token, lemma) VALUES ("' + st + '","' + el[1] + '","' + el[0] + '");\n'
            f.write(string)
            ind += 1
    f.close()


def sec_table_maker(text_arr):  # id token пункт_слева пункт_справа номер_в_тексте id_из_табл_с_леммами
    f = open('words.txt', 'r+', encoding='UTF-8')
    ins_text = f.read()
    punct = '.,:;?!-'
    id_ = 0
    text_num = 1
    ins_arr = []
    text = ' '.join(text_arr)
    text = re.sub('\n', ' ', text)
    text = re.sub(' ?, ?', ' , , ', text)
    text = re.sub(' ?\. ?', ' . . ', text)
    text = re.sub(' ?: ?', ' : : ', text)
    text = re.sub(' ?\? ?', ' ? ? ', text)
    text = re.sub(' ?! ?', ' ! ! ', text)
    text = re.sub(' ?; ?', ' ; ; ', text)
    text = re.sub(' ?- ', ' - - ', text)
    text_arr = text.split()
    print(text_arr)
    for el in text_arr:
        if el in punct:
            continue
        else:
            work_el = el.lower()
            st = '"(\d+)","' + work_el + '",'
            id_lemma = re.findall(st, ins_text)
            print(id_lemma)
            lem = ''.join(id_lemma)
            if text_arr.index(el) > 0:
                left_el = text_arr[text_arr.index(el) - 1]
            else:
                left_el = None
            if text_arr.index(el) < len(text_arr) - 1:
                right_el = text_arr[text_arr.index(el) + 1]
            else:
                right_el = None
            if left_el != None:
                if left_el in punct:
                    left = left_el
                else:
                    left = ''
                if right_el != None:
                    if right_el in punct:
                        right = right_el
                    else:
                        right = ''
                    string = 'insert into' + ' ' +'table1' + ' ' \
                     + '(id, token, left_punct, right_punct, text_num, id_lemma) VALUES ("' + str(id_) + '","' \
                     + el + '","' + left + '","' + right + '","' + str(text_num) + '","' + lem + '")\n'
                    ins_arr.append(string)
                    id_ += 1
                    text_num += 1
    print(ins_arr)
    ins = ''.join(ins_arr)
    f.write(ins)


if __name__ == '__main__':
        first = file_writer(file_opener())
        second = mystemer()
        third = insert_maker(dict_maker())
        fourth = sec_table_maker(file_opener())
