import time
import requests

def Main():
    f = open('z:/symbols.txt', 'rt')
    s = f.read()
    f.close()
    
    defaultHeaders = {
        'User-Agent' : 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    rootPath = 'D:/Tmp/vietstock_info/'
    
    symbols = s.split('\n')
    for symbol in symbols:
        print(symbol)

        url = 'https://finance.vietstock.vn/'
        url += symbol
        url += '-cong-ty.htm'
        
        resp = requests.get(url, headers = defaultHeaders)
        
        f = rootPath + symbol + '.html'
        f = open(f, 'wb')
        f.write(resp.content)
        f.close()
    
        time.sleep(1)
        #break

    pass

Main()
