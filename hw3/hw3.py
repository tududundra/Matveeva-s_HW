# В Сети появилось видео визита Грефа в Сбербанк под видом инвалида

import urllib.request as ur
import re
import html


def downloader():
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    f = open('links', 'r', encoding='UTF-8')
    urls = f.readlines()
    f.close()
    for link in urls:
        req = ur.Request(link, headers={'User-Agent': user_agent})
        with ur.urlopen(req) as response:
            html = response.read().decode('utf-8')
            yield html


def reader():
    d = downloader()
    text_arr = []
    for html in d:
        reg2 = re.findall('<p>(.+?)</p>', html)
        if reg2 != []:
            text = ' '.join(reg2)
            text_arr.append(text)
    return text_arr


def cleaner(text_arr):
    clean_arr = []
    for el in text_arr:
        el = re.sub('<.*?>', ' ', el)
        el = re.sub('&.+?;', ' ', el)
        el = re.sub('[/()\.\?,\$!–\"«»№:—=1-90]', '', el)
        el = re.sub(' +', ' ', el)
        el = re.sub('\xa0', ' ', el)
        html.unescape(el)
        clean_arr.append(el)
    return clean_arr




def counter(text_arr):

    arr1 = text_arr[0].split(' ')
    set1 = set(arr1)
    arr2 = text_arr[1].split(' ')
    set2 = set(arr2)
    arr3 = text_arr[2].split(' ')
    set3 = set(arr3)
    arr4 = text_arr[3].split(' ')
    set4 = set(arr4)
    crossing = set1 & set2 & set3 & set4
    unique1 = set1 - set2 - set3 - set4
    unique2 = set2 - set1 - set3 - set4
    unique3 = set3 - set1 - set2 - set4
    unique4 = set4 - set1 - set2 - set3
    f_crossing = open('crossing.txt', 'w', encoding='UTF-8') #файл с общими словами
    for el in sorted(crossing):
        f_crossing.write(el + '\n')
    f_crossing.close()
    f_unique = open('unique.txt', 'w', encoding='UTF-8') #файл с уникальными словами
    unique = unique1 | unique2 | unique3 | unique4
    for w in unique:
        if ' ' in w:
            un = set(w)
            unique = un | unique
    for word in sorted(unique):
        text = ' '.join(text_arr)
        a = text.split(' ')
        word = word.strip(' ,.?<>():;\"«»=')
        if a.count(word) > 1:
            f_unique.write(word + '\n')




def main():
    d = counter(cleaner(reader()))


main()
