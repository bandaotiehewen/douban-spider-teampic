# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'lb'
__mtime__ = '2016/12/7'
__des__='获取豆瓣请不要害羞小组中的图片'
"""
__author__ = 'lb'
import urllib2
import re
import json
from fake_useragent import UserAgent


class QBYHX_Real_GetPic():
	def __init__(self):
		print u'开始初始化信息'
		self.filedir = 'E://tmp//mainqbyhx//'

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

	def getPage(self, url):
		try:
			self.headers['User-Agent'] = self.fu.random
			print self.headers['User-Agent']
			req = urllib2.Request(url,headers=self.headers)
			rsp = urllib2.urlopen(req)
			pageContent = rsp.read().decode('utf-8')
			return pageContent
		except urllib2.URLError, e:
			if hasattr(e, 'reason'):
				print (u'豆瓣获取页面失败', e.reason)
				return None

	def getPic(self, url):
		url = url[1:-1]
		print url
		page = self.getPage(url)
		if not page:
			print u'页面加载失败'
			return None
		pattern = re.compile('<div class="topic-figure cc">.*?<img src="(.*?)" alt="" class="">', re.S)
		items = re.findall(pattern, page)
		print items
		for item in items:
			# print isinstance(item,(object))
			tmp = json.dumps(item)
			picUrl = tmp[1:-1]
			picName = picUrl.split('/')[7]
			self.savePic(picUrl,picName)


	def savePic(self,picurl,picName):
		print '图片URL ' + picurl
		print '图片名字 ' + picName
		try:
			req = urllib2.Request(picurl,headers=self.headers)
			rsp = urllib2.urlopen(req)
			data = rsp.read()
		except urllib2.URLError, e:
			if hasattr(e, 'reason'):
				print (u'豆瓣获取图片页面失败', e.reason)
				return None
		picName = self.filedir + picName
		print u'图片位置 ' + picName
		f = open(picName,'wb')
		f.write(data)
		f.close()

# url = 'https://www.douban.com/group/topic/93328842'
# url = 'https://www.douban.com/group/topic/94228175/'
# spider = QBYHX_Real_GetPic()
# spider.getPic(url)