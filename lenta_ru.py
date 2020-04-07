import sys
import os
import re
from random import choice
import pickle
import argparse
from calendar import Calendar
from datetime import datetime
from typing import NamedTuple

import requests
from bs4 import BeautifulSoup as Bs

from additional_const import *


# Most important constants
MAIN_URL = 'https://lenta.ru'
USERAGENT = {'User-agent': choice(USERAGENTS)}
ART_TAGS = {
    'news': 'item news b-tabloid__topic_news',
    'articles': 'item article'
}


class Art(NamedTuple):
    """ Contains all attributes of articles
    """
    rubric : str
    title : str
    link : str
    date : datetime
    text : str

    def __str__(self):
        return ('Новость: ' if self.rubric == 'news' else 'Статья: ')+\
               self.title+datetime.strftime(self.date, ' %d.%m.%Y')


def connected(url):
    req = requests.get(url, headers=USERAGENT)
    bs = Bs(req.text, "html.parser")

    return bs

	
# For processing parametrs
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
            format_date = ' '.join(date_spl[:-2] + 
                                   [MONTHS[date_spl[-2]]] + [date_spl[-1]])
        else:
            format_date = ' '.join(date_spl[:-1] + [MONTHS[date_spl[-1]]] +
                                   [str(datetime.today().year)])

    return format_date

	
# Return raw text of article, without pictures, special texts and titles
def get_art_text(full_url_art):
    all_raw_text = connected(full_url_art).find_all("p")
    text_art = ''
    for raw_art_text in all_raw_text:
        text_art += re.sub('\n', '', raw_art_text.get_text())+'\n'
    return text_art

	
# Parse attributes of article by parametrs
def get_art_attrs(rubric_url, date_url, dat_key):
    global all_art
    if rubric_url == 'all':
        rubrics = ('articles', 'news')
    else:
        rubrics = (rubric_url, )
		
    for rubric in rubrics:
        count_art_per_date = 0
        extense_url = f'{MAIN_URL}/{rubric}/{date_url}'
        all_raw_art = connected(extense_url)
                      .find_all("div", class_=ART_TAGS[rubric])
        count_art_per_date += len(all_raw_art)
		
        # Check for existing the date in dictionary
        if dat_key in all_art.keys():
            # If you didn't write date, programm will return articles
			# without text of article. Then, if you check
            # for articles for existing date, you will get completely 
            # new list of articles by rubric with text for the date
            if namespace.date and choice(all_art[dat_key]).text == '':
                all_art[dat_key].clear()
                print(ART_DELETE_FOR_TEXT)
            # If you have all articles by rubric, function return
            if count_art_per_date == len(all_art[dat_key]):
                print(ART_ADD_BEFORE_ALL)
                return
				
        for raw_art in all_raw_art:
            date = raw_art.find("span", class_='g-date item__date')
                                .get_text()
            title_art = raw_art.find("div", class_="titles").find('a')
            url_art = title_art.get('href')
            text_art = get_art_text(MAIN_URL+url_art) if namespace.date else ''
            art = Art(
                rubric=rubric,
                title=title_art.get_text(),
                link=url_art,
                date=datetime.strptime(to_format_date(date, date_url),
                                       '%H:%M %d %m %Y'),
                text=text_art				
            )
            if dat_key not in all_art.keys():
                all_art[dat_key] = [art, ]
            else:
                # Check art for existing in dictionary
                if art not in all_art[dat_key]:
                    all_art[dat_key].append(art)
                else:
                    print(ART_ADD_BEFORE)
    all_art[dat_key].sort(key=lambda element: element.date)


def main():
    global all_art
    path_file = namespace.file[1:-1]
    # If parametr of rubric is not given,
	# programm processing both rubrics
    rubric_url = namespace.rubric if namespace.rubric else 'all'

    if os.path.exists('/'.join(path_file.split('/')[:-1])):
        try:
            with open(path_file, 'rb') as art_pkl:
                all_art = pickle.load(art_pkl)
        except: pass
    else:
        print(WRONG_DIRECTORY)
        return
		
    # If parametr of date is not given, programm will process
	# every past day of current month
    if namespace.date:
        date_url = re.sub('.', '/', namespace.date)
        date_key = datetime.strptime(namespace.date, '%Y.%m.%d').date()
        get_art_attrs(rubric_url, date_url, date_key)
    else:
        date_url = datetime.strftime(datetime.today(), '%Y/%m/')
        for date_month in range(1, int(datetime.today().day)+1):
            date_month_str = f'{"0" if date_month < 10 else ""}'\
                              '{str(date_month)}'
            date_key = datetime.strptime(date_url + date_month_str,
                                         '%Y/%m/%d').date()
            get_art_attrs(rubric_url, date_url + date_month_str, date_key)
			
    # If everything is okay, the dictionary dumps into storage
    with open(path_file, 'wb') as art_pkl:
        pickle.dump(all_art, art_pkl)

    return True


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    all_art = {}
    if main():
        print(SUCCESS)