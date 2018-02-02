<<<<<<< HEAD
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
        print(reg2)
        if reg2 != []:
            text = ' '.join(reg2)
            text_arr.append(text)
    return text_arr


def cleaner(text_arr):
    for el in text_arr:
        el.replace('\xa0', ' ')
        html.unescape(el)
    return text_arr


#def arr_maker():
#    text_arr = []
#    while len(text_arr) != 5 :
#        clean_text = cleaner ()
#        text_arr.append(clean_text)
#    return text_arr


def counter(text_arr):
    f = open('links', 'r', encoding='UTF-8')
    urls = f.readlines()
    f.close()
    arr1 = text_arr[0].split(' ')
    set1 = set(arr1)
    print(set1)
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
    f_crossing = open('crossing.txt', 'a', encoding='UTF-8')
    for el in sorted(crossing):
        f_crossing.write(el + '\n')
    f_crossing.close()
    f_unique = open('unique.txt', 'a', encoding='UTF-8')
    f_unique.write(urls[0])
    for el1 in sorted(unique1):
        a = text_arr[0].split(' ')
        el1 = el1.strip(',.?<>():;')
        if a.count(el1) > 1:
            f_unique.write(el1 + '\n')
    f_unique.write(urls[1])
    for el2 in sorted(unique2):
        a = text_arr[1].split(' ')
        el2 = el2.strip(',.?<>():;')
        if a.count(el2) > 1:
            f_unique.write(el2 + '\n')
    f_unique.write(urls[2])
    for el3 in sorted(unique3):
        a = text_arr[2].split(' ')
        el3 = el3.strip(',.?<>():;')
        if a.count(el3) > 1:
            f_unique.write(el3 + '\n')
    f_unique.write(urls[3])
    for el4 in sorted(unique4):
        a = text_arr[3].split(' ')
        el4 = el4.strip(',.?<>():;')
        if a.count(el4) > 1:
            f_unique.write(el4 + '\n')



def main():
    d = counter(cleaner(reader()))


main()
=======
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
>>>>>>> ddea5461c8482fcda4a99685f5e6a6a9c712500f
