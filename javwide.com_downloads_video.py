'''
javwide.com 无码爬虫 需要requests，lxml酷
'''


import requests, os, sys, datetime
from lxml import etree
from contextlib import closing


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


def down_file(url, file_name, file_date):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Macintosh; Intel Mac OS X 10.14; rv: 63.0) Gecko / 20100101 Firefox / 63.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': url,
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    }
    date = {
        'r': '',
        'd': 'www.embed.media'
    }
    while True:
        try:
            text = r.post('https://www.embed.media/api/source/'+url.split('/')[-1], headers=headers, data=date)
            #print(text.json()['data'])
            if text.status_code == 404:
                break
            else:
                for i in reversed(text.json()['data']):
                    if '720p' in i['label']:
                        file_url = r.get('https://www.embed.media'+i['file'], allow_redirects=False).headers['location']
                        with closing(r.get(file_url, stream=True, headers=headers)) as response:
                            chunk_size = 1024  # 单次请求最大值
                            content_size = int(response.headers['content-length'])  # 内容体总大小
                            progress = ProgressBar(file_name + '.' + i['type'], total=content_size,
                                                   unit="KB", chunk_size=chunk_size, run_status="正在下载",
                                                   fin_status="下载完成")
                            with open('/vod/javwide' + file_date + '/' + file_name + '.' + i['type'], "wb") as file:
                                for data in response.iter_content(chunk_size=chunk_size):
                                    file.write(data)
                                    progress.refresh(count=len(data))
                        break
        except BaseException as e:
            print(e)

def dwon_page(url):
    text = r.get(url)
    text = etree.HTML(text.text).xpath('//*[@id="redirector"]/@data-key')[0]
    return text



def mian():
    for i in range(1,2):
        text = r.get('https://www.javwide.com/category/uncensored/'+str(i))
        #print(text.text)
        text = etree.HTML(text.text)
        url = text.xpath('//*[@class="row"]/div/div/div/h3/a/@href')
        for k in url:
            text = r.get(k)
            file_url = etree.HTML(text.text).xpath('//*[@class="embed-responsive-item"]/@src')[0]
            file_name = etree.HTML(text.text).xpath('//*[@class="wrap-meta"]/h2/text()')[0]
            #print(file_name)
            file_date = str(datetime.datetime.today())
            #print(file_date)
            url = dwon_page(file_url)
            down_file(url, file_name, file_date)



if __name__ == "__main__":
    r = requests.session()
    mian()