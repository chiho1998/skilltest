import pandas as pd
from bs4 import BeautifulSoup 
import numpy as np
from urllib.request import urlopen, Request
import requests
from pymongo import MongoClient
client = MongoClient("mongodb://127.0.0.1/test")
db = client['database']

link='https://std.stheadline.com/daily/hongkong/%E6%97%A5%E5%A0%B1-%E6%B8%AF%E8%81%9E'
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

baselink='https://std.stheadline.com/'

link =[
    'https://std.stheadline.com/daily/editorial/%E6%97%A5%E5%A0%B1-%E7%A4%BE%E8%AB%96',
    'https://std.stheadline.com/daily/hongkong/%E6%97%A5%E5%A0%B1-%E6%B8%AF%E8%81%9E',
    'https://std.stheadline.com/daily/education/%E6%97%A5%E5%A0%B1-%E6%95%99%E8%82%B2',
    'https://std.stheadline.com/daily/property/%E6%97%A5%E5%A0%B1-%E5%9C%B0%E7%94%A2',
    'https://std.stheadline.com/daily/finance/%E6%97%A5%E5%A0%B1-%E9%87%91%E8%9E%8D',
    'https://std.stheadline.com/daily/entertainment/%E6%97%A5%E5%A0%B1-%E5%A8%9B%E6%A8%82',
    'https://std.stheadline.com/daily/sport/%E6%97%A5%E5%A0%B1-%E9%AB%94%E8%82%B2',
    'https://std.stheadline.com/daily/international/%E6%97%A5%E5%A0%B1-%E5%9C%8B%E9%9A%9B',
    'https://std.stheadline.com/daily/china/%E6%97%A5%E5%A0%B1-%E4%B8%AD%E5%9C%8B'
    
] 

#get newslink
for i in link:
    k = BeautifulSoup(r.get(i).text)
    for o in k.find_all('h2',{'class':'h5 my-2'}):
        pro.append(o.find('a').get('href'))


for i in pro:
    c = BeautifulSoup(r.get(i).text)
    cont.append(c.find('div','paragraphs medium').text)
    title.append(c.find('h1').text)#title
    time.append(c.find('span',class_='date').text)#time
    newsfrom.append('星島日報')
for i in pro:
    ntype.append(i.split('-')[1])

d = {'title':title,'contant':cont, 'time':time, 'title':title,'type':ntype,'newsfrom':newsfrom}
df = pd.DataFrame(data=d)
df

db.news.insert_many(df.to_dict('records'))