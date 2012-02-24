#!/bin/sh

wl ap 0
wl passive 1
wl monitor 1
/jffs/usr/bin/wiviz 2>&1 | /jffs/usr/etc/wtm-pollster.lua
