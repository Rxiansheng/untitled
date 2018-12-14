import getopt
import os
import sys
from contextlib import closing

import requests
from lxml import etree


class ProgressBar(object):

    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "【%s】%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)


def login_youfile(accout, passwd):  # 登陆youfile网盘
    data = {
        'action': 'validateLogin',
        'ans': None,
        'LoginButton': '登录',
        'module': 'member',
        'password': str(passwd),
        'que': '0',
        'remember': 'on',
        'returnPath': 'http://page5.dfpan.com/fs/1l4i4f4e0d6r1e3am3/',
        'username': str(accout)
    }
    headers = {
        'User-Agent': 'Mozilla / 5.0(Macintosh; Intel Mac OS X 10.14; rv: 63.0) Gecko / 20100101 Firefox / 63.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://page5.dfpan.com/fs/1l4i4f4e0d6r1e3am3/',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    }
    text = r.post('http://www.yunfile.com/view', data=data, headers=headers)
    text = etree.HTML(text.text).xpath('//*[@class="safety_code_text"]/text()')
    if text:
        return text[0]

def down_file(url_orgin, file_name, vodie_date):  # 下载文件并打印进度条
    make_path(str(vodie_date))
    if os.path.isfile(str(vodie_date) + '/' + str(file_name) + '.rar'):  # 判断文件是否存在
        print('{0}已经存在，跳过下来'.format(file_name))
    else:
        headers = {
            'User-Agent': 'Mozilla / 5.0(Macintosh; Intel Mac OS X 10.14; rv: 63.0) Gecko / 20100101 Firefox / 63.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': url_orgin,
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
        }
        while True:
            try:
                text = r.get(url_orgin, headers=headers)
                # print(text.url)
                # print(text.text)
                if text.status_code == 404:
                    break
                else:
                    text = etree.HTML(text.text)

                    url = text.xpath('//*[@class="down_url_table_td_table"]/tr/td/a/@href')
                    headers = {
                        'User-Agent': 'Mozilla / 5.0(Macintosh; Intel Mac OS X 10.14; rv: 63.0) Gecko / 20100101 Firefox / 63.0',
                        'Referer': url_orgin,
                        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
                    }
                    if url:
                        for i in reversed(url):
                            try:
                                with closing(r.get(i, stream=True, headers=headers)) as response:
                                    if response.headers['content-length']:
                                        chunk_size = 1024  # 单次请求最大值
                                        content_size = int(response.headers['content-length'])  # 内容体总大小
                                        progress = ProgressBar(file_name, total=content_size,
                                                               unit="KB", chunk_size=chunk_size, run_status="正在下载",
                                                               fin_status="下载完成")
                                        with open(str(vodie_date) + '/' + str(file_name) + '.rar', "wb") as file:
                                            for data in response.iter_content(chunk_size=chunk_size):
                                                file.write(data)
                                                progress.refresh(count=len(data))
                                break
                            except BaseException as e:
                                print('下载地址失效，换地址下载')

                        break
            except BaseException as e:
                print(e)




def make_path(p):
    if os.path.exists(p):  # 判断文件夹是否存在
        pass
    else:
        os.mkdir(p)  # 创建文件夹


def main(argv):  # 获取脚本输入参数
    with open('page_num.txt', 'rt') as f:
        page_num = f.read()
        if page_num:
            page_num = int(page_num)
        else:
            page_num = 1
    file = ''
    accout = ''
    passwd = ''
    try:
        opts, args = getopt.getopt(argv, "h:i:a:p:", ["ifile=", "accout=", "passwd="])  # 获取脚本输入的文件保存路径，youfile账号密码
    except getopt.GetoptError:
        print('test.py -i <下载文件位置> -a <云盘账号> -p <云盘密码>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <下载文件位置> -a <云盘账号> -p <云盘密码>')
            sys.exit()
        elif opt in ("-i", "--ifile"):  #判断并获取文件保存路径
            file = arg
        elif opt in ("-a", "--accout"):  #判断并获取youfile账号
            accout = arg
        elif opt in ("-p", "--passwd"):  #判断并获取youfile密码
            passwd = arg
    login_status = login_youfile(accout, passwd)
    if login_status == '安全码':
        print('请手动解封账号')
        sys.exit(2)
    else:
        print('登录成功...准备开始采集')
    for i in range(page_num, 809):
        # print(type)
        text = r.get('http://922tp.com/page/' + str(i))  #获取922tp下载链接
        text = etree.HTML(text.text)
        for find_name in range(1, 6):
            vodie_name = text.xpath('//*[@id="blog"]/div[' + str(find_name) + ']/h2/a/text()')[0].split('[')[0].replace(
                '/', '')  #获取下载标题名
            vodie_date = text.xpath('//*[@id="blog"]/div[' + str(find_name) + ']/div[1]/span[1]/text()')[0].split(':')[
                -1].strip()  # 获取下载文件日期
            url = text.xpath('//*[@id="blog"]/div[' + str(find_name) + ']/div/p/a/@href')  # 获取youfile链接
            for find_jgp in url:  # 判断是否为youfile下载链接和图片
                if '.jpg' in find_jgp:
                    pass
                elif '.jpg' in find_jgp:
                    pass
                elif '.png' in find_jgp:
                    pass
                elif '.png' in find_jgp:
                    pass
                elif '.jpeg' in find_jgp:
                    pass
                elif '.jpeg' in find_jgp:
                    pass
                elif 'putpan.com' in find_jgp:
                    url = r.get(find_jgp, allow_redirects=False).headers['location']
                    down_file(url, vodie_name, file + vodie_date)
                    break
                elif 'pwpan.com' in find_jgp:
                    url = r.get(find_jgp, allow_redirects=False).headers['location']
                    down_file(url, vodie_name, file + vodie_date)
                    break
                elif 'tadown.com' in find_jgp:
                    url = r.get(find_jgp, allow_redirects=False).headers['location']
                    down_file(url, vodie_name, file + vodie_date)
                    break
        with open('page_num.txt', 'wt') as f:
            f.write(str(i))

if __name__ == "__main__":
    r = requests.session()
    main(sys.argv[1:])
