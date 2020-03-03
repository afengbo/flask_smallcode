#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/24 9:12'

class UrlManager:
    @staticmethod
    def buildUrl(path):
        return path

    @staticmethod
    def buildStaticUrl(path):
        path = path + "?ver=" + "20200224"
        return UrlManager.buildUrl(path)
