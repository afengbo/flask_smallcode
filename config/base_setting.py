#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/24 10:33'

SERVER_PORT = 5001
DEBUG = False
SQLALCHEMY_ECHO = False
AUTH_COOKIE_NAME = "mooc_food"

# 过滤URL
IGNORE_URLS = [
    "^/user/login"
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
