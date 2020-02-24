#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/24 11:41'

from flask import Blueprint

web_index = Blueprint("web_index", __name__)


@web_index.route("/")
def index():
    return "Index."
