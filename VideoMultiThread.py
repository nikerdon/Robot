import svgwrite
import gi
import time
import threading
import sys
import numpy as np
import os

gi.require_version('Gst', '1.0')

from gi.repository import Gst

Gst.init(None)

W = 640
H = 480

class Player():
    def __init__(self):
        self.pipeline = Gst.parse_launch("v4l2src device=/dev/video0 ! video/x-raw, width=640, height=480 ! videoconvert ! rsvgoverlay name=overlay ! videoconvert ! xvimagesink alsasrc device=plughw:CARD=2,DEV=0 ! audioconvert ! autoaudiosink")
        self.thread = MyThread(self.pipeline)
        self.thread.start()     
        
    def run(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        
    def stop(self):
        self.pipeline.set_state(Gst.State.NULL)
        os.abort()

class MyThread(threading.Thread):
    def __init__(self, pipeline):
        threading.Thread.__init__(self)
        self.pipeline = pipeline
                
    def run(self):
        p = 0
        n = 0
        while True:
            overlay = self.pipeline.get_by_name('overlay')
            svg_canvas = svgwrite.Drawing('test.svg', size=(W, H))
            path = [(W/2+n, H/2),(W/2+n-100, H/2),(W/2+n-100, H/2-100),(W/2+n, H/2-100)]
            sq = svg_canvas.add(svg_canvas.polygon(path, id='polygon', stroke='black', fill='black'))
            overlay.set_property('data', svg_canvas.tostring())

            p += 1
            n = 20 * np.sin(p)
            time.sleep(1)

Player().run()
try:   
    while True:
        time.sleep(1)
        
except (KeyboardInterrupt):
    Player().stop()
          

