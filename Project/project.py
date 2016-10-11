import urllib.request as ur
import os
import re
import time
import html


# 1874-1893(83)

def counter():
    d = []
    for n in range(1904, 1913):
        pageurl = 'http://zariagazeta.ru/?module=articles&action=view&id=' + str(n)
        d.append(pageurl)
    #print(d)
    return d


def downloader():
    d = counter()
    text_dict = {}
    print('я загружаю')
    for pageurl in d:
        page = ur.urlopen(pageurl)
        text = page.read().decode('UTF-8')
        text1 = text + 'url' + pageurl + 'url'
        text_dict[pageurl] = text1
        #print('пиу')
        time.sleep(3)
    return text_dict


def metainfo_finder(text_dict):
    print('ищу мету')
    meta_arr = []
    for el in text_dict:
        meta = []
        text = text_dict[el]
        head = re.findall('style=\'\' /><span class=\'h_2 name\'><h1>(.+?)</h1>', text)
        if head == []:
            print('Error at: ' + el)
            continue
        else:
            meta.append(head[0])
            date = re.findall('</span><span class=\'date_start\'>(.+?)</span><span class', text)
            date[0] = date[0][8:10] + date[0][4:8] + date[0][0:4]
            meta.append(date[0])
            autor = re.findall('</p><p>([^<>.,-?!:;(Фото)]+?)\.</p></span><span class=\'author\'', text)
            if autor == []:
                autor.append('Noname')
            autor[0] = html.unescape(autor[0])
            meta.append(autor[0])
            pageurl = el
            meta.append(pageurl)
            meta[1] = meta[1].replace('-', '.')
            print(meta)
            meta_arr.append(meta)
    return meta_arr


def text_cleaner(text_dict):
    print('я тут')
    clean_arr = []
    for el in text_dict:
        text_arr = []
        text = text_dict[el]
        clean_t = re.findall('<p><strong>(.+?)</p></span>', text)
        if clean_t == []:
            clean_t = re.findall('</span><span class=\'intro\'>(.+?)</p></span>', text)
            if clean_t == []:
                continue
        clean_text = clean_t[0]
        clean_text = re.sub('<.*?>', ' ', clean_text)
        clean_text = re.sub('\xa0', ' ', clean_text)
        clean_text = re.sub('</p><p>', '\n', clean_text)
        clean_text = html.unescape(clean_text)
        clean_text = re.sub('http://www\..+?\.(ru|com)', ' ', clean_text)
        text_arr.append(el)
        text_arr.append(clean_text)
        clean_arr.append(text_arr)
    print(clean_arr)
    return clean_arr


def walker(meta_arr, text_arr):
    print('cоздаю папки')
    dir_arr = []
    i = 0
    for meta in meta_arr:
        directory = './Zaria/plain/' + meta[1][6:10] + '/' + meta[1][3:5] + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)
    for el in meta_arr:
        for texturl in text_arr:
            if el[3] == texturl[0]:
                file_arr = []
                text = texturl[1]
                directory = './Zaria/plain/' + el[1][6:10] + '/' + el[1][3:5] + '/'
                files = os.listdir(directory)
                #print(files)
                name = el[1] + '.txt'
                for st in files:
                    if el[1] in st:
                        if '(' in st:
                            n = int(name[8:9])
                            name = el[1] + '(' + str(n + 1) + ')' + '.txt'
                        else:
                            name = el[1] + '(' + str(1) + ')' + '.txt'
                direct = directory + name
                file_arr.append(texturl[0])
                file_arr.append(direct)
                text = '@au' + el[2] + '\n' + '@ti' + el[0] + '' + '\n' + '@da' + el[1] + '\n' + '@url' + el[
                    3] + '\n' + text
                f = open(direct, 'w', encoding='UTF-8')
                f.write(text)
                f.close()
                dir_arr.append(file_arr)
    #print(dir_arr)
    mystem_writer(dir_arr)
    return dir_arr


def mystem_writer(dirr_arr):
    print('я в майстеме')
    for el in dirr_arr:
        inp = el[1]
        out_txt = inp.replace('plain', 'mystem-plain')
        out_xml = out_txt.replace('-plain', '-xml')
        out_xml = out_xml.replace('.txt', '.xml')
        #print(inp, out_txt, out_xml)
        directory1 = out_txt[:29]
        directory2 = out_xml[:27]
        if not os.path.exists(directory1):
            os.makedirs(directory1)
        if not os.path.exists(directory2):
            os.makedirs(directory2)
        os.system('mystem -cid' + ' ' + inp + ' ' + out_txt)
        f = open(out_txt, 'r+', encoding='UTF-8')
        fil = f.read()
        fil = re.sub('@.+?\\n', '', fil)
        f.write(fil)
        f.close()
        os.system('mystem -cid --format xml' + ' ' + inp + ' ' + out_xml)
        fl = open(out_txt, 'w+', encoding='UTF-8')
        fli = fl.read()
        fli = re.sub('@.+?\\n', '', fli)
        fl.write(fli)
        fl.close()
    print('майстем закончился')


def meta_maker(direct_arr, meta_arr):
    print('создаю файл меты')
    row_arr = []
    for el in meta_arr:
        for text_dir in direct_arr:
            if el[3] == text_dir[0]:
                direct = text_dir[1]
                row = direct + '\t' + el[2] + '\t\t\t' + el[0] + '\t' + el[1] + '\tпублицистика\t\t\t\t\
                \tнейтральный\tн-возраст\tн-уровень\tрайонная\
                \t' + el[3] + '\tЗаря\t\t' + el[1][6:10] + '\tгазета\tРоссия\tСмоленский район Алтайского края\tru'
                row_arr.append(row)
    meta_writer(row_arr)
    return row_arr


def meta_dirmaker():
    if not os.path.exists('./Zaria/'):
        os.makedirs('./Zaria/')
        if not os.path.exists('./Zaria/meta.tsv'):
            f = open('./Zaria/meta.tsv', 'w', encoding='UTF-8')
            meta_head = 'path\tauthor\tsex\tbirthday\theader\tcreated\tsphere\tgenre_fi\ttype\ttopic\tchronotop\
            \tstyle\taudience_age\taudience_level\taudience_size\tsource\tpublication\tpublisher\tpubl_year\t\
            medium\tcountry\tregion\tlanguage'
            f.write(meta_head)
            f.close()


def meta_writer(meta_arr):
    for el in meta_arr:
        f = open('./Zaria/meta.tsv', 'a', encoding='UTF-8')
        f.write(el + '\n')
        f.close()


def main():
    meta_dirmaker()
    meta_maker(walker(metainfo_finder(downloader()), text_cleaner(downloader())), (metainfo_finder(downloader())))


main()
