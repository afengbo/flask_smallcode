#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/29 20:55'
from application import app
from common.libs.Helper import ops_render
from common.libs.LogService import LogService


@app.errorhandler(404)
def error_404(e):
    print(type(str(e)), str(e))
    LogService.addErrorLog(e)
    return ops_render('error/error.html', {'status': 404, 'msg': "页面飞走了~~"})
