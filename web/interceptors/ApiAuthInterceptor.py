#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/26 8:23'
import re

from flask import request, redirect, g, jsonify

from application import app
from common.libs.LogService import LogService
from common.libs.UrlManager import UrlManager
from common.libs.member.memberService import MemberService

from common.models.member.Member import Member


@app.before_request
def before_request():
    api_ignore_urls = app.config['API_IGNORE_URLS']
    path = request.path
    if "/api" not in path:
        return

    pattern = re.compile("%s" % "|".join(api_ignore_urls))
    if pattern.match(path):
        return

    member_info = if_member_login()
    g.member_info = None
    if member_info:
        g.member_info = member_info
    else:
        resp = {'code': -1, 'msg': '未登录~~', 'data': {}}
        return jsonify(resp)
    return


def if_member_login():
    # 判断用户是否登录
    auth_cookie = request.headers.get("Authorization")
    if auth_cookie is None:
        return False

    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False

    try:
        member_info = Member.query.get_or_404(auth_info[1])
    except Exception:
        return False

    if auth_info[0] != MemberService.geneAuthCode(member_info):
        return False

    if member_info.status != 1:
        return False

    return member_info
