#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
# Author: zioer
# Created Time: 2020年08月29日 星期六 23时50分36秒
# Brief: Cookies信息管理工具
###############################################################################

import json
import base64
import os
import re
import sys
import time
import logging
import logging.config
import argparse
import asyncio
from pyppeteer import launch
from multiprocessing.dummy import Pool as ThreadPool
from redis import StrictRedis
import blog_conf


ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
# 无头模式，通过JS屏蔽`webdriver`检测
js0 = '''() =>{Object.defineProperty(navigator, 'webdriver', {get: () => undefined });}'''


class CookiesPool(object):
    '''
    博客文章发布工具
    '''
    def __init__(self, config):
        '''
        设置初始参数: 对于子类，只需要修改下面必须字段信息即可实现新的Blog发布对象
        '''
        self.platform = config["platform"]             # Blog平台名称,必须
        self.has_captcha = config['has_captcha']       # 是否包含验证码
        self.login_url = config['login_url']
        self.login_tab = config['login_tab']
        self.ele_login = config['ele_login']
        self.ele_pass = config['ele_pass']
        self.login_btn = config['login_btn']
        self.title_id = config['title_id']            # 标题内容CSS选择器,必须
        self.text_id = config['text_id']              # 文章内容CSS选择器,必须
        self.pub_btn = config['pub_btn']              # 发布按钮CSS选择器,必须
        self.new_post_url = config['new_post_url']
        self.check_url = config['check_url']
        self.cookies_url_list = config['cookies_url_list']

        redis_uri = config['redis_uri']
        self.db = StrictRedis.from_url(redis_uri)
        self.cookie_table = config['cookie_info'] + '_' + self.platform
        self.user_info = config['user_info'] + '_' + self.platform

        # logging config
        logging.config.fileConfig(config['log_conf'])
        self.logger = logging.getLogger('main')
        self.browser = None
        self.page = None

    async def get_browser(self, headless=True):
        """
        打开浏览器返回浏览器第一个页面对象
        """
        # proxy_server = "--proxy-server=socks5://127.0.0.1:1081"
        # browser_args = ['--disable-infobars', proxy_server]
        browser_args = ['--disable-infobars', ]
        # headless参数设为False，则变成有头模式
        headless = headless
        autoClose = True
        if self.has_captcha:
            autoClose = False
            headless = False
        browser = await launch(headless=headless, args=browser_args, autoClose=autoClose)
        pages = await browser.pages()
        page1 = pages[0]
        # 设置页面视图大小
        await page1.setViewport(viewport={'width': 1280, 'height': 800})
        await page1.setUserAgent(ua)
        await page1.evaluateOnNewDocument(js0)
        self.browser = browser
        self.page = page1
        return page1

    async def get_page(self):
        """新建Tab页面
        return:
            page
        """
        if self.browser is None:
            raise ValueError("browser is None")
        browser = self.browser
        page = await browser.newPage()
        # 设置页面视图大小
        await page.setViewport(viewport={'width': 1280, 'height': 800})
        await page.setUserAgent(ua)
        await page.evaluateOnNewDocument(js0)
        self.page = page
        return page

    async def login(self, username, password):
        """
        账号登录
        params:
            username: 用户名
            password: 密码
        return:
            bool True:登录成功，False失败
        """
        login_url = self.login_url
        login_tab = self.login_tab
        ele_login = self.ele_login
        ele_pass = self.ele_pass
        login_btn = self.login_btn
        has_captcha = self.has_captcha
        try:
            page1 = self.page
            await page1.goto(login_url)

            if login_tab is not None and login_tab != '':
                ele = await page1.J(login_tab)
                await ele.click()
            ele = await page1.J(ele_login)
            await ele.type(username)
            ele = await page1.J(ele_pass)
            await ele.type(password)
            ele = await page1.J(login_btn)
            await ele.click()
            if has_captcha:
                await page1.waitFor(20*1000)
            await page1.waitFor(10*1000)
            return True
        except Exception as e:
            self.logger.exception(f'usename:{username}, login_url: {login_url}, debug_wsEndpoint: {self.browser.wsEndpoint}, exception:{e}.')
        return False

    async def get_cookies(self):
        '''提取登陆成功后的cookies信息字符串
        return:
            cookies List类型,包含多个URL的cookies信息的Dict类型数据列表
        '''
        url_list = self.cookies_url_list
        if self.page is None:
            raise ValueError("browser is None")
        cookies = await self.page.cookies(*url_list)
        return cookies

    async def check_account(self, username):
        '''
        检查cookie有效性： 访问账户设置页面如果重定向到登录页面就说明cookie失效
        params:
            username: 需要检验的用户名
        return:
            bool: True: 用户cookie有效，False: 无效
        '''
        check_url = self.check_url
        cookies = self.read_cookies(username)
        if cookies is None:
            return False
        try:
            page = self.page
            for cookie in cookies:
                await page.setCookie(cookie)
            await page.goto(check_url)

            real_url = page.url
            self.logger.debug(f'check_url:{check_url}, real_url:{real_url}, status:{real_url.startswith(check_url)}')
            if real_url.startswith(check_url):
                return True
        except Exception as e:
            self.logger.exception(f'username:{username}, check_url: {check_url}, cookies: {len(cookies)}, Exception:{e}')
        return False

    def write_cookies(self, username, cookies):
        """保存cookie信息"""
        db = self.db
        key = username
        value = json.dumps(cookies)
        ret = db.hset(self.cookie_table, key, value)
        if ret > 0:
            return True
        return False

    def read_cookies(self, username):
        """读取cookie信息
        params:
            username: 用户名
        return:
            cookies: List, Dict类型数据的列表
        """
        db = self.db
        data = db.hget(self.cookie_table, username)
        self.logger.debug(f'username:{username}, {self.cookie_table}, cookies:{data}')
        if isinstance(data, bytes):
            data = data.decode()
        if data is None or data == '':
            return None
        return json.loads(data)

    def get_accounts(self):
        """获取账号信息"""
        db = self.db
        self.logger.debug(f'user_info:{self.user_info}')
        data_list = db.smembers(self.user_info)
        if len(data_list) > 0:
            return data_list
        return []

    def del_accounts(self, value):
        """删除账号信息"""
        db = self.db
        if db.sismember(self.user_info, value):
            ret = db.srem(self.user_info, value)
            self.logger.info(f'delete operation, set: {self.user_info}, ret: {ret}')
            return True
        else:
            self.logger.info(f'{value} not in set: {self.user_info}')
        return False

    def set_accounts(self, value):
        """设置账号信息: 账号格式: `username|password`"""
        db = self.db
        ret = db.sadd(self.user_info, value)
        self.logger.info(f'set operation, set: {self.user_info}, ret: {ret}')
        if ret > 0:
            return True
        return False

    def load_accounts(self, file):
        """设置账号信息: 账号格式: `username|password`"""
        if not os.path.exists(file):
            self.logger.error(f"{file} not exists!")
            return False
        with open(file, 'r') as f:
            data_list = f.readlines()
        db = self.db
        for data in data_list:
            data = data.strip()
            if len(data.split('|')) != 2:
                self.logger.error(f'set operation, format error: {data}')
                continue
            ret = db.sadd(self.user_info, data)
            self.logger.info(f'set operation, set: {self.user_info}, ret: {ret}')
        return True

    async def start(self, debug=False):
        '''
        主流程人物执行
        1. 有效性检查 check
        2. 失效删除
        3. 失效账号重新登录 login
        4. 提取新生效账号 get_cookies
        5. 更新到数据库中 write_cookies
        '''
        headless = True
        if debug is True:
            headless = False
        try:
            await self.get_browser(headless)
            user_list = self.get_accounts()
            for user in user_list:
                username, password = user.decode().split('|')
                status = await self.check_account(username)
                self.logger.debug(f"user:{username}, status:{status}")
                if not status:
                    # cookies失效
                    self.logger.warning(f"{username} cookies 失效，开始重新登录更新Cookies.")
                    login_status = await self.login(username, password)
                    if login_status:
                        cookies = await self.get_cookies()
                        self.write_cookies(username, cookies)
                        self.logger.info(f"{username} cookies 更新成功!")
                    else:
                        self.logger.info(f"{username} 登录失败, 更新Cookies失败!")
                else:
                    self.logger.info(f"{username} cookies 信息有效，不用更新了!")
        except Exception as e:
            self.logger.exception(e)
        # time.sleep(100)

    async def post(self, md_title, md_content):
        """文章内容发布
        params:
            md_title: 标题
            md_content: 正文内容
        return:
            bool  True:成功,False:失败
        """
        title_id = self.title_id
        text_id = self.text_id
        pub_btn = self.pub_btn
        new_post_url = self.new_post_url
        try:
            page = await self.get_browser()
            user_list = self.get_accounts()
            for user in user_list:
                username, password = user.decode().split('|')
                cookies = self.read_cookies(username)
                if cookies is None:
                    self.logger.warning("user:{username} cookies is None. continue to post next account!")
                    continue
                for cookie in cookies:
                    await page.setCookie(cookie)
                await page.goto(new_post_url)

                ele = await page.J(title_id)
                await ele.focus()
                await ele.type(md_title)

                ele = await page.J(text_id)
                await ele.focus()
                await ele.type(md_content)

                ele = await page.J(pub_btn)
                await ele.click()
            time.sleep(3)
            return True
        except Exception as e:
            self.logger.exception(e)
        return False

