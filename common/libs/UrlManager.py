# -*- coding: utf-8 -*-

class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl( path ):
        return path

    @staticmethod
    def buildStaticUrl(path):
        path =  "/static" + path
        return UrlManager.buildUrl( path )