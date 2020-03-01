#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/03/01 9:46'
from flask import request, jsonify

from common.libs.Helper import get_current_time
from common.libs.member.memberService import MemberService
from common.models.member.Member import Member
from common.models.member.OauthMemberBind import OauthMemberBind
from web.controllers.api import route_api
from application import db, app


@route_api.route('/member/login', methods=["GET", "POST"])
def login():
    ret = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        ret['code'] = -1
        ret['msg'] = '非法传值'
        return jsonify(ret)

    openid = MemberService.getWeChatOpenId(code)
    if openid is None:
        ret['code'] = -1
        ret['msg'] = '调用微信出错'
        return jsonify(ret)

    # 判断是否已经绑定
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        nickname = req['nickName'] if 'nickName' in req else ''
        sex = req['gender'] if 'gender' in req else 0
        avatar = req['avatarUrl'] if 'avatarUrl' in req else ''
        member_obj = Member()
        member_obj.nickname = nickname
        member_obj.sex = sex
        member_obj.avatar = avatar
        member_obj.salt = MemberService.geneSalt()
        member_obj.created_time = member_obj.updated_time = get_current_time()
        db.session.add(member_obj)
        db.session.commit()

        bind_obj = OauthMemberBind()
        bind_obj.member_id = member_obj.id
        bind_obj.type = 1
        bind_obj.openid = openid
        bind_obj.extra = ''
        bind_obj.created_time = bind_obj.updated_time = get_current_time()
        db.session.add(bind_obj)
        db.session.commit()

        bind_info = bind_obj

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    ret['data'] = {'token': token}
    return jsonify(ret)

@route_api.route('/member/check-reg', methods=["GET", "POST"])
def checkReg():
    ret = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        ret['code'] = -1
        ret['msg'] = '非法传值'
        return jsonify(ret)

    openid = MemberService.getWeChatOpenId(code)
    if openid is None:
        ret['code'] = -1
        ret['msg'] = '调用微信出错'
        return jsonify(ret)

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        ret['code'] = -1
        ret['msg'] = '未绑定'
        return jsonify(ret)

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    if not member_info:
        ret['code'] = -1
        ret['msg'] = '未查询到绑定信息'
        return jsonify(ret)

    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    ret['data'] = {'token': token}
    return jsonify(ret)
