import time
import requests

def Main():
    f = open('z:/symbols.txt', 'rt')
    s = f.read()
    f.close()
    
    defaultHeaders = {
        'User-Agent' : 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    url = 'https://finance.vietstock.vn/AAA/phan-tich-ky-thuat.htm'
    resp = requests.get(url, headers = defaultHeaders)
    cookies = resp.cookies
    
    rootPath = 'D:/Tmp/vietstock_prices/'
    
    symbols = s.split('\n')
    for symbol in symbols:
        print(symbol)

        url = 'https://api.vietstock.vn/ta/history?symbol='
        url += symbol
        url += '&resolution=W&from=1420074000&to=1657722336'
        
        resp = requests.get(url, headers = defaultHeaders, cookies = cookies)
        
        f = rootPath + symbol
        f = open(f, 'wb')
        f.write(resp.content)
        f.close()
    
        time.sleep(1)
        #break

    pass

Main()
