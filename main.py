# -*- coding: utf-8 -*-
#Created on Sun Nov 10 00:18:25 2019
#Author panxw

import requests 
import threading
import os

#要下载的m3u8网络地址
m3u8url="http://devimages.apple.com/iphone/samples/bipbop/gear1/prog_index.m3u8";

DL_DIR='dl' #下载存放目录
DL_THREADS=5 #下载并发线程数量
FILE_NAME="index.m3u8" #保存的m3u8文件名


#初始化
if not os.path.exists(DL_DIR):
    os.mkdir(DL_DIR)
lock=threading.Lock()
downloadIndex=0
tsNames=[]
tsUrls=[]


#下载m3u8文件
def getm3u8(url):
    print("downloading with requests")
    r = requests.get(url) 
    with open(DL_DIR+'/'+FILE_NAME, "wb") as code:
    	code.write(r.content)
    print("end getm3u8")


#解析ts文件流及地址
def parsem3u8(m3u8url):
    global downloadDic
    file = open(DL_DIR+'/'+FILE_NAME)
    findTag=False

    for line in file.readlines():
        line=line.strip('\n')
        if(findTag==True):
            if("#EXTINF" in line or "EXT-X-KEY" in line):
               continue
            else:
                index=line.find('?')
                if(index>-1):
                    tsname=line[0:index]
                else:
                    tsname=line
                tsurl = m3u8url[0:m3u8url.rfind('/')]+'/'+line
                tsNames.append(tsname)
                tsUrls.append(tsurl)
        if(("#EXTINF" in line) or ("#EXT-X-KEY" in line) or ("#EXT-X-KEY" in line)):
           findTag=True
        else:
            findTag=False
        if(findTag==True):
            continue
    print('end parsem3u8')


#下载任务
def downloadstream(tn):
    print('-'.join(('start thread',tn)))
    global downloadIndex
    while(True):
        lock.acquire()
        
        print(' '.join(('thread',tn,'take new work')))
        print('start '+str(downloadIndex))
        if(downloadIndex>=len(tsNames)):
            break
        tsName=tsNames[downloadIndex]
        tsUrl=tsUrls[downloadIndex]
        print(tsName)
        print(tsUrl)
        
        downloadIndex=downloadIndex+1
        lock.release()
        
        r = requests.get(tsUrl) 
        with open(DL_DIR+'/'+tsName, "wb") as code:
            code.write(r.content)
        print('end '+str(downloadIndex))



#下载m3u8,并解析   
def main():
    getm3u8(m3u8url)
    parsem3u8(m3u8url)
    
    #多线程下载
    for i in range(DL_THREADS):  
        p = threading.Thread(target=downloadstream,args=(str(i),))
        p.start()
    pass



#运行
main()
