#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Simple println capabilities.
"""

import requests
import os
import time
from bs4 import BeautifulSoup
from demo_opts import get_device
from luma.core.virtual import terminal
from PIL import ImageFont
import Test3


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)

#arrays = []


def render(draw, width, height):
    device = Test3.device
    arrays = []
    #global arrays
    #arrays.clear()
    res = requests.get('http://news.sina.com.cn/china/')
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    for news in soup.select('.news-2'):
        i=0
        for li_data in news.select('li'):
            li = news.select('li')[i].text
            arrays.append(li)
            i +=1
            
            
            
            
            

    font = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",16)
    term = terminal(device, font)
    for data in arrays:
        term.println(">>"+data)
        time.sleep(2)
   
           




