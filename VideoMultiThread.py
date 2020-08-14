import svgwrite
import gi
import time
import threading
import sys
import numpy as np
import os
from PIL import ImageFont

gi.require_version('Gst', '1.0')

from gi.repository import Gst

Gst.init(None)

W = 640
H = 480
NAME = 'Христарождественский П.А. г. Комсомольск-на-Амуре'
COLOR = 'lime'
FONT = 'Ubuntu-R'
FSIZE = '18px'
TIMER_SEC = 10

font = ImageFont.truetype("Ubuntu-R.ttf", 20)
size = font.getsize(NAME)
a = str(size)
b = ''
for i in range(len(a)):
    c = a[i]
    if c.isdigit():
        b = b + a[i]
    if a[i] == ' ':
        break
l = int(b)


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
        i = 0
        while True:
            overlay = self.pipeline.get_by_name('overlay')
            svg_canvas = svgwrite.Drawing('test.svg', size=(W, H))

            if p <= 3:
                svg_canvas.add(svg_canvas.text('Go! Go! Go!',insert = (W/2-120,H/2-90), font_size = '40px', fill = 'red', font_family = FONT))
                
            if p>3 and TIMER_SEC >= p:
                svg_canvas.add(svg_canvas.line((W/2,H/2-50), (W/2,H/2-15), stroke='red', stroke_width='7'))
                svg_canvas.add(svg_canvas.line((W/2,H/2+15), (W/2,H/2+50), stroke='red', stroke_width='7'))
                svg_canvas.add(svg_canvas.line((W/2-50,H/2), (W/2-15,H/2), stroke='red', stroke_width='7'))
                svg_canvas.add(svg_canvas.line((W/2+15,H/2), (W/2+50,H/2), stroke='red', stroke_width='7')) 
            
            svg_canvas.add(svg_canvas.rect(((W-l)/2-5, H-30), (l+10,28), stroke='black', fill='black', fill_opacity='0.5'))
         
            svg_canvas.add(svg_canvas.text('Battery: 100%', insert=(W-140, 20), font_size= FSIZE, fill = COLOR, font_family = FONT))
            
            svg_canvas.add(svg_canvas.rect((W-140,30), (120-i,30), stroke='black', fill='black', fill_opacity='0.5'))
            #i += 10
            svg_canvas.add(svg_canvas.text('3 выстрела', insert=(15, 20), font_size= FSIZE, fill = COLOR, font_family = FONT))
            svg_canvas.add(svg_canvas.text(NAME, insert = ((W-l)/2, H-10), font_size = FSIZE, fill = COLOR, font_family = FONT))

            MIN = (TIMER_SEC - p) // 60
            SEC = (TIMER_SEC - p) % 60
                        
            if TIMER_SEC >= p + 10 and SEC >= 10:
                svg_canvas.add(svg_canvas.text(str(MIN) + ':' + str(SEC),insert = (W/2-20,20), font_size = FSIZE, fill = COLOR, font_family = FONT))
            if SEC < 10 and MIN >= 0:
                svg_canvas.add(svg_canvas.text(str(MIN) + ':0' + str(SEC),insert = (W/2-20,20), font_size = FSIZE, fill = COLOR, font_family = FONT))
            if TIMER_SEC < p:
                svg_canvas.add(svg_canvas.text('GAME OVER',insert = (W/2-124,H/2-90), font_size = '40px', fill = 'red', font_family = FONT))
            overlay.set_property('data', svg_canvas.tostring())

            p += 1
            time.sleep(1)

Player().run()
try:   
    while True:
        time.sleep(1)
        
except (KeyboardInterrupt):
    Player().stop()
          

