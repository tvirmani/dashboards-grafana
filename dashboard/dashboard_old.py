# Dashboard API service
from flask import Flask, request, json
app = Flask(__name__)
  
@app.route("/query", methods=['POST'])
def query():
    for target in request.json['targets']:
        #print(target[1])
        data_type = target['type']
        if data_type == "timeseries":
           datapoints = calculate_datapoints(target)
        elif data_type == "table":
           datapoints = calculate_rows_and_columns(target)
           
    return "Message"  
           
def calculate_datapoints(target):
    if target['source'] == "couchbase":
      print ("Hello couchbase!")
    elif target['source'] == "json":
      print ("Hello json!")
    elif target['source'] == "csv":
      print ("Hello csv!")
      
    return "Message"
if __name__ == '__main__':
    app.run()