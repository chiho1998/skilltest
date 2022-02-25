import pandas as pd
from bs4 import BeautifulSoup 
import numpy as np
from urllib.request import urlopen, Request
import requests
from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1/test")
db = client['database']

baselink='https://news.mingpao.com/'
link='https://news.mingpao.com/pns/%E6%98%8E%E5%A0%B1%E6%96%B0%E8%81%9E%E7%B6%B2/main'
r = requests.session()
k = BeautifulSoup(r.get(link).text)

ltype = []
typenewslink =[]
pro=[]
cont=[]
time=[]
title=[]
ntype=[]
newsfrom = []



for i in k.find_all('div',{'class':'subtitle'}):
    newstype = sub = i.find('a').get('href')
    typenewslink.append(baselink + newstype.replace('../',""))


for i in typenewslink:
    l = BeautifulSoup(r.get(i).text)
    for o in l.find_all('li',{'class':'list_sub'}):
        sub = o.find('a').get('href')
        pro.append(baselink + sub.replace('../',""))
        
for i in pro:
    c = BeautifulSoup(r.get(i).text)
    cont.append(c.find('article',class_='txt4').text.replace('\n',''))
    time.append(c.find_all('div',{"class":"date"})[2].text)
    title.append(c.find('div',class_="incontent").find('hgroup').text)
    ntype.append(c.find('div',class_ = 'colleft').find('h3').text)
    newsfrom.append('明報')
    
d = {'title':title,'contant':cont, 'time':time, 'title':title,'type':ntype}
df = pd.DataFrame(data=d)


db.news.insert_many(df.to_dict('records'))