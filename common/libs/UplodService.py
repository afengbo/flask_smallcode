#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/03/02 14:49'
import os, stat
import uuid

from werkzeug.utils import secure_filename
from application import app, db
from common.libs.Helper import get_current_time
from common.models.Images import Image


class UploadService():
    @staticmethod
    def uploadByFile(file):
        config_upload = app.config['UPLOAD']
        ret = {"code": 200, "msg": "操作成功", "data": {}}
        filename = secure_filename(file.filename)
        ext = filename.rsplit(".", 1)[1]
        if ext not in config_upload['ext']:
            ret['code'] = -1
            ret['msg'] = "不允许的扩展类型未见"
            return ret

        root_path = app.root_path + config_upload['prefix_path']
        file_dir = get_current_time("%Y%m%d")
        save_dir = root_path + file_dir
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
            os.chmod(save_dir, stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)

        file_name = str(uuid.uuid4()).replace('-', '') + '.' + ext
        file.save("%s/%s" % (save_dir, file_name))

        model_image = Image()
        model_image.file_key = file_dir + '/' + file_name
        model_image.created_time = get_current_time()
        db.session.add(model_image)
        db.session.commit()

        ret['data'] = {
            'file_key': file_dir + "/" + file_name
        }
        return ret
