import os
import json
import csv
import html2text
import datetime

def LoadPricesList(rootDir):
    result = {}
    names = os.listdir(rootDir)
    for name in names:
        filename = rootDir + '/' + name
        f = open(filename, 'rb')
        s = f.read()
        f.close()
        s = s.decode('utf-8')
        
        x = json.loads(s)
        x = json.loads(x)

        ar_t = x['t']
        ar_c = x['c']
        
        items = []
        n = len(ar_t)
        i = 0
        while i < n:
            items.append([ar_t[i], ar_c[i]])
            i = i + 1
        
        symbol = name.upper()
        result[symbol] = items
    
    return result

def ParseSymbolInfo(rootDir):
    result = {}
    
    signal1 = '<span class=text>Ng&#224;nh: </span>'
    signal2 = '</div><div class=m-b-xs><small class=p-r-xs>'

    signal1 = signal1.lower()
    signal2 = signal2.lower()
    signal1Len = len(signal1)
    
    names = os.listdir(rootDir)
    for name in names:
        filename = rootDir + '/' + name
        f = open(filename, 'rb')
        s = f.read()
        f.close()
        html = s.decode('utf-8')
        
        symbol = name.upper()
        pos = symbol.rfind('.HTML')
        if pos >= 0:
            symbol = symbol[0:pos]
        
        pos = html.lower().find(signal1)
        if pos < 0:
            continue
        
        s = html[pos+signal1Len:]
        pos = s.lower().find(signal2)
        if pos < 0:
            continue
        
        items = []
        
        s = s[0:pos]
        data = s
        while True:
            pos = s.find(' href=/')
            if pos < 0:
                break
        
            s = s[pos+7:]
            pos = s.find('>')
            if pos < 0:
                break
            
            url = s[0:pos]
            s = s[pos+1:]

            pos = s.find('</')
            if pos < 0:
                break

            rawText = s[0:pos]
            s = s[pos+1:]
            
            text = html2text.html2text(rawText)
            text = text.strip()
            
            typeID = '?'
            pos = url.find('-')
            if pos >= 0:
                typeID = url[0:pos].lower()
            
            items.append([typeID, url, text])

        result[symbol] = items

    return result

def LoadExchangesInfo(filename):
    result = {}

    f = open(filename, 'rt')
    s = f.read()
    f.close()
    
    rows = s.split('\n')
    for row in rows:
        cells = row.split('\t')
        symbol = cells[0].upper()
        exchange = cells[1].upper()
        result[symbol] = exchange

    return result

def PrepareDic3(dic2):
    result = {}
    for symbol in dic2:
        items = dic2[symbol]
        for item in items:
            typeID = item[0]
            if typeID not in result:
                result[typeID] = item[2]
    
    return result

def Main():
    print('Load Dic1')
    dic1 = LoadPricesList('d:/Tmp/vietstock_prices')

    print('Load Dic2')
    dic2 = ParseSymbolInfo('d:/Tmp/vietstock_info')
    
    print('Load Exchanges Info')
    dic3 = LoadExchangesInfo('d:/Tmp/vn_exchange_info.txt')
    
    print('Export data')
    print()
    
    filename = 'd:/Tmp/vietstock_db.csv'
    f = open(filename, 'w', encoding = 'utf-8')
    writer = csv.writer(f)
    
    header = [
        'Symbol',
        'Exchange',
        'Business ID',
        'Business Name',
        'Timestamp',
        'DateTime',
        'Price'
    ]
    writer.writerow(header)
    
    for symbol in dic1:
        print(symbol)
        
        exchange = ''
        if symbol in dic3:
            exchange = dic3[symbol]
    
        items1 = dic1[symbol]
        items2 = []
        if symbol in dic2:
            items2 = dic2[symbol]

        businessID = ''
        businessName = ''

        n = len(items2)
        if n > 0:
            item = items2[0]
            businessID = item[0]
            businessName = item[2]
    
        for item in items1:
            timestamp = item[0]
            price = item[1]
            
            t = datetime.datetime.fromtimestamp(timestamp)
            t = datetime.datetime.strftime(t, '%Y-%m-%d')
            
            data = [symbol, exchange, businessID, businessName, timestamp, t, price]
            writer.writerow(data)
    
    f.close()
    
    print()
    print('Preprocess output file')
    
    f = open(filename, 'rt', encoding = 'utf-8')
    s = f.read()
    f.close()
    
    f = open(filename, 'wt', encoding = 'utf-8')
    rows = s.split('\n')
    for row in rows:
        row = row.strip()
        n = len(row)
        if n <= 0:
            continue
        
        s = row + '\n'
        f.write(s)
        
    f.close()
    
    pass

Main()
