import urllib.request, urllib.error, urllib.parse
import json
import mypath as path
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import requests
import decodeCaptcha
import random
from selenium import webdriver
from PIL import Image
from selenium.webdriver.common.keys import Keys
import sys

def urlremain(url):
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        return True
    except urllib.error.URLError:
        return False

def getWotScore(url):
    ulrwot='http://api.mywot.com/0.4/public_link_json2?hosts='+url+'&key=373fe6c5f2a19ef6841fb3965fd06f480d975e1e'
    req = urllib.request.Request(ulrwot)
    response = urllib.request.urlopen(req).read().decode('utf-8')
    return response


# Json = json.loads(getWotScore('http://bit.ly/1HXqx4O'))
# print(Json['bit.ly']['0'][0])


# proto, rest = urllib.parse("docs.python.org/dsds")
# res, rest = urllib.splithost(rest)
# print ("unkonw" if not res else res)

UlrWot=dict()
listofproxy=[]

with open(path.TweetJSONpath+'URLsNews.txt', mode='r')as Seenlist2:
     for line in Seenlist2:
         line=json.loads(line.replace("\n",''))[1]
         UlrWot[line]=0

# with open(path.datapath+'/webpagefortwitter/Tweet_JSON/'+'URLs.txt', mode='r')as Seenlist2:
#      for line in Seenlist2:
#          line=line.replace("\n",'')
#          UlrWot[line]=0
# with open(path.datapath+'/webpagefortwitter/Tweet_JSON/'+'URLsBBC.txt', mode='r')as Seenlist2:
#      for line in Seenlist2:
#          line=line.replace("\n",'')
#          UlrWot[line]=0
#
# with open(path.datapath+'/webpagefortwitter/Tweet_JSON/'+'WOtURLs.txt', mode='r')as Seenlist2:
#      for line in Seenlist2:
#          line=line.replace("\n",'').split("   ")
#          UlrWot[line[0]]=line[1]

outfile=path.TweetJSONpath+'WOtURLs2.txt'

listofweb=[]
try:
    with open(outfile, mode='r')as Seenlist2:
        for line in Seenlist2:
            print(line)
            url=json.loads(line)['url']
            listofweb.append(url)
except FileNotFoundError:
    pass

with open(path.TweetJSONpath+'WOtURLs.txt', mode='r')as Seenlist2:
    for line in Seenlist2:
        url=json.loads(line)['url']
        listofweb.append(url)
with open(path.TweetJSONpath+'WOtURLs2.txt', mode='r')as Seenlist2:
    for line in Seenlist2:
        url=json.loads(line)['url']
        listofweb.append(url)



def getHeader():
    ua = UserAgent()
    header={'User-agent': ua.random,'DNT': "1",'Accept-Language': "en-US;q=0.8,en;q=0.2",'Accept-Encoding': "deflate, sdch"}
    return header    

            # proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
            #
            # opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
            # opener.addheaders =[('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'),('DNT', "1"),('Accept-Language', "en-US;q=0.8,en;q=0.2"),('Accept-Encoding', "gzip, deflate, sdch")]
            # opener.open('http://www.google.com').read()
            #res = conn.getresponse()
       # except socket.gaierror:


#proxies=getProxy()
def getRanknoproxy(url):
    #opener = urllib.request.build_opener()
    # header=getHeader()
    # if len(header) ==0:
    #     header=getHeader()
    #proxies=getProxy()
    try:
        print('http://www.alexa.com/siteinfo/'+url)
        data=requests.get('http://www.alexa.com/siteinfo/'+url).text
        return phaseAlexa(data)
    except Exception as e:
        print('getRank error')
        print(e)
        return 'error'

# def getRank(url,proxies):
#     #opener = urllib.request.build_opener()
#     # header=getHeader()
#     # if len(header) ==0:
#     #     header=getHeader()
#     #proxies=getProxy()
#     try:
#         data=requests.get('http://www.alexa.com/siteinfo/'+url,proxies=proxies).text
#         return phaseAlexa(data)
#     except Exception:
#         print('getRank error')
#
#         return 'error'
    #data=opener.open('http://www.alexa.com/siteinfo/'+url).read()
    #data=data.decode('utf-8')

#16,852,849"
def getNum(numstring):
    numberstr='0123456789.'
    tempstr=numstring
    for char in numstring:
        if char not in numberstr:
            tempstr=tempstr.replace(char,'')
    return int(tempstr)
