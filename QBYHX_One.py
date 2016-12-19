# -*- coding: utf-8 -*-
#不需要登录的获取豆瓣小号‘请不要害羞’组的帖子内容
__author__ = 'lb'
import urllib2
import re
import time
from QBYHX_Real_GetPic import QBYHX_Real_GetPic
import random
from fake_useragent import UserAgent


class QBYHX():
    def __init__(self):
        self.fh = open('E://tmp//output.txt','r+')
        self.pageIndex = self.getStartPageIndex()
        self.topics = []
        self.enable = False

        self.fu = UserAgent()
        self.headers = {
            'User-Agent': self.fu.random,
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.douban.com',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cache - Control': 'max - age = 0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        self.groupUrl = 'https://www.douban.com/group/haixiuzu/discussion?start='
        self.spider = QBYHX_Real_GetPic()



    def getStartPageIndex(self):
        lines = self.fh.readlines()
        last_lint = lines[-1]
        print last_lint
        print type(last_lint)
        return int(last_lint)

    def savePageIndexFile(self,page):
        self.fh.write('\n')
        self.fh.write(str(page))


    def getPage(self,pageIndex):
        try:
            # url = 'https://www.douban.com/group/505473/discussion?start='+str(pageIndex*25)
            url = 'https://www.douban.com/group/haixiuzu/discussion?start='+str(pageIndex*25)
            print url
            self.headers['User-Agent'] = self.fu.random
            print self.headers['User-Agent']
            request = urllib2.Request(url,headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            # print pageCode
            return pageCode
        except urllib2.URLError , e:
            if hasattr(e,'reason'):
                print(u'链接豆瓣失败，错误原因',e.reason)
                return None

    def getPageItems(self,pageIdnex):
        topics = []
        pageCode = self.getPage(pageIdnex)
        if not pageCode:
            print '页面加载失败'
            return None
        # pattern = re.compile(
        #     '<td.*?title">.*?<a.*?>(.*?)</a>.*?</td>.*?<td.*?class="">(.*?)</a>.*?</td>.*?<td.*?class="">(.*?)</td>'
        #     '.*?<td.*?class="time">(.*?)</td>', re.S)
        pattern = re.compile(
            '<td class="title">.*?<a href=(.*?) title=.*?>(.*?)</a>.*?</td>.*?<td.*?class="">(.*?)</a>.*?</td>.*?<td.*?class="">(.*?)</td>'
            '.*?<td.*?class="time">(.*?)</td>', re.S)
        items = re.findall(pattern,pageCode)
        # print items
        for item in items:
            topics.append([item[0],item[1],item[2],item[3],item[4]])
        # print topics
        return topics

    def loadPage(self):
        if self.enable == True:
            if len(self.topics) < 1:
                print 'self topics size < 1'
                topics = self.getPageItems(self.pageIndex)
                if topics:
                    self.topics.append(topics)
                    self.pageIndex += 1
                    print u'写入新的page ' + str(self.pageIndex)
                    print '0000000000000000000000'
                    self.fh.write('\n')
                    self.fh.write(str(self.pageIndex))
                    self.savePageIndexFile(self.pageIndex)
                    print '1111111111111111111111111'

                else:
                    self.enable = False

    def getOneTopic(self,topics,page):
        self.loadPage()
        for topic in topics:
            # print topic[0] + ' ' + topic[1] + ' ' + topic[2] + ' ' + topic[3]
            if topic[2] == '':
                topic[2] = 0
            print u'第%d页\turl:%s\t话题:%s\t作者:%s\t回应:%s\t时间:%s' %(page,topic[0],topic[1],topic[2],topic[3],topic[4])
            url = topic[0]
            print u'话题详情url ' + url
            time.sleep(random.uniform(1,3))
            self.spider.getPic(url)


    def start(self):
        print u'正在读取豆瓣请不要害羞小号组的内容，按回车下一条，Q退出'
        self.enable = True
        self.loadPage()
        print '第一次获取数据完毕'
        nowPage = self.pageIndex
        while self.enable:
            if len(self.topics) > 0:
                # print self.topics
                tcs = self.topics[0]
                nowPage += 1
                del self.topics[0]
                self.getOneTopic(tcs,nowPage)
                time.sleep(random.uniform(1,5))

spider = QBYHX()
spider.start()