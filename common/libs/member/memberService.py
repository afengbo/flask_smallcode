#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/25 11:31'

import hashlib, base64
import json
import random
import string

import requests

from application import app


class MemberService():
    @staticmethod
    def geneAuthCode(member_info):
        m = hashlib.md5()
        str = "%s-%s-%s" % (member_info.id, member_info.salt, member_info.status)
        m.update(str.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def geneSalt(length=16):
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return "".join(keylist)

    @staticmethod
    def getWeChatOpenId(code):
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' \
              % (app.config['MINA_APP']['appid'], app.config['MINA_APP']['appkey'], code)
        r = requests.get(url).text
        res = json.loads(r)
        openid = None
        if 'openid' in res:
            openid = res['openid']
        return openid
