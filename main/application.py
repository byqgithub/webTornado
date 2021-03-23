# -*- coding: utf-8 -*-

import os
import tornado.log
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options, define_logging_options

from unattend.config import parse_config


class MainHandler(tornado.web.RequestHandler):
    """ main handler """
    def get(self):
        self.write("Hello world !")


def command_options():
    """ Define web cmd line option """
    define("port", default=8888, help="run on the given port", type=int)
    config_file = os.path.join(os.path.dirname(__file__), "..", "config", "config.toml")
    define("config", default=config_file, help="", type=str)


def setting_log_config(config):
    """  """
    options.logging = config.get("log_level")
    options.log_file_prefix = config.get("log_file_path")
    options.log_file_max_size = int(config.get("max_size")) * 1024 * 1024
    options.log_file_num_backups = int(config.get("backupCount"))
    options.log_rotate_when = config.get("when")
    options.log_rotate_interval = config.get("interval")
    options.log_rotate_mode = config.get("rotate_mode")
    # tornado.log.enable_pretty_logging(options)
    define_logging_options(options)


def setting_server_config(config):
    """ tornado server 相关参数 """
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "..", config.get("template_path", "templates")),
        static_path=os.path.join(os.path.dirname(__file__), "..", config.get("static_path", "static")),
        compress_response=config.get('compress_response', True),
        xsrf_cookies=config.get('xsrf_cookies', True),
        cookie_secret=config.get('cookie_secret', ""),
        login_url=config.get('login_url', ""),
        debug=config.get('debug', False),
        default_handler_class=BaseHandler,
    )
    return settings


def setting_config():
    """  """
    command_options()
    options.parse_command_line()
    config_file = options.config
    config_dict = parse_config(config_file)
    setting_log_config(config_dict.get("log"))
    setting_server_config(config_dict.get("general"))


if __name__ == "__main__":
    setting_config()
    options.parse_command_line()
    application = tornado.web.Application(handlers=[(r"/", MainHandler)])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
