import getopt
import sys

import requests
from lxml import etree


def login_yam(accout, passwd):
    text = r.get('https://member.yam.com/Account/Login/?URL=https://s.yam.com')
    text = etree.HTML(text.text)
    VIEWSTATE = text.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
    EVENTVALIDATION = text.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
    VIEWSTATEGENERATOR = text.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]

    data = {
        '__EVENTARGUMENT': None,
        '__EVENTTARGET': None,
        '__EVENTVALIDATION': EVENTVALIDATION,
        '__LASTFOCUS': None,
        '__VIEWSTATE': VIEWSTATE,
        '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
        'MEMBER_ID': accout,
        'MEMBER_PWD': passwd,
        'UrlReferrer': 'https://s.yam.com',
        'yamMemberFormSubmit': '立即登入'
    }
    headers = {
        'User-Agent:': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'
    }

    text = r.post('https://member.yam.com/Account/Login/default.aspx?URL=https://s.yam.com', data, headers)
    text = etree.HTML(text.text).xpath('//*[@class="nav-nick dropdown-toggle"]/text()')[0]
    if text == accout:
        print('登录成功')
    else:
        print('登录失败，请检查账号密码')


def main(argv):
    domain = ''
    token = ''
    while_num = ''
    try:
        opts, args = getopt.getopt(argv, "hu:p:r:s",
                                   ["user=", "passwd=", "read=", "save="])  # 获取脚本输入的文件保存路径，youfile账号密码
    except getopt.GetoptError:
        print('test.py -u <账号> -p <密码>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -u <账号> -p <密码>')
            sys.exit()
        elif opt in ("-u", "--user"):  # 判断并获取文件保存路径
            user = arg
        elif opt in ("-p", "--passwd"):  # 判断并获取youfile账号
            passwd = arg
        elif opt in ("-r", "--read"):  # 判断并获取youfile账号
            read = arg
        elif opt in ("-s", "--save"):  # 判断并获取youfile账号
            save = arg
    login_yam(user, passwd)
    with open(str(read) + '.txt', 'rt') as f:
        data = f.readlines()
    for i in data:
        data = {
            'url': i
        }
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent:': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'
        }
        text = r.post('https://s.yam.com/a/GetShort/', data, headers)
        if text.json()['code'] == 200:
            print('获取{0}短网址成功,短网址: https://s.yam.com/{1}'.format(i, text.json()['YSID']))
            with open(str(save) + '.txt', 'a') as f:
                f.writelines('https://s.yam.com/' + text.json()['YSID'] + '\r\n')


if __name__ == "__main__":
    r = requests.session()
    main(sys.argv[1:])
