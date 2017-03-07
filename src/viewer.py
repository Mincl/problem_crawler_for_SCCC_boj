import http.client
import ast
import argparse
from operator import itemgetter
from bs4 import BeautifulSoup

def get_response_data(host, path):
    conn = http.client.HTTPSConnection(host)
    conn.connect()
    conn.request('GET', path)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def has_class(element, class_name):
    if 'class' in element.attrs and class_name in element['class']:
        return True
    return False


HOST = 'www.acmicpc.net'
GROUP_MEMBER_CNT = 43
USER_PATH = '/user/%s'

file = open('solved_list', 'r')
solved_list_str = file.read()
file.close()

solved_list = ast.literal_eval(solved_list_str)
# key - link
# value
## 'number': problem number
## 'title': problem title
## 'solved_cnt': count of people who solved the problem
## 'failed_cnt': count of people who failed to solve the problem

# rebuilding problem info
rebuild_list = []
for link, val in solved_list.items():
    info = {}
    info['number'] = val['number']
    info['title'] = val['title']
    info['solved_cnt'] = val['solved_cnt']
    info['failed_cnt'] = val['failed_cnt']
    info['link'] = '%s%s' % (HOST, link)
    info['solved_per_all'] = info['solved_cnt'] * 100.0 / GROUP_MEMBER_CNT
    info['solved_per_challenger'] = \
        info['solved_cnt'] * 100.0 / (info['solved_cnt']+info['failed_cnt'])
    info['challenger_per_all'] = \
        (info['solved_cnt']+info['failed_cnt']) * 100.0 / GROUP_MEMBER_CNT
    rebuild_list.append(info)

parser = argparse.ArgumentParser()
parser.add_argument('-spa', help="sort by solved per all", action="store_true")
parser.add_argument('-spc', help="sort by solved per challenger [default]", action="store_true")
parser.add_argument('-cpa', help="sort by challenger per all", action="store_true")
parser.add_argument('-d', help="sort by descending order [default]", action="store_true")
parser.add_argument('-a', help="sort by ascending order", action="store_true")
parser.add_argument('-u', help="grep specific user's unsolved problem list")
args = parser.parse_args()

column = 'solved_per_challenger'
if args.spa:
    column = 'solved_per_all'
elif args.cpa:
    column = 'challenger_per_all'

order=True
if args.a:
    order=False

sorted_list = sorted(rebuild_list, key=itemgetter(column, 'solved_cnt'), reverse=order)

user_solved = []
if args.u:
    user_html = get_response_data(HOST, USER_PATH % args.u)
    soup = BeautifulSoup(user_html, 'html.parser')
    panel_cnt = 0
    for div in soup.find_all('div'):
        if has_class(div, 'panel-body'):
            panel_cnt = panel_cnt + 1
            for span in div.find_all('span'):
                if has_class(span, 'problem_number'):
                    number=span.a.string
                    if panel_cnt == 1:
                        user_solved.append(number)
for info in sorted_list:
    if not info['number'] in user_solved:
        print('%2d %2d %6.2f %6.2f %6.2f [%5s - %s]' % (
            info['solved_cnt'], info['failed_cnt'],
            info['solved_per_challenger'],
            info['solved_per_all'],
            info['challenger_per_all'],
            info['number'], info['title']
            )
        )
