#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/26 8:23'
import re

from flask import request, redirect, g

from application import app
from common.libs.LogService import LogService
from common.libs.UrlManager import UrlManager

from common.libs.userService import UserService
from common.models.user import User


@app.before_request
def before_request():
    path = request.path
    ignore_urls = app.config['IGNORE_URLS']
    ignore_check_login_urls = app.config['IGNORE_CHECK_LOGIN_URLS']
    pattern = re.compile("%s" % "|".join(ignore_check_login_urls))

    if pattern.match(path):
        return
    pattern = re.compile("%s" % "|".join(ignore_urls))
    if pattern.match(path):
        return

    if '/api' in path:
        return

    user_info = if_login()
    g.current_user = None
    if user_info:
        g.current_user = user_info
        # 加入日志
        LogService.addAccessLog()
    else:
        return redirect(UrlManager.buildUrl('/user/login'))
    return


def if_login():
    # 判断用户是否登录
    cookie = request.cookies
    auth_cookie = cookie[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookie else None
    if auth_cookie is None:
        return False

    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False

    try:
        user_info = User.query.get_or_404(auth_info[1])
    except Exception:
        return False

    if auth_info[0] != UserService.geneAuthCode(user_info):
        return False

    if user_info.status != 1:
        return False

    return user_info
