#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from flask import Flask, request, session, redirect, url_for, render_template, g
from server import *

if __name__ == '__main__':
	Watcher()
	monitor = threading.Thread(target=check)
	monitor.start()
	app.run(host='0.0.0.0',debug=True)	