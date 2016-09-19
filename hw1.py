#http://www.resbash.ru/
import urllib.request as ur
import re
def opening(name):
    page = ur.urlopen(name)
    text = page.read().decode('utf-8')
    return text
def working(tx):
    titles1 = []
    titles2 = []
    titles = re.findall('_zag.>(.+?)</a>', tx)
    for el in titles:
        if '<' in el:
            el1 = re.search('_zag.>(.+?)', el)
        elif '(' in el:
            continue
        elif el in titles1:
            continue
        else:
            titles1.append(el)
    titles2 = '\n'.join(titles1)
    print(titles2)
    return(titles2)
def writing(titles):
    fw = open('results.tsv', 'w', encoding = 'utf-8')
    fw.write(titles)
    fw.close
def main():
    q1 = writing(working(opening(input('Please, give me url '))))
main()
