#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/24 10:35'
from application import app
from web.controllers.index import web_index

app.register_blueprint(web_index, url_prefix="/")
