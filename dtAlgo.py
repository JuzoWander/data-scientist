import pandas as pd

# Проанализировав данные таблицы я нашел:
#  1. Категории, которые чаще всего посещали
#  2. Разделы, которые чаще всего посещали
#  3. Пользователь, который дольше всего находися на сайте
# Сказать что-то о пользователях, которые продолжили или бросили обучение на сайте, невозможно, так как информации в таблице недостаточно

def time(date):
    data = [int(i) for i in date.split('.')]
    t = data[0] + data[1] * 30 + data[2] * 365
    return t

db = pd.read_csv('events.csv')

sites = dict()
categories = dict()
users = dict()
for i in range(52280):
    site = db.iloc[i]['URL_visited']
    if site in sites.keys():
        sites[site] += 1
    else:
        sites[site] = 1

    category = site.replace('https://dasreda.ru/learn/', '')
    if '/' in category:
        category = category[:category.index('/')]

    if 'https:' in category:
        category = ''

    if category in categories.keys():
        categories[category] += 1
    else:
        categories[category] = 1

    user_id = db.iloc[i]['user_id']
    user_date_1 = db.iloc[i]['user_reg_date']
    user_date_2 = db.iloc[i]['visit_date']
    if user_id in users.keys():
        if time(user_date_2) > time(users[user_id][1]):
            users[user_id][1] = user_date_2
    else:
        users[user_id] = [user_date_1, user_date_2]

sites = [[i, sites[i]] for i in sites.keys()]
sites.sort(key=lambda x: x[1], reverse=True)

categories['root'] = categories.pop('')
categories = [[i, categories[i]] for i in categories.keys()]
categories.sort(key=lambda x: x[1], reverse=True)

users = [[i, users[i][0], users[i][1]] for i in users.keys()]
users.sort(key=lambda x: time(x[2]) - time(x[1]), reverse=True)


print('Топ 3 самых популярных категории на сайте:')
for i in range(3):
    print(f'  {i + 1}) Раздел {categories[i][0]} посетили {categories[i][1]} раз')

print()
print('Топ 3 самых часто посещаемых раздела на сайте:')
for i in range(3):
    print(f'  {i + 1}) Раздел {sites[i][0]} посетили {sites[i][1]} раз')

print()
print('Пользователь дольше всего находящийся на сайте:')
print(f'ID пользователя {users[0][0]} регистрация {users[0][1]} последнее посещение {users[0][2]} всего {time(users[0][2]) - time(users[0][1])} дней на сайте')