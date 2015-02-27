# -*- coding: utf-8 -*-

import re
from ConfigParser import ConfigParser

config = ConfigParser()
config.read('config.ini')


def get_start_url():
    return config.get('base', 'start')


def fetch_all_urls(html):
    pattern = config.get('pattern', 'url')
    return re.findall(pattern, html)