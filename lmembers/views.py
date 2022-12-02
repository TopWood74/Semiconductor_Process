from django.shortcuts import render

import json
import urllib.request
from django.http import JsonResponse
from bs4 import BeautifulSoup

import lmembers.imembers_surprise as lms

# import surprise
# print('surprise:', surprise.__version__)

def landing(request):
    return render(
        request,
        'lmembers/landing.html'
    )

def naver(request):
    context = {}
    return render(request, 'lmembers/naver.html', context)

def naver_search(request):
    jsonObject = json.loads(request.body)
    print('jsonObject:',jsonObject)
    q = jsonObject.get('q')

    baseUrl = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=' # url주소
    url = baseUrl + urllib.parse.quote_plus(q)

    print(url)

    html = urllib.request.urlopen(url).read() #url 주소를 읽음
    soup = BeautifulSoup(html,'html.parser')

    title = soup.find_all("img", class_='thumb api_get', limit=1) #해당 클래스를 모두 찾음
    print(title)

    data = []
    for i in title:
        dict = {}
        dict['title'] = i.attrs['src']
        dict['href'] = i.attrs['src']
        data.append(dict)
        #print(i.attrs['title'])
        #print(i.attrs['href'])

    context = {'q': q, 'list': data}
    return JsonResponse(context)

def naver_search2(request):
    jsonObject = json.loads(request.body)
    print('jsonObject:',jsonObject)
    q = jsonObject.get('q')

    #baseUrl = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=' # url주소
    baseUrl = 'https://search.naver.com/search.naver?where=blog&sm=tab_opt&query='
    url = baseUrl + urllib.parse.quote_plus(q)

    print(url)

    html = urllib.request.urlopen(url).read() #url 주소를 읽음
    soup = BeautifulSoup(html,'html.parser')

    title = soup.find_all(class_='api_txt_lines total_tit') #해당 클래스를 모두 찾음

    data = []
    for i in title:
        dict = {}
        dict['title'] = i.text
        dict['href'] = i.attrs['href']
        data.append(dict)
        #print(i.attrs['title'])
        #print(i.attrs['href'])

    context = {'q': q, 'list': data}
    return JsonResponse(context)

def lmembers_surprise(request):
    jsonObject = json.loads(request.body)
    print('jsonObject:',jsonObject)
    q = jsonObject.get('q')

    # import pandas as pd
    # print('pd.__version__',pd.__version__)

    # import time
    # start = time.time()  # 시작 시간 저장

    print('#### Top-10 추천 제품 리스트 ####')
    top_pro_preds = lms.get_not_buy_member_item(q, top_n=12)
    # for top_pro in top_pro_preds:
    #    print(top_pro[0], ':', top_pro[1], top_pro[2], top_pro[3], top_pro[4], top_pro[5])

    # print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간

    data = []
    # id, rating, bgroup, mgroup, sgroup, scode
    for top_pro in top_pro_preds:
        dict = {}
        dict['id'] = top_pro[0]
        dict['rating'] = top_pro[1]
        dict['bgroup'] = top_pro[2]
        dict['mgroup'] = top_pro[3]
        dict['sgroup'] = top_pro[4]
        dict['scode'] = top_pro[5]

        data.append(dict)

    context = {'q': q, 'list': data}
    # print(context)
    return JsonResponse(context)