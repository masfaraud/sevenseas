#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 12:12:56 2022

@author: steven
"""

from sevenseas_backend import app

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"