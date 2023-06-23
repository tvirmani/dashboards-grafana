import json
import logging
import csv
from datetime import timedelta

from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions, ClusterTimeoutOptions,QueryOptions
from couchbase.bucket import Bucket
from couchbase.management.queries import (CreatePrimaryQueryIndexOptions,
                                          CreateQueryIndexOptions,
                                          DropPrimaryQueryIndexOptions,
                                          WatchQueryIndexOptions)
from flask import Flask,Response
app = Flask(__name__)

logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
log = logging.getLogger()
log.setLevel(logging.DEBUG)

with open('queries.json', 'r') as f:
  settings = json.load(f)

for options in settings['queries'] + settings["columns"]:
    log.info("Registered metrics collection for {}".format(options['name']))

def get_labels(row, options):
    rename_map = options.get("rename", {})
    return ["{}=\"{}\"".format(rename_map[label] if label in rename_map else label, row[label]) for label in options["labels"]]

def collect_cb(clusters, metrics, options):
    rows = clusters[options["cluster"]].query(options["query"]).rows()
    log.info("Cluster Name {}".format(options["cluster"]))
    log.info("Query Name {}".format(options["query"]))
    
    for row in rows:
        if len(options["labels"]) > 0:
            labels = get_labels(row, options)
            log.info("Label is {}".format(labels))
            metrics.append("{}{{{}}} {}".format(
                options["name"], ",".join(labels), row[options["value_key"]]))
        else:
            metrics.append("{} {}".format(
                options["name"], row[options["value_key"]]))

def collect_csv(metrics, options):
    #csvfile = requests.get(csvs[options["csv"]]).text.splitlines()
       with open(options["csv"]+".csv", mode ='r') as file:   
            reader = csv.DictReader(file)
            for row in reader:
                if options["column"] not in row or row[options["column"]] == "":
                   continue
                if len(options["labels"]) > 0:
                   labels = get_labels(row, options)
                   metrics.append("{}{{{}}} {}".format(
                       options["name"], ",".join(labels), row[options["column"]]))
                else:
                   metrics.append("{} {}".format(
                       options["name"], row[options["column"]]))
@app.route('/')
def hello():
    return 'Hello, World!'
    
@app.route('/metrics')
def metrics():
    metrics = []
    clusters = {}
    log.debug("--Test--")
    for [cluster_name, options] in settings['clusters'].items():
        log.warning("----Details Started----")
        log.warning(cluster_name)
        log.warning(options)
        #log.warning(cluster_name["host"])
        log.warning("----Details Ended----")
        if cluster_name not in clusters:
             try:
                log.debug("--Connecting to Below Cluster with Hard Coded---")
                #log.debug(clusters[cluster_name])
                #static_vms
                #auth = PasswordAuthenticator('Administrator', 'password')
                timeout_opts = ClusterTimeoutOptions(kv_timeout=timedelta(seconds=10),query_timeout=timedelta(seconds=120))
                #cluster = Cluster.connect('couchbase://couchbase-server', ClusterOptions(auth, timeout_options=timeout_opts))
                #clusters[cluster_name] = Cluster.connect('couchbase://couchbase-server',ClusterOptions(PasswordAuthenticator('Administrator', 'password')),timeout_options=timeout_opts)
                #cluster = Cluster('couchbases://{}'.format(endpoint), options)
                #clusters[cluster_name] = Cluster('couchbase://'+options['host'],ClusterOptions(PasswordAuthenticator(options['username'], options['password'])))
                clusters[cluster_name] = Cluster('couchbase://couchbase-server',ClusterOptions(PasswordAuthenticator('Administrator', 'password')),timeout_options=timeout_opts)
             except Exception as e:
                print (e)
                log.warning("Couldn't connect to cluster {}".format(e))
             else:
                #clusters[cluster_name] = Cluster.connect('couchbase://localhost',ClusterOptions(PasswordAuthenticator('Administrator', 'password')),timeout_options=timeout_opts)
                #cb = clusters[cluster_name].bucket("tarun")
                clusters[cluster_name].wait_until_ready(timedelta(seconds=7))
                cb = clusters[cluster_name].bucket("tarun")
                log.debug("--Bucket Set---")
                cb_coll = cb.scope("my_scope").collection("collection1")
                clusters[cluster_name].query_indexes().create_primary_index("tarun",CreatePrimaryQueryIndexOptions(ignore_if_exists=True))
                #clusters[cluster_name] = Cluster('couchbase://'+options['host'],ClusterOptions(PasswordAuthenticator(options['username'], options['password'])))
                inventory_scope = cb.scope('my_scope') 
                log.debug("--Query Set---")
                #sql_query = 'SELECT poolId as `pool`, COUNT(*) AS count FROM tarun group by $1'
                #sql_query = 'SELECT poolId as `pool`, COUNT(*) AS count FROM (SELECT poolId FROM `tarun` WHERE IS_ARRAY(poolId)=FALSE and state='available' UNION ALL SELECT poolId FROM `tarun` UNNEST poolId where `tarun`.state = 'available'  ) AS pools group by poolId'
                #rows = clusters[options["cluster"]].query(options["query"]).rows()
                result=clusters[cluster_name].query("SELECT poolId as `pool` FROM `tarun`.`my_scope`.`collection1` WHERE state=$1","available")
                for row in result.rows():
                  log.debug("Found row: {}".format(row))
                
                #log.debug("Report execution time: {}".format(result.metadata().metrics().execution_time()))
                
                #sql_query = 'SELECT poolId as `pool` FROM `tarun`.`my_scope`.`collection1` WHERE state = $1'
                #row_iter = inventory_scope.query(sql_query,QueryOptions(positional_parameters='available'))
                #for row in row_iter:
                #    log.debug(row)
            #except Exception as e:
                #print(e)
                #log.warning("Couldn't connect to cluster {}".format(e))
                log.debug("Connected to {}".format(options['host']))
    for options in settings["queries"] + settings["columns"]:
        log.debug("Collecting metrics for {}".format(options["name"]))
        try:
            if "cluster" in options:
                log.debug("Found Cluster in Options")
                collect_cb(clusters, metrics, options)
            elif "csv" in options:
                log.debug("Found CSV in Options")
                collect_csv(metrics, options)
            else:
                raise Exception("Invalid type")
        except Exception as e:
            log.warning("Error while collecting {}: {}".format(
                options["name"], e))
    return Response("\n".join(metrics), mimetype="text/plain")
    
if __name__ =='__main__':  
    app.run(debug=True, port=5005, host='0.0.0.0')
    