def phaseAlexa(html):
    css_soup = BeautifulSoup(html)
    if css_soup.find('h1')!=None and  css_soup.find('h1').text=='Forbidden':
       return 'error'

    try:
        #css_soup.select(".align-vmiddle")
        rank= css_soup.select(".change-r2")[0].parent.strong.text.replace('\n','')

        return getNum(rank)
    except Exception:
        return 20000000


def getTypenoproxy(url,captcha=None):
    #proxies=getProxy()
    try:
        header=getHeader()
        r=None
        if captcha==None:
            r = requests.post('http://sitereview.bluecoat.com/rest/categorization', data = {'url':url},headers=header,timeout=4)
        else:
            print("get type with captcha     "+str(captcha))
            r = requests.post('http://sitereview.bluecoat.com/rest/categorization', data = {'url':url,'captcha':captcha},headers=header,timeout=4)
        #print("get type with proxy"+str(proxies))
        data=r.json()
        return phaseTypes(url,data)

    except Exception:
        return 'error'
def getType(url,proxies):
    #proxies=getProxy()
    try:
        header=getHeader()
        r = requests.post('http://sitereview.bluecoat.com/rest/categorization', data = {'url':url},proxies=proxies,headers=header,timeout=4)
        print("get type with proxy"+str(proxies))
        data=r.json()
        return phaseTypes(url,data)

    except Exception:
        # postdata = urllib.parse.urlencode({'url': url})
        # postdata = postdata.encode('utf-8')
        #
        # response = urllib.request.urlopen('http://sitereview.bluecoat.com/rest/categorization',postdata)
        # text =response.read().decode('utf-8')
        # time.sleep('15')
        return 'error'

     #return phaseTypes(url,)
     #return phaseTypes(data)
def inputcaptcha(url):
    bowser =webdriver.Chrome('/Users/licheng5625/PythonCode/masterarbeit/coder/snopesCrawler/chromedriver')

    bowser.get('http://sitereview.bluecoat.com/sitereview.jsp#/?search='+'google.com')
    #
    #
    # element = bowser.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "bluecoat_logo", " " ))]')#//*[contains(concat( " ", @class, " " ), concat( " ", "captcha", " " ))]')
    #
    # time.sleep(20)
    bowser.save_screenshot('screenshot.png') # saves screenshot of entire page
    #
    im = Image.open('screenshot.png') # uses PIL library to open image in memory
    #
    im = im.crop((80, 800, 480, 900)) # defines crop points
    captcha=decodeCaptcha.decode_captcha(im)
    print(captcha)
    im.save('screenshot2.png') # saves new cropped image
    inputElement = bowser.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "smallInput", " " ))]')
    inputElement.send_keys(captcha)
    inputElement.send_keys(Keys.ENTER)
    bowser.quit()

    print(url)
def phaseTypes(url,html):
    rank ="no type"
    print(html)
    if 'error' in html.keys():
        if html['error']=='Please complete the CAPTCHA':
            inputcaptcha(url)
            return 'error'
        else:
            print(url)
            sys.exit()
    try:
        if not html['unrated']:
            css_soup = BeautifulSoup(html['categorization'])
            #print(html['categorization'])
            #css_soup.select(".align-vmiddle")
            try:
                rank= css_soup.find_all("a")[1].text#.findall('a')
            except IndexError:
                rank= css_soup.find_all("a")[0].text
    except KeyError:
        inputcaptcha(url)
        #time.sleep(5)

        print('phaseTypes error')
        return 'error'
    print(rank)
    return rank


blacklistproxy=set()
def getProxy():
        global blacklistproxy
        print('change proxy')
        proxy=None
        while proxy==None:
            try:
                proxy=random.choice(listofproxy)
                while proxy['proto']=='https' or proxy['url'] in blacklistproxy:
                    assert len(listofproxy)>len(blacklistproxy)
                    proxy=random.choice(listofproxy)
                # proxies = {
                #     proxy.split('://')[0]:proxy}
                proxies={proxy['proto']:proxy['url']}
                #print(proxies)
                requests.get('http://www.alexa.com/siteinfo/'+'google.com',proxies=proxies,timeout=4)
                proxy = proxies
            except Exception as e:
                blacklistproxy.add(proxy['url'])
                print(float(len(blacklistproxy))/len(proxy))
                #print(str(proxy)+str(e))
                return None
        print('pick:'+str(proxy))
        return proxy
