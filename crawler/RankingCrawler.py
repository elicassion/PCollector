#!/usr/bin/env python3
# -*- coding: utf8 -*-

import urllib.request
import urllib.parse
import os.path
import utils
import time
import json
import getpass
from bs4 import BeautifulSoup
from api import PixivLoginer
from basic.PItem import PItem
from crawler.BasicCrawler import BasicCrawler

class RankingCrawler(BasicCrawler):
  def __init__(self, op, rank_type_num=0, saveDir='PixivPictures', max_pages=3):
    super(RankingCrawler, self).__init__(op, saveDir)
    self.pixiv_url_ranking = 'http://www.pixiv.net/ranking.php'
    self.rank_types = [
      'daily',
      'weekly',
      'monthly',
      'rookie',
      'original',
      'male',
      'female'
    ]
    self.query_format = 'json'
    self.query_tt = None
    self.rank_type_num = rank_type_num
    self.cur_page = 0
    self.max_pages = max_pages
    self.mode = self.rank_types[rank_type_num]



  def analyze_html(self, html):
    pids = []
    rootSoup = BeautifulSoup(html, 'lxml')
    selector = rootSoup.select('#wrapper > div.layout-body > div > '
                'div.ranking-items-container > div.ranking-items.adjust > section')

    for child in selector:
      pid = child['data-id']
      pids.append(pid)
    return pids


  def analyze_json(self, js):
    pid = []
    contents = json.loads(js)['contents']
    for child in contents:
      pid = child['illust_id']
      pids.append(pid)

    return pids


  def get_tt(self, html):
    rootSoup = BeautifulSoup(html, 'lxml')
    tt = rootSoup.select('#wrapper > footer > div > ul > li')[0].select('form > input')[1]['value']
    return tt

  def fetch_first_page(self):
    visit = self.pixiv_url_ranking + '?' + urllib.parse.urlencode({'mode': self.mode})
    # print('visit: ', visit)
    tt = None
    items = None

    with self.op.open(visit) as f:
      if f.status == 200:
        html = utils.ungzip(f.read()).decode()
        self.tt = self.get_tt(html)
        items = self.analyze_html(html)

    if items:
      self.download_original_imgs(items)
      print ('------------Page %d Done.------------' % self.cur_page+1)



  def fetch_more_page(self):
    visit = self.pixiv_url_ranking + '?' + urllib.parse.urlencode({
      'mode': self.mode,
      'p': self.cur_page,
      'format': self.query_format,
      'tt': self.query_tt
    })

    items = None

    with self.op.open(visit) as f:
      if f.status == 200:
        js = utils.ungzip(f.read()).decode()
        items = self.analyze_json(js)

    if items:
      self.download_original_imgs(items)
      print ('------------Page %d Done.------------' % self.cur_page+1)

  def fetch_pages(self):
    self.fetch_first_page()
    self.cur_page += 1
    while (self.cur_page < self.max_pages):
      self.fetch_more_page()
      self.cur_page += 1

  def begin_download(self):
    self.fetch_pages()
