import requests

url = 'https://www1.hkexnews.hk/listedco/listconews/sehk/2015/0429/ltn20150429713.pdf'

response = requests.get(url, stream= True)
filename = url.split('/')
name = filename[len(filename)-1]
with open(name, 'wb') as f:
    for chunk in response.iter_content(chunk_size=32):
        f.write(chunk)