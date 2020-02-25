from bs4 import BeautifulSoup as Bs
import pickle
import requests
from typing import NamedTuple
import argparse
import sys
import os


from random import choice
import re

from additional_const import *
from datetime import datetime


MAIN_URL = 'https://lenta.ru'
USERAGENT = {'User-agent': choice(USERAGENTS)}
ART_TAGS = {
    'news': 'item news b-tabloid__topic_news',
    'articles': 'item article'
}


class Art(NamedTuple):
    rubric : str
    title : str
    link : str
    date : datetime

    def __str__(self):
        return ('Новость: ' if self.rubric == 'news' else 'Статья: ') + \
               self.title + datetime.strftime(self.date, ' %d.%m.%Y')

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True)
    parser.add_argument('-r', '--rubric', default=None)
    parser.add_argument('-d', '--date', default=None)

    return parser

def to_format_date(raw_date, dat_url):
    if raw_date[5] != ' ':
        raw_date = raw_date[:5] + ' ' + raw_date[5:]
    date_spl = re.sub('—', '', raw_date).split()
    if date_spl[-1].lower() == 'сегодня':
        format_date = ' '.join(date_spl[:-1]) + \
                      datetime.strftime(datetime.today(), ' %d %m %Y')
    else:
        if dat_url[:4] != '2020':
            format_date = ' '.join(date_spl[:-2] + [MONTHS[date_spl[-2]]] + [date_spl[-1]])
        else:
            format_date = ' '.join(date_spl[:-1] + [MONTHS[date_spl[-1]]] +
                                   [str(datetime.today().year)])

    return format_date

def get_art_attrs(rubric_url, date_url, dat_key):
    global all_art
    print('begin get', date_url)
    req = requests.get(f'{MAIN_URL}/{rubric_url}/{date_url}', headers=USERAGENT)
    print(req.text)
    if 'div' in req.text:
        print('diiiv')
    bs = Bs(req.text, "html.parser")
    if rubric_url == 'all':
        rubrics = ('articles', 'news')
    else:
        rubrics = (rubric_url, )
    count_art_per_date = 0
    for rubric in rubrics:
        print('circle', rubric)
        all_raw_art = bs.find_all("div", class_=ART_TAGS[rubric])
        print(ART_TAGS[rubric], all_raw_art)
        count_art_per_date += len(all_raw_art)
        if dat_key in all_art.keys():
            if count_art_per_date == len(all_art[dat_key]):
                print(ART_ADD_BEFORE)
        for raw_art in all_raw_art:
            date = raw_art.find("span", class_='g-date item__date').get_text()
            title_art = raw_art.find("div", class_="titles").find('a')
            art = Art(
                rubric = rubric,
                title = title_art.get_text(),
                link = title_art.get('href'),
                date = datetime.strptime(to_format_date(date, date_url), '%H:%M %d %m %Y')
            )
            print('added art')
            if dat_key not in all_art.keys():
                all_art[dat_key] = [art, ]
            else:
                if art not in all_art[dat_key]:
                    all_art[dat_key].append(art)
    all_art[dat_key].sort(key=lambda element: element.date)

def main():
    global all_art
    path_file = namespace.file[1:-1]
    rubric_url = namespace.rubric if namespace.rubric else 'all'
    print('in main', rubric_url)
    if os.path.exists('/'.join(path_file.split('/')[:-1])):
        try:
            with open(path_file, 'rb') as art_pkl:
                all_art = pickle.load(art_pkl)
        except: pass
    else:
        print(WRONG_DIRECTORY)
        return

    if namespace.date:
        date_url = '/'.join(namespace.date.split('.'))
        date_key = datetime.strptime(namespace.date, '%Y.%m.%d').date()
        print(date_key)
        get_art_attrs(rubric_url, date_url, date_key)
    else:
        date_url = datetime.strftime(datetime.today(), '%Y/%m/')
        print(date_url)
        for date_month in range(1, int(datetime.today().day)+1):
            date_month_str = f'{"0" if date_month < 10 else ""}{str(date_month)}'
            date_key = datetime.strptime(date_url + date_month_str, '%Y/%m/%d').date()
            print('in date_month', date_key)
            get_art_attrs(rubric_url, date_url + date_month_str, date_key)

    with open(path_file, 'wb') as art_pkl:
        pickle.dump(all_art, art_pkl)

    return True


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    all_art = {}
    if main():
        print(SUCCESS)
