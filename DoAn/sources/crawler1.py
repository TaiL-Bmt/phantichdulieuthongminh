#Crawler
#Lấy lịch sử lãi suất ngân hàng từ trang "vneconomy.vn"

import sys
import json
import requests
import time
import decimal
from datetime import datetime
from bs4 import BeautifulSoup


dicVnBank = {}


def ParseTimeTZ(s):
    ar1 = s.split('T')
    n = len(ar1)
    if n < 2:
        return None
    
    ar2 = ar1[1].split('Z')
    ar2 = ar2[0].split('.')
    
    s2 = ar1[0] + ' ' + ar2[0]
    result = datetime.strptime(s2, '%Y-%m-%d %H:%M:%S')
    
    return result

def Html2Text(html):
    engine = BeautifulSoup(html, 'html.parser')
    txt = engine.get_text()
    return txt

def SearchNext(pageNum):
    results = []

    url = 'https://search.hemera.com.vn/search/1/L%C3%A3i%20su%E1%BA%A5t%20ti%E1%BA%BFt%20ki%E1%BB%87m/'
    url += str(pageNum)
    r = requests.get(url)
    items = r.json()
    for item in items:
        try:
            url = item['UrlArticle']
            publishedDate = item['PublishedDate']
            jsonTags = item['JsonTag']
            title = item['Title']
            
            title = Html2Text(title).lower()
            jsonTags = json.loads(jsonTags)
            
            tag1OK = False
            tag2OK = False
            tag3OK = False
            
            cmpMode = 2
            if 1 == cmpMode:
                for jsonTag in jsonTags:
                    tagName = jsonTag['Name'].lower()
                    pos = tagName.find('lãi suất')
                    if pos >= 0:
                        tag1OK = True
                    pos = tagName.find('tiết kiệm')
                    if pos >= 0:
                        tag2OK = True
                    pos = tagName.find('ngân hàng')
                    if pos >= 0:
                        tag3OK = True
            elif 2 == cmpMode:
                tag1OK = True
                pos = title.find('lãi suất')
                if pos >= 0:
                    tag2OK = True
                    pos2 = title.find('tiết kiệm')
                    if pos2 > pos:
                        tag3OK = True
            

            tagNameOK = tag1OK and tag2OK and tag3OK
            if not tagNameOK:
                continue
            
            url = 'https://vneconomy.vn/' + url
            publishedDate = ParseTimeTZ(publishedDate)
            
            newItem = {}
            newItem['publishedDate'] = publishedDate
            newItem['url'] = url
            results.append(newItem)
        except:
            pass
    
    return results

def DownloadAndExtractProfitInfo(results, publishedDate, url):
    global dicVnBank

    print(url)

    r = requests.get(url)
    html = r.content.decode('utf-8')
    txt = Html2Text(html)
    
    txt = txt.lower()
    txt = txt.replace('m.', 'm ')
    txt = txt.replace('m,', 'm ')
    txt = txt.replace('m;', 'm ')
    txt = txt.replace('m)', 'm ')
    txt = txt.replace('m…', 'm ')
    
    ar1 = txt.split('năm ')
    for s1 in ar1:
        s1 = s1.strip()
        l = len(s1)
        if '/' != s1[l - 1]:
            continue
        
        s1 = s1[0:l-1].strip()
        l = len(s1)
        if '%' != s1[l - 1]:
            continue

        s1 = s1[0:l-1].strip()
        
        pos = s1.rfind(' ')
        if pos < 0:
            continue

        s2 = s1[pos+1:]
        s1 = s1[0:pos]
        
        s2 = s2.replace('(', ' ')
        s2 = s2.replace('.', '')
        s2 = s2.replace(',', '.')
        s2 = s2.strip()
        
        interest = None
        try:
            #interest = decimal.Decimal(s2)
            interest = float(s2)
        except:
            interest = None
        if interest is None:
            break

        foundBankName = None
        s3 = s1
        for bankName in dicVnBank:
            pos = s3.rfind(bankName)
            if pos >= 0:
                foundBankName = dicVnBank[bankName]
                found = True
                s3 = s3[0:pos]
                break
        
        if foundBankName is None:
            continue
        
        newItem = {}
        newItem['date'] = publishedDate
        newItem['bankName'] = foundBankName
        newItem['interest'] = interest
        results.append(newItem)
        print(str(newItem))