if __name__ == '__main__':

    parser = argparse.ArgumentParser('Cookies池管理工具')

    parser.add_argument('-c', '--check', action='store_true', default=False, help='执行Cookies有效性检查')
    parser.add_argument('-s', '--set', help='设置用户名和密码信息')
    parser.add_argument('-d', '--delete', help='删除用户名和密码信息')
    parser.add_argument('-g', '--get', action='store_true', default=False, help='提取用户名和密码信息')
    parser.add_argument('-l', '--load', default=None, help='文件中加载用户名和密码信息,格式(两列数据，分隔符为竖线)：username|password')
    parser.add_argument('-p', '--post', default=None, help='发布Markdown文章,Markdown文件存放路径')
    parser.add_argument('-t', '--title', default=None, help='文章标题')
    parser.add_argument('-m', '--plat', default=None, help='Blog平台信息')

    # 调试模式开关
    parser.add_argument('-x', '--debug', default=True, help='调试模式')

    parse_result = parser.parse_args()
    check = parse_result.check
    acc_set = parse_result.set
    acc_get = parse_result.get
    acc_del = parse_result.delete
    acc_load = parse_result.load
    title = parse_result.title
    post = parse_result.post
    debug = parse_result.debug
    plat = parse_result.plat

    conf_list = blog_conf.config_list

    if post:
        print("start to post article:")
        if not os.path.exists(post):
            print(f"{post} file not exists!")
            exit(1)
        if title is None:
            filepath = post.rsplit('/', maxsplit=1)
            title = filepath[len(filepath) - 1].replace('.md', '')
        print('title:', title)
        with open(post, 'r') as f:
            md_content = f.read()
        task_list = [CookiesPool(conf).post(title, md_content) for conf in conf_list]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(task_list))
    elif check:
        task_list = [CookiesPool(conf).start(debug) for conf in conf_list]
        print("start to check account cookies info:")
        asyncio.get_event_loop().run_until_complete(asyncio.wait(task_list))

    else:
        if plat is None:
            print("plat is None")
            exit(1)
        config = None
        for conf in conf_list:
            if conf['platform'] == plat:
                config = conf
                break
        if config is None:
            print(f"{plat} is not found!")
            exit(2)
        blog = CookiesPool(config)
        if acc_set:
            print("start to set account:", acc_set)
            ret = blog.set_accounts(acc_set)
            ret = blog.get_accounts()
            print('get ret:', ret)
        elif acc_del:
            print("start to del account:", acc_del)
            blog.del_accounts(acc_del)
        elif acc_get:
            print("start to get account:", acc_get)
            ret = blog.get_accounts()
            if ret:
                for i in list(ret):
                    print(i.decode())
        elif acc_load:
            print("start to load accounts:", acc_load)
            blog.load_accounts(acc_load)
