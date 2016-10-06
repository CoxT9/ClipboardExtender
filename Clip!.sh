#!/bin/bash

[ -e /opt/clipboard_main.py ] || mv ./clipboard_main.py /opt/clipboard_main.py
nohup python /opt/clipboard_main.py &