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


def login_youfile(url_orgin, file_name, vodie_date, accout, passwd):
    data ={
        'action': 'validateLogin',
        'ans': None,
        'LoginButton': '登录',
        'module': 'member',
        'password': str(passwd),
        'que': '0',
        'remember': 'on',
        'returnPath': url_orgin,
        'username': str(accout)
    }
    headers = {
        'User-Agent': 'Mozilla / 5.0(Macintosh; Intel Mac OS X 10.14; rv: 63.0) Gecko / 20100101 Firefox / 63.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://page5.dfpan.com/fs/1l4i4f4e0d6r1e3am3/',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    }
    text = r.post('http://www.yunfile.com/view', data=data,headers=headers)
    text = etree.HTML(text.text)
    url = text.xpath('//*[@class="down_url_table_td_table"]/tr/td/a/@href')
    headers = {
        'User-Agent': 'Mozilla / 5.0(Macintosh; Intel Mac OS X 10.14; rv: 63.0) Gecko / 20100101 Firefox / 63.0',
        'Referer': url_orgin,
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    }
    make_path(str(vodie_date))
    if os.path.isfile(str(vodie_date) + '/' + str(file_name) + '.rar'):  # 判断文件是否存在
        pass
    else:
        with closing(r.get(url[-1], stream=True, headers=headers)) as response:
            chunk_size = 1024  # 单次请求最大值
            content_size = int(response.headers['content-length'])  # 内容体总大小
            progress = ProgressBar(file_name, total=content_size,
                                   unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
            with open(str(vodie_date) + '/' + str(file_name) + '.rar', "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(count=len(data))


def make_path(p):
    if os.path.exists(p):  # 判断文件夹是否存在
        pass
    else:
        os.mkdir(p)  # 创建文件夹


def main(argv):
    file = ''
    accout = ''
    passwd = ''
    try:
        opts, args = getopt.getopt(argv, "h:i:a:p:", ["ifile=", "accout=", "passwd="])
    except getopt.GetoptError:
        print('test.py -i <下载文件位置> -a <云盘账号> -p <云盘密码>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <下载文件位置> -a <云盘账号> -p <云盘密码>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            file = arg
        elif opt in ("-a", "--accout"):
            accout = arg
        elif opt in ("-p", "--passwd"):
            passwd = arg
    for i in range(1, 809):
        text = r.get('http://922tp.com/page/' + str(i))
        text = etree.HTML(text.text)
        for find_name in range(1, 6):
            vodie_name = text.xpath('//*[@id="blog"]/div[' + str(find_name) + ']/h2/a/text()')[0].split('[')[0]
            vodie_date = text.xpath('//*[@id="blog"]/div[' + str(find_name) + ']/div[1]/span[1]/text()')[0].split(':')[
                -1].strip()
            url = text.xpath('//*[@id="blog"]/div[' + str(find_name) + ']/div/p/a/@href')
            for find_jgp in url:
                if '.JPG' in find_jgp:
                    pass
                elif '.jpg' in find_jgp:
                    pass
                elif '.png' in find_jgp:
                    pass
                elif '.PNG' in find_jgp:
                    pass
                elif '.jpeg' in find_jgp:
                    pass
                elif '.JPEG' in find_jgp:
                    pass
                elif 'putpan.com' in find_jgp:
                    url = r.get(find_jgp, allow_redirects=False).headers['location']
                    login_youfile(url, vodie_name, file + vodie_date, accout, passwd)
                    break
                elif 'pwpan.com' in find_jgp:
                    url = r.get(find_jgp, allow_redirects=False).headers['location']
                    login_youfile(url, vodie_name, file + vodie_date, accout, passwd)
                    break
                elif 'tadown.com' in find_jgp:
                    url = r.get(find_jgp, allow_redirects=False).headers['location']
                    login_youfile(url, vodie_name, file + vodie_date, accout, passwd)
                    break


if __name__ == "__main__":
    r = requests.session()
    main(sys.argv[1:])
