#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/03/02 11:07'
import json
import re

from flask import Blueprint, request, jsonify

from application import app
from common.libs.UplodService import UploadService
from common.libs.UrlManager import UrlManager
from common.models.Images import Image

route_upload = Blueprint('upload_page', __name__)


@route_upload.route("/ueditor", methods=["GET", "POST"])
def ueditor():
    req = request.values
    action = req['action'] if 'action' in req else ''

    if action == 'config':
        root_path = app.root_path
        config_path = "%s/web/static/plugins/ueditor/upload_config.json" % root_path
        with open(config_path) as cp:
            try:
                config_data = json.loads(re.sub(r'\/\*.*\*/', '', cp.read()))
            except Exception:
                config_data = {}
        return jsonify(config_data)

    if action == 'uploadimage':
        return upload_image()
    elif action == 'listimage':
        return list_image()


@route_upload.route('/pic', methods=["GET", "POST"])
def upload_pic():
    file_target = request.files
    upload_file = file_target['pic'] if 'pic' in file_target else None
    callback_target = 'window.parent.upload'
    if upload_file is None:
        return "<script type='text/javascript'>%s.error('%s')</script>" % (callback_target, '上传失败')

    ret = UploadService.uploadByFile(upload_file)
    if ret['code'] != 200:
        return "<script type='text/javascript'>%s.error('%s')</script>" % (callback_target, '上传失败' + ret['msg'])
    return "<script type='text/javascript'>%s.success('%s')</script>" % (callback_target, ret['data']['file_key'])


def upload_image():
    resp = {"state": "SUCCESS", "url": "", "title": "", "original": ""}
    file_target = request.files
    upload_file = file_target['upfile'] if 'upfile' in file_target else None
    if upload_file is None:
        resp['state'] = "上传失败"
        return jsonify(resp)

    ret = UploadService.uploadByFile(upload_file)
    if ret['code'] != 200:
        resp['state'] = "上传失败：" + ret['msg']
        return jsonify(resp)

    resp['url'] = UrlManager.buildImageUrl(ret['data']['file_key'])
    return jsonify(resp)


def list_image():
    resp = {"state": "SUCCESS", "list": [], "start": 0, "total": 0}
    req = request.values
    start = int(req['start']) if 'start' in req else 0
    page_size = int(req['size']) if 'size' in req else 20

    query = Image.query
    if start > 0:
        query = query.filter(Image.id < start)

    image_list = query.order_by(Image.id.desc()).limit(page_size).all()
    images = []
    if image_list:
        for image in image_list:
            images.append({'url': UrlManager.buildImageUrl(image.file_key)})
            start = image.id
    resp['list'] = images
    resp['start'] = start
    resp['total'] = len(images)
    return jsonify(resp)
