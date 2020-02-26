#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/26 10:18'
from flask import g, render_template


def ops_render(template, context={}):
    # 统一渲染方法
    if 'current_user' in g:
        context['current_user'] = g.current_user
    return render_template(template, **context)