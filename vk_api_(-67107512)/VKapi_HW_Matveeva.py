import urllib.request
import re
import html
import matplotlib.pyplot as plt

def Posts_downloader():
    offsets = [0, 100]
    data = ''
    for off in offsets:
        req = urllib.request.Request(
            'https://api.vk.com/method/wall.get.xml?domain=vidnoeoverhear&offset=' + str(off) + '&count=100')
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        data += result
        data_arr = data.split('</post>')
    f = open('posts.txt', 'w', encoding='UTF-8')
    f.write(data)
    f.close()
    return data_arr

def info_finder(data):
    d = {}
    for el in data:
        if '<id>' in el:
            el = html.unescape(el)
            el = re.sub('<br>', ' ', el)
            #print(el)
            post_id = re.findall(
                '<id>([1-90]+?)</id>', el)
            post_text = re.findall('<text>(.+?)</text>', el)
            post_comm = re.findall('<comments>\n *<count>([1-90]+?)</count>', el)
            #print(post_id, post_text, post_comm)
            if post_id != []:
                arr = []
                arr.append(post_text[0])
                if post_comm != []:
                    arr.append(post_comm[0])
                    d[post_id[0]] = arr
                else:
                    d[post_id[0]] = arr
    #print(d)
    return d

def Text_len(d):
    dic = {}
    for pair in d.items():
        #print(pair)
        arr = pair[1][0].split(' ')
        text_len = len(arr)
        new_arr = []
        new_arr.append(text_len)
        if len(pair[1]) != 1:
            new_arr.append(pair[1][1])
            dic[pair[0]] = new_arr
        else:
            dic[pair[0]] = new_arr
        #print(new_arr)
    #print(dic)
    return dic

def Comments_dowloader(d):
    dic = {}
    for pair in d.items():
        post_id = pair[0]
        #print(pair)
        res = ''
        if len(pair[1]) > 1:
            if int(pair[1][1]) > 100:
                offsets = []
                package = []
                offsets.append('0')
                package.append('100')
                offsets.append('100')
                fir = int(pair[1][1])
                while True:
                    fir = fir - 100
                    if fir > 100:
                        n = len(offsets)
                        offsets.append(str(100*n))
                        package.append('100')
                        continue
                    elif fir < 100:
                        package.append(fir)
                        break
                for off in offsets:
                    pack = package[offsets.index(off)]
                    req = urllib.request.Request(
                        'https://api.vk.com/method/wall.getComments.xml?owner_id=-67107512&post_id=' \
                        + post_id + '&offset=' + str(off) + '&count=' + str(pack))
                    response = urllib.request.urlopen(req)
                    result = response.read().decode('utf-8')
                    res += result
                    #print(result)
            else:
                req = urllib.request.Request(
                    'https://api.vk.com/method/wall.getComments.xml?owner_id=-67107512&post_id=' \
                    + post_id + '&count=' + pair[1][1])
                response = urllib.request.urlopen(req)
                result = response.read().decode('utf-8')
                res += result
                #print(result)
        arr = []
        arr.append(pair[1][0])
        arr.append(pair[1][1])
        arr.append(res)
        dic[pair[0]] = arr
    f = open('comments.txt', 'w', encoding='UTF-8')
    f.write(res)
    f.close()
        #print(dic)
    return dic


def Comment_info(d):
    dic = {}
    for pair in d.items():
        length = 0
        arr = []
        comments_text = []
        comments_text_first = re.findall('<text>(.+?)</text>', pair[1][2])
        for el in comments_text_first:
            el = html.unescape(el)
            el = re.sub('<br>', ' ', el)
            el = re.sub(' ?https://vk.com/.+', '', el)
            comments_text.append(el)
        #print(comments_text)
        users_id = re.findall('<uid>([1-90].+?)</uid>', pair[1][2])
        #print(users_id)
        arr.append(pair[1][0])
        for comment in comments_text:
            ins_d = {}
            if comment == '':
                length += 0
                len_com = 0
            else:
                len_com = len(comment.split(' '))
                length += len_com
            #print(length)
            comment_creator = users_id[comments_text.index(comment)]
            ins_d[comment_creator] = len_com
            #print(ins_d)
            arr.append(ins_d)
        if int(pair[1][1]) != 0:
            average_length = length/int(pair[1][1])
        else:
            average_length = 0
        #print(average_length)
        arr.append(round(average_length, 1))
        dic[pair[0]] = arr
        #print(dic)
    return dic

