#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
from tornado.options import define
from tornado.options import options
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler

from tornado_web.web import TWApplication
from tornado_web.routers import router_urls


_the_path = os.path.dirname(__file__)

define("port", type=int, default=9527, help="tornado server listened on the given port.")
define("debug", type=bool, default=False, help="tornado server running mode.")


def usage():
    _usage = """\
tornado server running with:
    debug: {}
    port: {}
tornado server start...""".format(options.debug, options.port)
    print(_usage)

if __name__ == '__main__':
    options.parse_command_line()

    usage()

    static_path = os.path.join(_the_path, "tornado_web/static")
    config_file = os.path.join(_the_path, 'config.conf')
    print(config_file)
    print(static_path)
    router_urls += [(r"/favicon.ico", StaticFileHandler, dict(path=static_path)), ]

    app = TWApplication(config_file,
                        handlers=router_urls,
                        gzip=True,
                        xheaders=True,
                        static_path=static_path,
                        debug=options.debug)

    http_server = HTTPServer(app)
    http_server.listen(options.port)
    IOLoop.instance().start()