#'http': 'http://111.13.136.36:80'
#'http': 'http://120.198.248.97:80'
#http://80.112.170.75:80
#'http': 'http://103.27.24.236:83'
#http://123.126.32.102:8080
# bowser =webdriver.Chrome('/Users/licheng5625/PythonCode/masterarbeit/coder/snopesCrawler/chromedriver')
# html2=bowser.get('https://www.google.com').page_source#'http://sitereview.bluecoat.com/sitereview.jsp#/?search='+url)
#
# css_soup = BeautifulSoup(html2)
# css_soup=css_soup.select(".captcha")
# bowser =webdriver.Chrome('/Users/licheng5625/PythonCode/masterarbeit/coder/snopesCrawler/chromedriver')
# bowser.get('http://sitereview.bluecoat.com/sitereview.jsp#/?search='+'google.com')
#html2=bowser.page_source
# img = bowser.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "captcha", " " ))]').screenshot('ds')

# css_soup = BeautifulSoup(html2)
# css_soup=css_soup.select(".captcha")[0].get('src')
# print(css_soup)
UlrWotold={}
# with open(path.TweetJSONpath+'WOtURLsOLD.txt', mode='r')as Seenlist2:
#      for line in Seenlist2:
#          line=json.loads(line)
#          UlrWotold[line['url']]=line

sss='www.kairalinewsonline.comreal-or-fake-photo-of-worlds-darkest-baby-goes-viral'
with open(outfile, mode='a')as Seenlist2:
        wotdict=dict()
        proxies=None
        # while proxies==None:
        #     proxies=getProxy()
        count=0
        for key in UlrWot.keys():
            count+=1
            if key not in listofweb :
                if key=='turkey':
                    continue
                if key=='' or key=='\n' or len(key)>70 or key=='California.http:' or len(key)<5 or 'www.businessi' in key or 'khilafah.com'in key or 'inlocalneworleans' in key or 'comnews' in key:
                    continue
                if 'tumblr' not in key:

                    print(str( count)+"--------"+str(len(UlrWot)))
                    if key not in UlrWotold.keys():
                        wotdict['type']=getTypenoproxy(key)
                        while wotdict['type']=='error':
                            wotdict['type']=getTypenoproxy(key)
                    else:
                        wotdict['type']=UlrWotold[key]['type']
                        # blacklistproxy.add(proxies['http'])
                        # proxies=None
                        # while proxies==None:
                        #     proxies=getProxy()
                        # wotdict['type']=getType(key,proxies)
                    if key  in UlrWotold.keys() and UlrWotold[key]['rank']!=20000000:
                        wotdict['rank']=UlrWotold[key]['rank']#,proxies)
                    else:
                        wotdict['rank']=getRanknoproxy(key)#,proxies)
                        if wotdict['rank']=='error':
                            print('get rank error')
                            break
                    #while wotdict['rank']=='error':
                        # if proxies!=None:
                        #     blacklistproxy.add(proxies['http'])
                        # proxies=None
                        # while proxies==None:
                        #     proxies=getProxy()
                        #wotdict['rank']=getRanknoproxy(key)
                        #wotdict['rank']=getRank(key,proxies)
                    wotdict['url']=key
                    #if UlrWot[key]!=0:
                    if key in UlrWotold.keys() and UlrWotold[key]['wot']!=0:
                        wotdict['wot']=UlrWotold[key]['wot']
                    else:
                        Json = json.loads(getWotScore(key+'/'))
                        print(Json)
                        try:
                            wotdict['wot']=Json[key]['0'][0]
                        except KeyError:
                            wotdict['wot']=0
                    # else:
                    #         wotdict['wot']=0
                else:
                    wotdict['wot']=0
                    wotdict['rank']=20000000
                    wotdict['type']='no type'
                    wotdict['url']=key
                listofweb.append(key)
                Seenlist2.write(json.dumps(wotdict)+"\n")


# proxies=None
# while proxies==None:
#     proxies=getProxy()
# print(proxies)
# header=getHeader()
# data=requests.get('http://www.whatsmyip.org/more-info-about-you/',proxies=proxies,headers=header).text
# print(data)