def Personal_info(d):
    dic = {}
    for pair in d.items():
        arr = []
        average_length = pair[1][len(pair[1])-1]
        #print(average_length)
        post_length = pair[1][0]
        #print(comment_length)
        full_data = pair[1][1:-1]
        #print(full_data)
        arr.append(post_length)
        arr.append(average_length)
        for data in full_data:
            working_arr = []
            user_dictionary = {}
            for user_and_commentlength in data.items():
                #print(user_and_commentlength)
                user_id = user_and_commentlength[0]
                req = urllib.request.Request(
                    'https://api.vk.com/method/users.get.xml?user_ids=' + str(user_id) + '&fields=bdate,city')
                response = urllib.request.urlopen(req)
                result = response.read().decode('utf-8')
                working_arr.append(user_and_commentlength[1])
                working_arr.append(result)
                user_dictionary[user_id] = working_arr
                arr.append(user_dictionary)
        dic[pair[0]] = arr
    #print(dic)
    return dic

def Age_counting(d):
    dic = {}
    for pair in d.items():
        #print(pair[0])
        full_data = pair[1][2:]
        arr = []
        post_length = pair[1][0:1]
        average_length = pair[1][1:2]
        arr.append(post_length[0])
        arr.append(average_length[0])
        for el in full_data:
            for data in el.items():
                user_dict = {}
                working_arr = []
                working_arr.append(data[1][0])
                response = data[1][1]
                town_code = re.findall('<city>([1-90]+)</city>', response)
                #print(town_code)
                if town_code == []:
                    town_code = '0'
                working_arr.append(town_code[0])
                b_date = re.findall('<bdate>([1-90.]+)</bdate>', response)
                #print(b_date)
                if b_date != []:
                    b_date_arr = b_date[0].split('.')
                    #print(b_date_arr)
                    if len(b_date_arr) == 3:
                        if int(b_date_arr[1]) > 4:
                            age = 2016 - int(b_date_arr[2])
                            #print(age)
                        else:
                            age = 2017 - int(b_date_arr[2])
                            #print(age)
                    else:
                        age = 'Не указан'
                else:
                    age = 'Не указан'
                        #print(age)
                working_arr.append(age)
                user_dict[data[0]] = working_arr
                arr.append(user_dict)
        dic[pair[0]] = arr
    #print(dic)
    Drawnings_1(dic)
    return dic

def Drawnings_1(dic):
    X_1 = []
    Y_1 = []
    for pair in dic.items():
        X_1.append(pair[1][1])
        Y_1.append(pair[1][0])
    #print(X_1, Y_1)
    plt.bar(X_1, Y_1, align='center')
    plt.title('Отношение длины поста к длине комментария')
    plt.ylabel('Длина поста')
    plt.xlabel('Округленная средняя длина комментария')
    plt.grid(True)
    plt.show()

def Stat_counter(d):
    age_dic = {}
    town_dic = {}
    for pair in d.items():
        full_data = pair[1][2:]
        for el in full_data:
            for data in el.items():
                #print(data)
                if data[1][2] != 'Не указан':
                    if data[1][2] in age_dic:
                        age_dic[data[1][2]].append(data[1][0])
                    else:
                        age_dic[data[1][2]] = []
                        age_dic[data[1][2]].append(data[1][0])
                if data[1][1] in town_dic:
                    town_dic[data[1][1]].append(data[1][0])
                else:
                    town_dic[data[1][1]] = []
                    town_dic[data[1][1]].append(data[1][0])
    #print(age_dic)
    Drawning_2(age_dic)
    #print(town_dic)
    Drawning_3(town_dic)

def Drawning_2(age_dic):
    x_2 = []
    y_2 = []
    for data in age_dic.items():
        full_length = 0
        for length in data[1]:
            full_length += length
        average_length = full_length/len(data[1])
        x_2.append(data[0])
        x_2 = sorted(x_2)
        y_2.append(round(average_length, 1))
    #print(x_2, y_2)
    plt.bar(range(len(x_2)), y_2, align='center')
    plt.title('Отношение возраста к длине комментария')
    plt.ylabel('Cредняя длина комментария')
    plt.xlabel('Возраст комментатора')
    plt.xticks(range(len(x_2)), x_2, rotation=90)
    plt.grid(True)
    plt.show()

def Drawning_3(town_dic):
    x_3 = []
    y_3 = []
    for data in town_dic.items():
        full_length = 0
        for length in data[1]:
            full_length += length
        average_length = full_length / len(data[1])
        x_3.append(str(data[0]))
        y_3.append(round(average_length, 1))
    #print(x_3, y_3)
    plt.bar(range(len(x_3)), y_3, align='center')
    plt.title('Отношение города к длине комментария')
    plt.ylabel('Cредняя длина комментария')
    plt.xlabel('Город комментатора')
    plt.xticks(range(len(x_3)), x_3, rotation=90)
    plt.grid(True)
    plt.show()



if __name__ == '__main__':
    o = Stat_counter(
        Age_counting(
            Personal_info(
                Comment_info(
                    Comments_dowloader(
                        Text_len(
                            info_finder(
                                Posts_downloader())))))))

