#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 12:13:43 2022

@author: steven
"""

import os
from pathlib import Path
from io import BytesIO
import requests

from flask import Flask, request, send_file
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

SHOM_FOLDER = 'data/SHOM' 

def create_if_path_not_exist(path):
    path_lib = Path(path)
    folders_to_create = []
    if not os.path.isdir(path):
        folders_to_create.append(path)

    for parent in path_lib.parents:
        if not os.path.isdir(parent):
            folders_to_create.append(parent)
        else:
            break
    # print('Will create folders', folders_to_create[::-1])
    for folder in folders_to_create[::-1]:
        os.mkdir(folder)
    

create_if_path_not_exist('data')
create_if_path_not_exist(SHOM_FOLDER)


@app.route("/wmts/shom")
def shom_wmts():
    params = request.args

    file_name = f"SHOM-{params['TileMatrix']}-{params['TileRow']}-{params['TileCol']}.png"
    # create_if_path_not_exist(os.path.join(*[SHOM_FOLDER, params['TileMatrix']]))
    # create_if_path_not_exist(os.path.join(*[SHOM_FOLDER, params['TileMatrix'], params['TileRow']]))
    create_if_path_not_exist(os.path.join(*[SHOM_FOLDER, params['TileMatrix'], params['TileRow']]))
    file_path = os.path.join(*[SHOM_FOLDER, params['TileMatrix'], params['TileRow'], file_name])
    # Finding cache
    if os.path.isfile(file_path):
        # with open(file_path, 'rb') as stream:
        #     print('Using cache!')
        return send_file(file_path, mimetype='image/png')

    # print('route params', params)
    # params = {'layer': 'RASTER_MARINE_3857_WMTS',
    #           'style': 'normal',
    #           'Service': 'WMTS'}
    print('Missing tile, fetching from internet')
    headers = {'Referer': 'https://data.shom.fr'}
    req = requests.get('https://services.data.shom.fr/clevisu/wmts',
                       params=params,
                       headers=headers)
    # ?&&tilematrixset=3857&Request=GetTile&Version=1.0.0&Format=image/png&TileMatrix=7&TileCol=63&TileRow=44
    if req.status_code == 200:
        img = req.content
        with open(file_path, 'wb') as file:
            file.write(img)

        stream = BytesIO()
        stream.write(img)
        stream.seek(0)

        
        return send_file(stream, mimetype='image/png')

    return req.text, req.status_code


