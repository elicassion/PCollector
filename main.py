#!/usr/bin/env python3
# -*- coding: utf8 -*-

import getpass
import os
from api import PixivLoginer
from crawler.RankingCrawler import RankingCrawler
from crawler.BasicCrawler import BasicCrawler


if __name__ == '__main__':
    while True:
        userid = input("请输入用户名：")
        password = getpass.getpass(prompt="请输入密码：")
        try:
            opener = PixivLoginer.login(userid, password)
            print ('登录成功，耶！')
            break
        except Exception as e:
            print ('登录失败，僵，请重试...')

    while True:
        save_dir = input("请输入插图保存文件夹路径(默认本文件夹下PixivPictures)：")
        try : 
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            print ('读取文件夹成功')
            break
        except Exception as e:
            print ('读取文件夹失败...')

    mode_num = input('''请选择爬取插图排行榜类型(0：今日 | 1：本周 | 2：本月 | 3：新人 | 4：原创 | 5：受男性欢迎 | 6：受女性欢迎)：''')
    while int(mode_num) < 0 or int(mode_num) > 6:
        mode_num = ("排行榜类型值超出范围，请重新输入：")

    page_num = input('请输入爬取数量(页数，≤10)：')
    while True:
        try:
            if int(page_num) <= 0:
                page_num = input('请重新输入大于零的整数作为页数：')
            elif int(page_num) > 10:
                print ('排行榜没那么多辣，最多10页，已按10页开始下载')
                break
            else:
                break
        except Exception as e:
            page_num = input('页码是整数...请重新输入')

    rc = RankingCrawler(opener, int(mode_num), save_dir, page_num)
    print ('-----------------Begin Download------------------')
    rc.begin_download()