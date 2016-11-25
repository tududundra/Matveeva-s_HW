from flask import Flask
from flask import render_template, url_for, request, redirect
import json
import os

app = Flask(__name__)


def file_maker():
    if os.path.exists('results.txt') == False:
        f = open('results.txt', 'w', encoding='UTF-8')
        head = 'Имя' + '\t' + 'Выбранный вариант' + '\t' + 'Родной город' + '\t' + 'Возраст' + '\t' + 'Пол' + \
               '\t' + 'Образование' + '\t' + 'Комментарий' + '\n'
        f.write(head)


@app.route('/')
def form():
    main_url = url_for('form')
    stats_url = url_for('stats')
    json_url = url_for('json_str')
    search_url = url_for('searcher')
    f = open('results.txt', 'a', encoding='UTF-8')
    if request.args:
        name = request.args['name']
        variant = request.args['variant']
        town = request.args['town']
        age = request.args['age']
        sex = request.args['sex']
        edu = request.args['edu']
        comment = request.args['comment']
        if name != '':
            f.write(name + '\t' + variant + '\t' + town + '\t' + age + '\t' + sex + '\t' + edu + '\t' + comment + '\n')
            f.close()
    return render_template('proj.html', main_url=main_url, stats_url=stats_url, json_url=json_url, search_url=search_url)


@app.route('/stats')
def stats():
    main_url = url_for('form')
    stats_url = url_for('stats')
    json_url = url_for('json_str')
    search_url = url_for('searcher')
    f = open('results.txt', 'r', encoding='UTF-8')
    answ = f.readlines()
    strok = ''
    ageframe1 = ageframe2 = ageframe3 = ageframe4 = 0
    for st in answ:
        st1 = st.split('\t')
        st1 = st1[0:6]
        if st1[3] != 'Возраст':
            if int(st1[3]) <= 18:
                ageframe1 += 1
            elif int(st1[3]) > 18 and int(st1[3]) <= 30:
                ageframe2 += 1
            elif int(st1[3]) > 30 and int(st1[3]) <= 45:
                ageframe3 += 1
            elif int(st1[3]) > 45:
                ageframe4 += 1
        st2 = '  '.join(st1)
        strok += st2 + '  '
    stat, gen1, gen2, gen3, age12, age34 = {}, {}, {}, {}, {}, {}
    arrstat = strok.split('  ')
    one = arrstat.count('рАкушка')
    two = arrstat.count('ракУшка')
    sex1 = arrstat.count('М')
    sex2 = arrstat.count('Ж')
    sex3 = arrstat.count('Затрудняюсь ответить')
    stat[one] = two
    gen1['gen1'] = sex1
    gen2['gen2'] = sex2
    gen3['gen3'] = sex3
    age12[ageframe1] = ageframe2
    age34[ageframe3] = ageframe4
    return render_template('stat.html', stat=stat, sex1=gen1, sex2=gen2, \
                           sex3=gen3, age12=age12, age34=age34, main_url=main_url, stats_url=stats_url, \
                           json_url=json_url, search_url=search_url)


@app.route('/json')
def json_str():
    main_url = url_for('form')
    stats_url = url_for('stats')
    json_url = url_for('json_str')
    search_url = url_for('searcher')
    f = open('results.txt', 'r', encoding='UTF-8')
    strarr = f.readlines()
    d = {}
    for el in strarr:
        if el == strarr[0]:
            elarr = el.split('\t')
            name = elarr[0]
            d[name] = []
            variant = elarr[1]
            d[variant] = []
            town = elarr[2]
            d[town] = []
            age = elarr[3]
            d[age] = []
            sex = elarr[4]
            d[sex] = []
            edu = elarr[5]
            d[edu] = []
            komment = elarr[6]
            komment = komment.strip('\n')
            d[komment] = []
        else:
            elarr1 = el.split('\t')
            d[name].append(elarr1[0])
            d[variant].append(elarr1[1])
            d[town].append(elarr1[2])
            d[age].append(elarr1[3])
            d[sex].append(elarr1[4])
            d[edu].append(elarr1[5])
            elarr1[6] = elarr1[6].strip('\n')
            d[komment].append(elarr1[6])
    json_string = json.dumps(d, ensure_ascii=False, separators=(',\n', ':'))
    return render_template('jsonstring.html', json_string=json_string, main_url=main_url, stats_url=stats_url, \
                           json_url=json_url, search_url=search_url)


@app.route('/search')
def searcher():
    main_url = url_for('form')
    stats_url = url_for('stats')
    json_url = url_for('json_str')
    search_url = url_for('searcher')
    # поиск по полу
    # поиск по варианту
    # поиск по возрасту
    if request.args:
        variant = request.args['variant']
        age = request.args['age']
        sex = request.args['sex']
        f = open('searcher.txt', 'w', encoding='UTF-8')
        st = variant + '\t' + age + '\t' + sex
        f.write(st)
        f.close()
        return redirect(url_for('results'))
    return render_template('searsherform.html', main_url=main_url, stats_url=stats_url, \
                           json_url=json_url, search_url=search_url)


@app.route('/results')
def results():
    main_url = url_for('form')
    stats_url = url_for('stats')
    json_url = url_for('json_str')
    search_url = url_for('searcher')
    fl = open('searcher.txt', 'r', encoding='UTF-8')
    fil = fl.read()
    ar = fil.split('\t')
    variant = ar[0]
    age = ar[1]
    sex = ar[2]
    arrforwork1 = []
    arrforwork2 = []
    f = open('results.txt', 'r', encoding='UTF-8')
    strarr = f.readlines()
    strarr = strarr[1:]
    for el in strarr:
        el1 = el.split('\t')
        if variant == 'не имеет значения' or variant in el1:
            if age != 'не имеет значения':
                if age == '<19' and int(el1[3]) <= 18:
                    arrforwork1.append(el1)
                elif age == '19-30' and int(el1[3]) > 18 and int(el1[3]) <= 30:
                    arrforwork1.append(el1)
                elif age == '31-45' and int(el1[3]) > 30 and int(el1[3]) <= 45:
                    arrforwork1.append(el1)
                elif age == '45+' and int(el1[3]) > 45:
                    arrforwork1.append(el1)
            else:
                arrforwork1.append(el1)
            if sex != 'не имеет значения':
                if sex in el1:
                    arrforwork2.append(el1)
            else:
                arrforwork2.append(el1)
    f.close()
    n = 0
    result = {}
    resu = []
    for elem in arrforwork2:
        n += 1
        result[n] = elem
    return render_template('restable.html', result=result, main_url=main_url, stats_url=stats_url, \
                           json_url=json_url, search_url=search_url)


if __name__ == '__main__':
    p = file_maker()
    app.run()