def PrepareBankList():
    global dicVnBank
    dicVnBank['bidv'] = 'BIDV'
    dicVnBank['đầu tư và phát triển việt nam'] = 'BIDV'
    dicVnBank['vietinbank'] = 'VietinBank'
    dicVnBank['công thương việt nam'] = 'VietinBank'
    dicVnBank['vietcombank'] = 'Vietcombank'
    dicVnBank['ngoại thương việt nam'] = 'Vietcombank'
    dicVnBank['vpbank'] = 'VPBank'
    dicVnBank['việt nam thịnh vượng'] = 'VPBank'
    dicVnBank['mb'] = 'MB'
    dicVnBank['quân đội'] = 'MB'
    dicVnBank['techcombank'] = 'Techcombank'
    dicVnBank['kỹ thương'] = 'Techcombank'
    dicVnBank['agribank'] = 'Agribank'
    dicVnBank['nn&pt nông thôn việt nam'] = 'Agribank'
    dicVnBank['acb'] = 'ACB'
    dicVnBank['á châu'] = 'ACB'
    dicVnBank['hdbank'] = 'HDBank'
    dicVnBank['phát triển thành phố hồ chí minh'] = 'HDBank'
    dicVnBank['shb'] = 'SHB'
    dicVnBank['sài gòn – hà nội'] = 'SHB'
    dicVnBank['sacombank'] = 'Sacombank'
    dicVnBank['sài gòn thương tín'] = 'Sacombank'
    dicVnBank['vbsp'] = 'VBSP'
    dicVnBank['chính sách xã hội việt nam'] = 'VBSP'
    dicVnBank['vib'] = 'VIB'
    dicVnBank['quốc tế'] = 'VIB'
    dicVnBank['msb'] = 'MSB'
    dicVnBank['hàng hải'] = 'MSB'
    dicVnBank['scb'] = 'SCB'
    dicVnBank['sài gòn'] = 'SCB'
    dicVnBank['vdb'] = 'VDB'
    dicVnBank['phát triển việt nam'] = 'VDB'
    dicVnBank['seabank'] = 'SeABank'
    dicVnBank['đông nam á'] = 'SeABank'
    dicVnBank['ocb'] = 'OCB'
    dicVnBank['phương đông'] = 'OCB'
    dicVnBank['eximbank'] = 'Eximbank'
    dicVnBank['xuất nhập khẩu'] = 'Eximbank'
    dicVnBank['lienvietpostbank'] = 'LienVietPostBank'
    dicVnBank['bưu điện liên việt'] = 'LienVietPostBank'
    dicVnBank['tpbank'] = 'TPBank'
    dicVnBank['tiên phong'] = 'TPBank'
    dicVnBank['pvcombank'] = 'PVcomBank'
    dicVnBank['đại chúng việt nam'] = 'PVcomBank'
    dicVnBank['woori'] = 'Woori'
    dicVnBank['woori việt nam'] = 'Woori'
    dicVnBank['bac a bank'] = 'Bac A Bank'
    dicVnBank['bắc á'] = 'Bac A Bank'
    dicVnBank['hsbc'] = 'HSBC'
    dicVnBank['hsbc việt nam'] = 'HSBC'
    dicVnBank['scbvl'] = 'SCBVL'
    dicVnBank['standard chartered việt nam'] = 'SCBVL'
    dicVnBank['pbvn'] = 'PBVN'
    dicVnBank['public bank việt nam'] = 'PBVN'
    dicVnBank['abbank'] = 'ABBANK'
    dicVnBank['an bình'] = 'ABBANK'
    dicVnBank['shbvn'] = 'SHBVN'
    dicVnBank['shinhan việt nam'] = 'SHBVN'
    dicVnBank['vietabank'] = 'VietABank'
    dicVnBank['việt á'] = 'VietABank'
    dicVnBank['donga bank'] = 'DongA Bank'
    dicVnBank['đông á'] = 'DongA Bank'
    dicVnBank['uob'] = 'UOB'
    dicVnBank['uob việt nam'] = 'UOB'
    dicVnBank['vietbank'] = 'Vietbank'
    dicVnBank['việt nam thương tín'] = 'Vietbank'
    dicVnBank['nam a bank'] = 'Nam A Bank'
    dicVnBank['nam á'] = 'Nam A Bank'
    dicVnBank['ncb'] = 'NCB'
    dicVnBank['quốc dân'] = 'NCB'
    dicVnBank['oceanbank'] = 'OceanBank'
    dicVnBank['đại dương'] = 'OceanBank'
    dicVnBank['cimb'] = 'CIMB'
    dicVnBank['cimb việt nam'] = 'CIMB'
    dicVnBank['viet capital bank'] = 'Viet Capital Bank'
    dicVnBank['bản việt'] = 'Viet Capital Bank'
    dicVnBank['kienlongbank'] = 'Kienlongbank'
    dicVnBank['kiên long'] = 'Kienlongbank'
    dicVnBank['ivb'] = 'IVB'
    dicVnBank['indovina'] = 'IVB'
    dicVnBank['baoviet bank'] = 'BAOVIET Bank'
    dicVnBank['bảo việt'] = 'BAOVIET Bank'
    dicVnBank['saigonbank'] = 'SAIGONBANK'
    dicVnBank['sài gòn công thương'] = 'SAIGONBANK'
    dicVnBank['co-opbank'] = 'Co-opBank'
    dicVnBank['hợp tác xã việt nam'] = 'Co-opBank'
    dicVnBank['gpbank'] = 'GPBank'
    dicVnBank['dầu khí toàn cầu'] = 'GPBank'
    dicVnBank['vrb'] = 'VRB'
    dicVnBank['liên doanh việt nga'] = 'VRB'
    dicVnBank['cb'] = 'CB'
    dicVnBank['xây dựng'] = 'CB'
    dicVnBank['pg bank'] = 'PG Bank'
    dicVnBank['xăng dầu petrolimex'] = 'PG Bank'
    dicVnBank['anzvl'] = 'ANZVL'
    dicVnBank['anz việt nam'] = 'ANZVL'
    dicVnBank['hlbvn'] = 'HLBVN'
    dicVnBank['hong leong việt nam'] = 'HLBVN'

def Main():
    PrepareBankList()

    results = []
    pageNum = 1
    while pageNum is not None:
        items = SearchNext(pageNum)
        n = len(items)
        if n <= 0:
            #break
            pass
        
        for item in items:
            url = item['url']
            publishedDate = item['publishedDate']
            publishedYear = publishedDate.year
            
            publishedDateStr = publishedDate.strftime('%Y-%m-%d')
            
            if publishedYear < 2020:
                continueSearch = False
            else:
                DownloadAndExtractProfitInfo(results, publishedDateStr, url)
                time.sleep(0.25)
        
        time.sleep(1)
        pageNum = pageNum + 1
        if pageNum > 5:
            break

    argv = sys.argv
    s = json.dumps(results)
    f = open(argv[1], 'wt')
    f.write(s)
    f.close()
    
Main()
