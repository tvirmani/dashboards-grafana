#!/usr/bin/python
# -*- coding: utf-8 -*-
# Dashboard API service

from flask import Flask, request
from flask import json, jsonify, abort
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta
#from numpyencoder import NumpyEncoder
import os ,sys, json
import logging
import pandas as pd
import numpy as np


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

methods = ('GET', 'POST')
metric_finders= {}
metric_readers = {}
annotation_readers = {}
panel_readers = {}
my_input={}


def add_reader(name, reader):
    metric_readers[name] = reader


def add_finder(name, finder):
    metric_finders[name] = finder


def add_annotation_reader(name, reader):
    annotation_readers[name] = reader


def add_panel_reader(name, reader):
    panel_readers[name] = reader

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

@app.route('/', methods=methods)
def handle_get():
    #if request.method == 'POST':
    #   print (request.headers), (request.get_json())
    #   return 'Hanlding PoST'
    #else:
    return 'Tarun\'s python Grafana datasource, used for rendering HTML panels and timeseries data.'
     
@app.route('/search',methods=['POST'])
def handlesearch():
    targets ={1:'last:30', 2:'last:90', 3:'last:100', 4:'Node4', 5:'Node5'}
    json_string = json.dumps(targets)
    return json_string

    
@app.route('/query', methods=['POST'])
def query():
    req = request.get_json()
    print("---Request JSON Start----")
    print (req,flush=True)
    print("---Request JSON End----")
    print("Dashboard ID and Panel ID")
    print(req['dashboardId'])
    print(req['panelId'])    
    data_type1 = ""
    if req['panelId']==2:
       #my_input = np.array([22,43,83,45,65,88,3,75,34,43,22,43,83,45,65,88,3,75,34,43,22,43,83,45,65,88,3,75,34,43])
       my_input = np.random.randint(low=15, high=100, size=30)
    elif req['panelId']==4:
       #my_input = np.array([43,43,18,35,65,18,3,75,14,43,22,77,83,45,65,88,3,75,34,43,22,43,83,45,65,88,3,55,84,13])
       my_input = np.random.randint(low=15, high=65, size=30)
    elif req['panelId']==6:
       #my_input = np.array([13,3,18,35,15,18,3,9,14,43,22,17,10,35,3,8,3,7,34,43,22,43,13,15,15,18,3,33,35,13])
       my_input = np.random.randint(low=5, high=45, size=30)
    elif req['panelId']==8:
       #my_input = np.array([43,13,18,35,15,18,13,19,14,43,22,17,10,35,3,8,3,7,34,43,22,43,13,15,15,18,3,33,35,13])
       my_input = np.random.randint(low=3, high=30, size=30)
    elif req['panelId']==10 : # id=10
       #my_input = np.array([43,13,18,35,15,18,13,19,14,43,22,17,10,35,3,8,3,7,34,43,22,43,13,15,15,18,3,33,35,13])
       my_input = np.random.randint(low=180, high=630, size=30)
    else:
       #my_input = np.array([43,13,18,35,15,18,13,19,14,43,22,17,10,35,3,8,3,7,34,43,22,43,13,15,15,18,3,33,35,13])
       my_input = np.random.randint(low=40, high=150, size=30)
 
    arr=[int((datetime.now() - timedelta(days=i)).timestamp()*1000) for i in range(30)]
    last_30_days=np.asarray(arr)
    #timestamps=(last_30_days.index.astype(pd.np.int64) // 10**6).values.tolist()    
    #df = df.astype({'col1_int':'float64'
    #1686566420], [322, 1686480020]
    data_type1=[{"target":"last:30","datapoints":list(zip(my_input,last_30_days))}]
    
    
    for target in req['targets']:
      if ':' not in target.get('target', ''):
        abort(404, Exception('Target must be of type: <finder>:<metric_query>, got instead: ' + target['target']))
      else:
        print (target['target'],flush=True)
        print (target['refId'],flush=True)
        print (target['type'],flush=True)
        
      req_type = target.get('type', 'timeserie')
      #data_type1=[{"target":"upper:75","datapoints":[[622,1686550318000],[365,1686550258000]]},{"target":"upper:90","datapoints":[[861,1686550318000],[767,1686550258000]]}]
      json_object=json.dumps(data_type1,cls=NpEncoder,sort_keys=False)
      #sort_keys is used because it was moving some fields in the end of datapoints so 
      #json_object=json.dumps(data_type1)
      print(json_object)
      
      #json_object=json.dumps(data_type1)
      return json_object
      #if data_type == 'timeserie':  
      #   print ("Handle Timeseries")
      #elif data_type == 'table':
      #   print ("Handle Table")

def calculate_datapoints(target):
    app.logger.warning('couchbase')
    return 'Message'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
