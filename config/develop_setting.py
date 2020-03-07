#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/24 10:33'

DEBUG = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = "mysql://root:333333@127.0.0.1/food_db?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = 'utf8mb4'

APP = {
    "domain": "https://food.fone.cn"
}

RELEASE_VERSION = '20200307001'
