# -*- coding: utf-8 -*-

import os
import toml

__all__ = ["parse_config"]


def parse_config(config_file=os.path.join(os.path.dirname(__file__), "config.toml")):
    """ Parse toml config """
    config_dict = dict()
    try:
        config_dict = toml.load(config_file)
    except Exception as e:
        print("Load toml file error: %s" % e)
    return config_dict
