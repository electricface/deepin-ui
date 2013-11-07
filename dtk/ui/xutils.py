#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Wang Yong
# 
# Author:     Wang Yong <lazycat.manatee@gmail.com>
# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
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

from Xlib import Xatom, display

xlib_display = None

def init_xlib():
    global xlib_display
    
    if xlib_display == None:
        xlib_display =  display.Display()
        
def get_window_by_id(win_id):
    global xlib_display
    init_xlib()
        
    return xlib_display.create_resource_object("window", win_id)

def set_window_property(xwindow, property_type, property_content):
    global xlib_display
    init_xlib()
        
    xwindow.change_property(
        xlib_display.get_atom(property_type),
        Xatom.STRING,
        8,
        property_content,
        )    
    xlib_display.sync()
    
def get_window_property(xwindow, property_type):
    global xlib_display
    init_xlib()
        
    try:
        return xwindow.get_full_property(
            xlib_display.get_atom(property_type),
            Xatom.STRING
            ).value
    except:
        return None

def set_window_property_by_id(window_id, property_type, property_content):
    global xlib_display
    init_xlib()

    set_window_property(get_window_by_id(window_id), property_type, property_content)
    
def get_window_property_by_id(window_id, property_type):
    global xlib_display
    init_xlib()

    return get_window_property(get_window_by_id(window_id), property_type)
