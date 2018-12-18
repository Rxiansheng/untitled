import requests

url = 'https://v7.wuso.tv/wp-content/uploads/2018/03/asdysb0320007.mp4'

headers = {'Referer': 'https://wuso.me/',
           'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}

req = requests.get(url, headers=headers, stream=True, )
print(req.headers)
