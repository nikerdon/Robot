import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject
import time

Gst.init(None)

resolution = (640, 480)
framerate = 30

width = resolution[0]
height = resolution[1]      

pipeline = Gst.Pipeline()

v4l2src = Gst.ElementFactory.make('v4l2src')
v4l2src.set_property('device', '/dev/video0')

capsfil = Gst.ElementFactory.make('capsfilter')
videoCaps = Gst.caps_from_string('video/x-raw, width=%d, height=%d, framerate=%d/1' %
                               (width, height, framerate))
capsfil.set_property('caps', videoCaps)

videocon = Gst.ElementFactory.make('videoconvert')
videosink = Gst.ElementFactory.make('autovideosink')

elemlist = [v4l2src, capsfil, videocon, videosink]
for elem in elemlist:
    pipeline.add(elem)

v4l2src.link(capsfil)
capsfil.link(videocon)
videocon.link(videosink)

pipeline.set_state(Gst.State.PLAYING)

