#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Xia Bin
# 
# Author:     Xia Bin <xiabin@linuxdeepin.com>
# Maintainer: Xia Bin <xiabin@linuxdeepin.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk
import gobject
from timeline import Timeline, CURVE_SINE

class HSlider(gtk.Viewport):
    __gsignals__ = {
            "completed_slide" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
            }
    def __init__(self, slide_time=200):
        gtk.Viewport.__init__(self)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.fixed = gtk.Fixed()
        self.add(self.fixed)
        self.slide_time = slide_time
        self.pre_widget = None
        self.active_widget = None
        self.connect("realize", self._update_size)
        self.connect("size_allocate", self._update_size)
        self.page_width = 0
        self.page_height = 0
        self.in_sliding = False


    def _update_size(self, w=None, _w=None):
        self.page_width = self.allocation.width
        self.page_height = self.allocation.height
        if self.active_widget:
            self.active_widget.set_size_request(self.page_width, self.page_height)
        if self.pre_widget:
            self.pre_widget.set_size_request(self.page_width, self.page_height)
        self.show_all()

    def _to_right(self, percent):
        self.offset = int(round(percent * self.page_width)) 
        
        if self.pre_widget:
            self.fixed.move(self.pre_widget, - self.offset, 0)
        
        self.fixed.move(self.active_widget, self.page_width - self.offset, 0)
    def _to_left(self, percent):
        self.offset = int(round(percent * self.page_width))
        
        if self.pre_widget:
            self.fixed.move(self.pre_widget, self.offset, 0)
        
        self.fixed.move(self.active_widget, self.offset - self.page_width, 0)

    def _no_effect(self):
        self.offset = self.page_width

        if self.pre_widget:
            self.fixed.remove(self.pre_widget)
        self.fixed.move(self.active_widget, 0, 0)

    def to_page(self, w, direction):
        if self.in_sliding:
            #TODO:  animation should continue in according to previous status. this can be done to record offset in 
            #self.timeline.stop()
            #self.timeline.emit("completed")
            return
        #self.to_page_now(w)
        if w != self.active_widget:
            w.set_size_request(self.page_width, self.page_height)
            if w.parent != self.fixed:
                self.fixed.put(w, self.page_width, 0)
            self.active_widget = w

            self.timeline = Timeline(self.slide_time, CURVE_SINE)
            if direction == "right":
                self.timeline.connect('update', lambda source, status: self._to_right(status))
            elif direction == "left":
                self.timeline.connect('update', lambda source, status: self._to_left(status))
            else:
                self._no_effect()

            self.timeline.connect("completed", lambda source: self._completed())
            self.timeline.run()
            self.in_sliding = True

            self.show_all()

    def _completed(self):
        if self.pre_widget and self.pre_widget.parent == self.fixed:
            self.fixed.remove(self.pre_widget)
        self.pre_widget = self.active_widget
        #print "Pre: " +  str(self.pre_widget)  + "  act: " + str(self.active_widget) + "children: " + str(self.get_children())
        self.show_all()
        self.in_sliding = False
        self.emit("completed_slide")

    def to_page_now(self, w, d=None):
        '''
        if self.pre_widget:
            self.fixed.remove(self.pre_widget)
        self.active_widget = w
        self.pre_widget = self.active_widget

        if self.get_realized():
            w.set_size_request(self.allocation.width, self.allocation.height)
            self.show_all()
        self.fixed.add(w)
        '''
        self.to_page(w, d)



    def slide_to_page(self, w, d):
        #raise Warning("use to_page and to_page_now instead of slide_to_page/set_to_page.")
        self.to_page(w, d)
    def set_to_page(self, w):
        #raise Warning("use to_page and to_page_now instead of slide_to_page/set_to_page.")
        self.to_page_now(w)
    def append_page(self, w):
        #Warning("slider didn't need this method..")
        pass


gobject.type_register(HSlider)



if __name__ == "__main__":
    s = HSlider()

    w = gtk.Window()
    w.set_size_request(300, 300)
    h = gtk.HBox()
    w1 = gtk.Button("Widget 1")
    w2 = gtk.Button("Widget 2")

    s.to_page_now(w1)

    b = gtk.Button("to1")
    b.connect("clicked", lambda w: s.to_page(w1, "right" ))
    h.add(b)

    b = gtk.Button("to2")
    b.connect("clicked", lambda w: s.to_page(w2, "left"))
    h.add(b)

    v = gtk.VBox()
    v.add(h)
    v.add(s)

    w.add(v)
    w.show_all()

    w.connect("destroy", gtk.main_quit)

    gtk.main()
