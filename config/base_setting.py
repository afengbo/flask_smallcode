#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/24 10:33'

SERVER_PORT = 5001
DEBUG = False
SQLALCHEMY_ECHO = False
AUTH_COOKIE_NAME = "mooc_food"

# 过滤URL
IGNORE_URLS = [
    "^/user/login",
    "^/api",
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]

PAGE_SIZE = 20
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    "1": "正常",
    "0": "已删除"
}

ACCESS_COUNT = 5

MINA_APP = {
    'appid': 'wxd6d468b482bfb735',
    'appkey': '4f0c732dbd9891c34062e27437c73fe0'
}
