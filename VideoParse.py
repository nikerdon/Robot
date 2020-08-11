import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')

from gi.repository import Gst, Gtk

Gst.init(None)

class Player(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.connect('destroy', self.quit)
        self.pipeline = Gst.parse_launch("v4l2src device=/dev/video0 ! video/x-raw, width=640, height=480 ! videoconvert ! xvimagesink")

    def run(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        Gtk.main()

    def quit(self, window):
        self.pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit()

        
Player().run()

