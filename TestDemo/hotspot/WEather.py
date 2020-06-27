#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
An analog clockface with date & time.

Ported from:
https://gist.github.com/TheRayTracer/dd12c498e3ecb9b8b47f#file-clock-py
"""

import math
import time
import datetime
from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont
import urllib.request as r
import json


    

def posn(angle, arm_length):
    dx = int(math.cos(math.radians(angle)) * arm_length)
    dy = int(math.sin(math.radians(angle)) * arm_length)
    return (dx, dy)


def getUrlData(url):
    try:
        data = r.urlopen(url).read().decode('utf-8')
        data = json.loads(data)
    except Exception as e:
        print("????")
        data={"results":[{"location":{"id":"WX4FBXXFKE4F","name":u"常州","country":"CN","path":"常州,江苏,中国","timezone":"Asia/Shanghai","timezone_offset":"+08:00"},\
        "now":{"text":u"无网络","code":"0","temperature":"null"},"last_update":"2020-xx-xxTxx:xx:08+08:00"}]}
        return data
    else:
        return data

data = None
temp = None
temp1 = None
count = 1201
def render(draw, width, height):
    global count,data,temp,temp1
    today_last_time = "Unknown"
    url = r'https://api.seniverse.com/v3/weather/now.json?key=SWuIGNXNNNZJWC2dp&location=changzhou&language=zh-Hans&unit=c'
    font = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",14)
    #font1 = ImageFont.truetype("/usr/test/luma.examples-master/examples/fonts/TRANA___.TTF",12)
    
    now = datetime.datetime.now()
    today_date = now.strftime("%d %b %y")
    today_time = now.strftime("%H:%M:%S")    
        
    if count >= 1200:
        count = 0
        
        data=getUrlData(url)
        
        #pprint.pprint(data)

        temp = data['results'][0]['location']
        temp1= data['results'][0]['now']
            #time.sleep(2)
    count +=1
    #print("count:"+str(count))
        
        
        
        
        
    if today_time != today_last_time:
        today_last_time = today_time
        now = datetime.datetime.now()
        today_date = now.strftime("%d %b %y")

        margin = 4

        cx = 30
        cy = min(height, 64) / 2

        left = cx - cy
        right = cx + cy

        hrs_angle = 270 + (30 * (now.hour + (now.minute / 60.0)))
        hrs = posn(hrs_angle, cy - margin - 7)

        min_angle = 270 + (6 * now.minute)
        mins = posn(min_angle, cy - margin - 2)

        sec_angle = 270 + (6 * now.second)
        secs = posn(sec_angle, cy - margin - 2)

        draw.ellipse((left + margin, margin, right - margin, min(height, 64) - margin), outline="white")
        draw.line((cx, cy, cx + hrs[0], cy + hrs[1]), fill="white")
        draw.line((cx, cy, cx + mins[0], cy + mins[1]), fill="white")
        draw.line((cx, cy, cx + secs[0], cy + secs[1]), fill="red")
        draw.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill="white", outline="white")
        draw.text((2 * (cx + margin), cy - 8+20), today_date,  fill="yellow")
        draw.text((2 * (cx + margin), cy+20), today_time,  fill="yellow")
        draw.text((2 * (cx + margin), 0), temp['name']+":", font=font,fill="white")
        draw.text((2 * (cx + margin)+10, 16), temp1['text'], font=font,fill="white")
        draw.text((2 * (cx + margin)+10, 32), temp1['temperature']+'℃', font=font,fill="white")
   


