import ast
import argparse
from operator import itemgetter

HOST = 'www.acmicpc.net'
GROUP_MEMBER_CNT = 43

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
parser.add_argument('-spa', help="sort by solved per all")
parser.add_argument('-spc', help="sort by solved per challenger [default]")
parser.add_argument('-cpa', help="sort by challenger per all")
parser.add_argument('-d', help="sort by descending order [default]")
parser.add_argument('-a', help="sort by ascending order")
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
for info in sorted_list:
    print('%2d %2d %6.2f %6.2f %6.2f [%5s - %s]' % (
        info['solved_cnt'], info['failed_cnt'],
        info['solved_per_challenger'],
        info['solved_per_all'],
        info['challenger_per_all'],
        info['number'], info['title']
        )
    )
