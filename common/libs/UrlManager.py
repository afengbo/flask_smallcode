# -*- coding: utf-8 -*-
import time

from application import app


class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl( path ):
        return path

    @staticmethod
    def buildStaticUrl(path):
        release_version = app.config.get("RELEASE_VERSION")
        ver = release_version if release_version else str(time.time())
        path =  "/static" + path + "?ver=" + ver
        return UrlManager.buildUrl( path )