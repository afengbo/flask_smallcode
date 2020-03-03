#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/23 16:38'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from imooc import imooc_bp
from sqlalchemy import text

from test_first.common import UrlManager

app = Flask(__name__)
app.register_blueprint(imooc_bp, url_prefix='/imooc')

# 连接mysql数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:333333@127.0.0.1/mysql'
db = SQLAlchemy(app)


@app.route('/')
def index():
    sql = text('select * from `user`')
    res = db.engine.execute(sql)
    for r in res:
        app.logger.info(r)
    su = UrlManager.buildStaticUrl("/api")
    return "Index." + su


@app.route('/hello')
def hello_world():
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 3)
    app.logger.error('An error occurred')
    return "Hello World!"


@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return 'This page does not exist', 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
