import os.path
import getpass
import urllib.request
import urllib.parse
import time
import json
import getpass
import gzip
from bs4 import BeautifulSoup
from api import PixivLoginer

class BasicCrawler:

  def __init__(self, op, savePath='PixivPictures'):
    self.op = op
    self.savePath = savePath
    self.detailPagePrefix = 'http://www.pixiv.net/member_illust.php'

  def analyze(self, content):
    pass

  def download_real_url(self, picurl):
  	with self.op.open(picurl) as response:
  		if response.status == 200:
  			with open(os.path.join(self.savePath, picurl.split('/')[-1]), 'wb') as img:
  				img.write(response.read())
  				print('[%s] Donwloaded Successfully.' % picurl.split('/')[-1])

  def download_single(self, pid, pageRoot):
	  imgDoms = pageRoot.select('#wrapper > div._illust_modal > div > img')
	  # print (imgDom[0])
	  originalUrl = imgDoms[0]['data-src']
	  self.download_real_url(originalUrl)

  def download_multi(self, pid, pageRoot):
  	metas = pageRoot.select('ul.meta > li')
  	try:
  		picNum = int(metas[1].string.split(' ')[-1].replace('P', ''))
  	except Exception as e:
  		print ('Failed on extracting PicNum')
  	for pnum in range(0, picNum):
	  	mangaPage = self.detailPagePrefix + '?' + urllib.parse.urlencode({
	  								'mode': 'manga_big', 
	  								'illust_id': pid, 
	  								'page': pnum})
	  	with self.op.open(mangaPage) as mp:
	  		if mp.status == 200:
	  			mphtml = gzip.decompress(mp.read())
	  			mpPageRoot = BeautifulSoup(mphtml, 'lxml')
	  			imgDoms = mpPageRoot.select('img')
	  			originalUrl = imgDoms[0]['src']
	  			self.download_real_url(originalUrl)
	  		else:
	  			continue

  def download_original_imgs(self, pids):
    for pid in pids:
      try:
        detailPage = self.detailPagePrefix + '?' + urllib.parse.urlencode({
        							'mode': 'medium', 
        							'illust_id': pid})
        # detailPage = '?mode=medium&illust_id=%s' % pid
        print (detailPage)
        # visit = self.op.open(detailPage)
        with self.op.open(detailPage) as f:
          if f.status == 200:
            html = gzip.decompress(f.read())
            # print (html)
            pageRoot = BeautifulSoup(html, 'lxml')
            # whether has many pictures 
            worksDisplay = pageRoot.select('div.works_display > a')
            # print (worksDisplay)
            if worksDisplay:
            	# print ('entering multi..')
            	self.download_multi(pid, pageRoot)
            else:
            	self.download_single(pid, pageRoot)
          else:
            print('Error %s when visiting detail page %s.' % (f.status, detailPage))
            continue
          
      except Exception as e:
      	print(e)
      	print('(%s) Failed.' % pid)
      	continue

      time.sleep(0.5)
