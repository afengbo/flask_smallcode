# -*- coding: utf-8 -*-
import json

from flask import Blueprint, request, jsonify, make_response, redirect, g

from common.libs.UrlManager import UrlManager
from common.libs.userService import UserService
from common.models.user import User
from application import app, db

from common.libs.Helper import ops_render

route_user = Blueprint('user_page', __name__)


@route_user.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return ops_render("user/login.html")
    ret = {'code': 200, 'msg': "登录成功", 'data': {}}
    req = request.values
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    if login_name is None or len(login_name) < 1:
        ret['code'] = -1
        ret['msg'] = "请输入正确的登录用户名~~"
        return jsonify(ret)

    if login_pwd is None or len(login_pwd) < 1:
        ret['code'] = -1
        ret['msg'] = "请输入正确的登录密码~~"
        return jsonify(ret)

    user_info = User.query.filter_by(login_name=login_name).first()
    if not user_info:
        ret['code'] = -1
        ret['msg'] = "请输入正确的登录用户名和密码~~"
        return jsonify(ret)

    if user_info.login_pwd != UserService.genePwd(login_pwd, user_info.login_salt):
        ret['code'] = -1
        ret['msg'] = "请输入正确的登录用户名和密码~~"
        return jsonify(ret)

    response = make_response(json.dumps(ret))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s#%s"%(UserService.geneAuthCode(user_info), user_info.uid))

    return response


@route_user.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == 'GET':
        return ops_render("user/edit.html", context={'current': 'edit'})
    ret = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''

    if nickname is None or len(nickname) < 1:
        ret['code'] = -1
        ret['msg'] = '请输入符合规范的昵称'
        return jsonify(ret)

    if email is None or len(email) < 1:
        ret['code'] = -1
        ret['msg'] = '请输入符合规范的邮箱'
        return jsonify(ret)

    user_info = g.current_user
    user_info.nickname = nickname
    user_info.email = email
    db.session.add(user_info)
    db.session.commit()

    return jsonify(ret)


@route_user.route("/reset-pwd", methods=["GET", "POST"])
def resetPwd():
    if request.method == "GET":
        return ops_render("user/reset_pwd.html", context={'current': 'reset-pwd'})

    ret = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    old_password = req['old_password'] if 'old_password' in req else ''
    new_password = req['new_password'] if 'new_password' in req else ''

    user_info = g.current_user
    user_info.login_pwd = UserService.genePwd(new_password, user_info.login_salt)
    db.session.add(user_info)
    db.session.commit()

    response = make_response(json.dumps(ret))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s#%s" % (UserService.geneAuthCode(user_info), user_info.uid))

    return response


@route_user.route("/logout")
def logout():
    response = make_response(redirect(UrlManager.buildUrl("/user/login")))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response
