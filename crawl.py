import http.client
import time
from bs4 import BeautifulSoup

def get_response_data(host, path):
    print('http request to "%s%s"...' % (host, path))
    conn = http.client.HTTPSConnection(host)
    conn.connect()
    conn.request('GET', path)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    print('http response from "%s%s"!' % (host, path))
    return data

def has_class(element, class_name):
    if 'class' in element.attrs and class_name in element['class']:
        return True
    return False



HOST = 'www.acmicpc.net'
GROUP_ID = '543'
GROUP_MEMBER_PATH = '/group/member/%s' % GROUP_ID

# get member list(HTML)
member_html = get_response_data(HOST, GROUP_MEMBER_PATH)

# parse member list(HTML)
print ('member list(HTML) parse...')
sccc_member = {}
soup = BeautifulSoup(member_html, 'html.parser')
for div in soup.find_all('div'):
    if has_class(div, 'member'):
        sccc_member[div.a.string] = div.a['href']
print ('member list(HTML) parse DONE!')

# get solved problem list by member
solved_problems = {}
for member, link in sccc_member.items():
    user_html = get_response_data(HOST, link)

    # parse solved problem list by user(HTML)
    print ('user %s(HTML) parse...' % member)
    cnt = 0
    panel_cnt = 0
    soup = BeautifulSoup(user_html, 'html.parser')
    for div in soup.find_all('div'):
        if has_class(div, 'panel-body'):
            panel_cnt = panel_cnt + 1
            for span in div.find_all('span'):
                if has_class(span, 'problem_number'):
                    cnt = cnt + 1
                    if not span.a['href'] in solved_problems:
                        # initialize new problem
                        solved_problems[span.a['href']] = {
                            'solved_cnt': 0,
                            'failed_cnt': 0
                        }
                    key = span.a['href']
                    solved_problems[key]['number']=span.a.string
                    # if panel_cnt is 1, solved
                    if panel_cnt == 1:
                        solved_problems[key]['solved_cnt'] = \
                            solved_problems[key]['solved_cnt'] + 1
                    # else, failed
                    else:
                        solved_problems[key]['failed_cnt'] = \
                            solved_problems[key]['failed_cnt'] + 1
                elif has_class(span, 'problem_title'):
                    solved_problems[span.a['href']]['title']=span.a.string
    print ('user %s(HTML) parse DONE! (%d)' % (member, cnt))
    time.sleep(1)

file = open('solved_list', 'w')
file.write(str(solved_problems))
file.close()