#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
# Author: zioer
# Created Time: 2020年09月17日 星期四 15时03分57秒
# Brief: 配置博客平台信息
###############################################################################

redis_uri = 'redis://localhost:6379/1'

# 用户信息集合 {username, password, platform}
user_info = 'user_info'

# 登录成功用户的Cookie池信息: key={platform}#{username}, value={cookies} , 如果cookie失效会立即删除
cookie_info = 'user_cookies'

# 日志配置文件
log_conf = './logging.conf'

# 支持多平台配置参数化

config_list = [
    {
        "platform": "cnblogs",             # Blog平台名称,必须
        "has_captcha": False,               # 是否有验证码，有就等待30秒
        'login_url': 'https://account.cnblogs.com/signin',
        'login_tab': 'div.mat-tab-label-content',   # 登录TAB页面显示
        'ele_login': '#mat-input-0',      # 用户名
        'ele_pass': '#mat-input-1',       # 密码
        'login_btn': '.mat-button-wrapper',  # 登录按钮
        "title_id": '#post-title',        # 标题内容CSS选择器,必须
        "text_id": '#md-editor',          # 文章内容CSS选择器,必须
        "pub_btn": 'button.cnb-button',   # 发布按钮CSS选择器,必须
        "new_post_url": 'https://i.cnblogs.com/posts/edit',   # 发布文章的URL,必须
        "check_url": 'https://account.cnblogs.com/settings/account',   # 校验Cookies有效(URL是否重定向),必须
        "cookies_url_list": [
            'https://account.cnblogs.com',
            'https://cnblogs.com',
        ],   # Cookies关联URL列表,必须
        'redis_uri': redis_uri,
        'user_info': user_info,
        'cookie_info': cookie_info,
        'log_conf': log_conf,
    },
    {
        "platform": "csdn",             # Blog平台名称,必须
        "has_captcha": False,               # 是否有验证码，有就等待30秒
        'login_url': 'https://passport.csdn.net/login',
        'login_tab': 'div.main-select > ul > li:nth-child(2) > a',   # 登录TAB页面显示
        'ele_login': '#all',      # 用户名
        'ele_pass': '#password-number',       # 密码
        'login_btn': 'button.btn-primary',  # 登录按钮
        "cookies_url_list": [
            'https://csdn.net',
            'https://www.csdn.net',
            'https://passport.csdn.net',
        ],   # Cookies关联URL列表,必须
        "title_id": 'input.article-bar__title',         # 标题内容CSS选择器,必须
        "text_id": 'div.editor',                        # 文章内容CSS选择器,必须
        "pub_btn": 'button.btn-publish',                # 发布按钮CSS选择器,必须
        "new_post_url": 'https://editor.csdn.net/md/',   # 发布文章的URL,必须
        "check_url": 'https://i.csdn.net/',  # 校验Cookies有效(URL是否重定向),必须
        'redis_uri': redis_uri,
        'user_info': user_info,
        'cookie_info': cookie_info,
        'log_conf': log_conf,
    },
    {
        "platform": "oschina",             # Blog平台名称,必须
        "has_captcha": True,               # 是否有验证码，有就等待30秒
        'login_url': 'https://www.oschina.net/home/login',
        'login_tab': 'div.login_account-header > div > div:nth-child(2)',   # 登录TAB页面显示
        'ele_login': 'div.form_item.form_item_account > input.item_input',      # 用户名
        'ele_pass': 'div.form_item form_item_password > input.item_input',       # 密码
        'login_btn': 'button.btn-submit',  # 登录按钮
        "check_url": 'https://my.oschina.net/learnhard/admin/profile',  # 校验Cookies有效(URL是否重定向),必须
        "cookies_url_list": [
            'https://oschina.net',
            'https://www.oschina.net',
            'https://mookie1.com',
            'https://rlcdn.com',
        ],   # Cookies关联URL列表,必须
        "title_id": 'div.two.fields > div >input[type=text]',     # 标题内容CSS选择器,必须
        "text_id": 'div.CodeMirror-lines',                        # 文章内容CSS选择器,必须
        "pub_btn": 'button.btn-publish',                          # 发布按钮CSS选择器,必须
        "new_post_url": 'https://my.oschina.net/learnhard/blog/write',   # 发布文章的URL,必须
        'redis_uri': redis_uri,
        'user_info': user_info,
        'cookie_info': cookie_info,
        'log_conf': log_conf,
    },
    {
        "platform": "jianshu",             # Blog平台名称,必须
        "has_captcha": True,               # 是否有验证码，有就等待30秒
        'login_url': 'https://www.jianshu.com/sign_in',
        'login_tab': None,                    # 登录TAB页面显示
        'ele_login': '#session_email_or_mobile_number',                 # 用户名
        'ele_pass': '#session_password',                                # 密码
        'login_btn': 'button#sign-in-form-submit-btn',                 # 登录按钮
        "check_url": 'https://www.jianshu.com/settings/basic',  # 校验Cookies有效(URL是否重定向),必须
        "cookies_url_list": [
            'https://jianshu.com',
            'https://www.jianshu.com',
        ],   # Cookies关联URL列表,必须
        "title_id": 'div.two.fields > div >input[type=text]',     # 标题内容CSS选择器,必须
        "text_id": 'div.CodeMirror-lines',                        # 文章内容CSS选择器,必须
        "pub_btn": 'button.btn-publish',                          # 发布按钮CSS选择器,必须
        "new_post_url": 'https://my.oschina.net/learnhard/blog/write',   # 发布文章的URL,必须
        'redis_uri': redis_uri,
        'user_info': user_info,
        'cookie_info': cookie_info,
        'log_conf': log_conf,
    },
    {
        "platform": "zhihu",                # Blog平台名称,必须
        "has_captcha": True,               # 是否有验证码，有就等待30秒
        'login_url': 'https://www.zhihu.com/signin',
        'login_tab': 'div.SignFlow-tabs > div:nth-child(2)',            # 登录TAB页面显示
        'ele_login': 'div.SignFlow-account > div > label > input[name=username]',           # 用户名
        'ele_pass': 'div.SignFlow-password > div > label > input[name=password]',           # 密码
        'login_btn': 'button.SignFlow-submitButton',                                      # 登录按钮
        "check_url": 'https://www.zhihu.com/settings/account',          # 校验Cookies有效(URL是否重定向),必须
        "cookies_url_list": [
            'https://zhihu.com',
            'https://www.zhihu.com',
        ],   # Cookies关联URL列表,必须
        "title_id": 'div.two.fields > div >input[type=text]',     # 标题内容CSS选择器,必须
        "text_id": 'div.CodeMirror-lines',                        # 文章内容CSS选择器,必须
        "pub_btn": 'button.btn-publish',                          # 发布按钮CSS选择器,必须
        "new_post_url": 'https://my.oschina.net/learnhard/blog/write',   # 发布文章的URL,必须
        'redis_uri': redis_uri,
        'user_info': user_info,
        'cookie_info': cookie_info,
        'log_conf': log_conf,
    },
    {
        "platform": "segmentfault",             # Blog平台名称,必须
        "has_captcha": False,               # 是否有验证码，有就等待30秒
        'login_url': 'https://segmentfault.com/user/login',
        'login_tab': '#loginDiv > div > div > div > a[data-mode=password]',                 # 登录TAB页面显示
        'ele_login': 'form.password-form > div > input[name=username]',                                # 用户名
        'ele_pass': 'form.password-form > div > input[name=password]',           # 密码
        'login_btn': '#loginDiv > div > form.password-form > button',                       # 登录按钮
        "check_url": 'https://segmentfault.com/user/settings',          # 校验Cookies有效(URL是否重定向),必须
        "cookies_url_list": [
            'https://segmentfault.com',
            'https://sponsor.segmentfault.com',
        ],   # Cookies关联URL列表,必须
        "title_id": 'div.two.fields > div >input[type=text]',     # 标题内容CSS选择器,必须
        "text_id": 'div.CodeMirror-lines',                        # 文章内容CSS选择器,必须
        "pub_btn": 'button.btn-publish',                          # 发布按钮CSS选择器,必须
        "new_post_url": 'https://my.oschina.net/learnhard/blog/write',   # 发布文章的URL,必须
        'redis_uri': redis_uri,
        'user_info': user_info,
        'cookie_info': cookie_info,
        'log_conf': log_conf,
    },
]
#
