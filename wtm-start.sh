#!/bin/bash

tcpdump -tt -i wlan0 -e | ./wtm-pollster.py