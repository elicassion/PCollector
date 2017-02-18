#!/usr/bin/env python3
# -*- coding: utf8 -*-

import urllib.request
import http.cookiejar
import urllib.parse
import re
import os.path
import utils
import getpass


pixiv_url_login = "https://accounts.pixiv.net/login"
pixiv_url_login_post = 'https://accounts.pixiv.net/api/login'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'Host': 'accounts.pixiv.net',
    'Referer': 'http://www.pixiv.net/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/50.0.2661.102 Safari/537.36'
}


def getopener(header):
    cj = http.cookiejar.CookieJar()
    cp = urllib.request.HTTPCookieProcessor(cj)
    op = urllib.request.build_opener(cp)
    h = []
    for key, value in header.items():
        elem = (key, value)
        h.append(elem)
    op.addheaders = h
    return op


def getpostkey(body):
    res = re.search('name="post_key" value="\w*', body)
    if res:
        return res.group().split('"')[-1]
    else:
        return None


def login(uid, pwd):
    op = getopener(headers)

    # 访问登陆界面，获取登陆所需的post_key
    op_key = op.open(pixiv_url_login)

    data = op_key.read()
    op_key.close()
    data = utils.ungzip(data).decode()

    # 初始化登陆所需提交的数据
    pixiv_key = getpostkey(data)
    pixiv_id = uid
    pixiv_password = pwd
    pixiv_source = 'accounts'

    post_data = {
        'pixiv_id': pixiv_id,
        'password': pixiv_password,
        'post_key': pixiv_key,
        'source': pixiv_source
    }
    post_data = urllib.parse.urlencode(post_data).encode('utf-8')

    # 提交登录数据
    
    op_login = op.open(pixiv_url_login_post, post_data)
    op_login.close()

    # 返回带cookie管理的opener
    return op
