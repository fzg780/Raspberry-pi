#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Showcase viewport and hotspot functionality.

Loosely based on poster_demo by @bjerrep
https://github.com/bjerrep/ssd1306/blob/master/examples/poster_demo.py

Needs psutil (+ dependencies) installed::
  $ sudo apt-get install python-dev
  $ sudo pip install psutil
"""

import psutil
import time
from demo_opts import get_device
from luma.core.virtual import viewport, snapshot

from hotspot import memory, uptime, cpu_load, network, disk, WEather,Message



device = get_device()

def position(max):
    forwards = range(0, max)
    backwards = range(max, 0, -1)
    count_load = range(0, 200)
    while True:
        i=0
        for x in forwards:
            yield x
        for x in backwards:
            yield x
        for i in count_load:
            yield 0


def pause_every(interval, generator):
    try:
        while True:
            x = next(generator)
            if x % interval == 0:
                for _ in range(20):
                    yield x
            else:
                yield x
    except StopIteration:
        pass


def intersect(a, b):
    return list(set(a) & set(b))


def first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default


def main():
    if device.rotate in (0, 2):
        # Horizontal
        widget_width = device.width 
        widget_height = device.height
    else:
        # Vertical
        widget_width = device.width
        widget_height = device.height // 2


    # Either function or subclass
    #  cpuload = hotspot(widget_width, widget_height, cpu_load.render)
    #  cpuload = cpu_load.CPU_Load(widget_width, widget_height, interval=1.0)
    mem = snapshot(widget_width, widget_height, memory.render, interval=1)
    dsk = snapshot(widget_width, widget_height, disk.render, interval=1.0)
    cpuload = snapshot(widget_width, widget_height, cpu_load.render, interval=1.0)
    weathers = snapshot(widget_width, widget_height, WEather.render, interval=0.1)
    news = snapshot(widget_width, widget_height, Message.render, interval=60.0)
    


    widgets = [weathers, cpuload,  mem, news, dsk ]


    if device.rotate in (0, 2):
        virtual = viewport(device, width=widget_width * len(widgets), height=widget_height)
        for i, widget in enumerate(widgets):
            virtual.add_hotspot(widget, (i * widget_width, 0))

        for x in pause_every(widget_width, position(widget_width * (len(widgets) - 2))):
            virtual.set_position((x, 0))
            

    else:
        virtual = viewport(device, width=widget_width, height=widget_height * len(widgets))
        for i, widget in enumerate(widgets):
            virtual.add_hotspot(widget, (0, i * widget_height))

        for y in pause_every(widget_height, position(widget_height * (len(widgets) - 2))):
            virtual.set_position((0, y))
    

if __name__ == "__main__":
    try:
        
        main()
    except KeyboardInterrupt:
        pass
