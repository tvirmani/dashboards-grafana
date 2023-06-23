import json
import logging
from datetime import timedelta
import csv

metrics = []
clusters = {}

with open('queries.json', 'r') as f:
  settings = json.load(f)

def get_labels(row, options):
    rename_map = options.get("rename", {})
    return ["{}=\"{}\"".format(rename_map[label] if label in rename_map else label, row[label]) for label in options["labels"]]
    
for options in settings['queries'] + settings["columns"]:
    print("Registered metrics collection for {}".format(options['name']))
    print("setting[queries] = {}".format(settings['queries']))
    print("setting[columns] = {}".format(settings['columns']))


for [cluster_name, options] in settings['clusters'].items():
  for options in settings["queries"] + settings["columns"]:
      if "csv" in options:
       print("CSV NAME --{}".format(options["csv"]))
       with open(options["csv"]+".csv", mode ='r') as file:   
            reader = csv.DictReader(file)
            for row in reader:
                if options["column"] not in row or row[options["column"]] == "":
                   continue
                if len(options["labels"]) > 0:
                   labels = get_labels(row, options)
                   metrics.append("{}{{{}}} {}".format(options["name"], ",".join(labels), row[options["column"]]))
                   print(metrics)
                else:
                   metrics.append("{} {}".format(options["name"], row[options["column"]]))
                   print(metrics)
