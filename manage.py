#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/24 10:35'
import sys
import traceback
from application import app, manager
from flask_script import Server

import www

# web server
manager.add_command("runserver", Server(host='0.0.0.0', port=app.config['SERVER_PORT'], use_debugger=True, use_reloader=True))


def main():
    manager.run()


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        traceback.print_exc()
