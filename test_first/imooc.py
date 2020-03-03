#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/24 8:43'

from flask import Blueprint

imooc_bp = Blueprint("imooc_page", __name__)


@imooc_bp.route("/")
def index():
    return "imooc index"


@imooc_bp.route("/hello")
def hello():
    return "imooc hello world"
