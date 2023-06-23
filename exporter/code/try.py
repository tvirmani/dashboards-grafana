import json
import logging
from datetime import timedelta

from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions, ClusterTimeoutOptions,QueryOptions
from couchbase.bucket import Bucket

timeout_opts = ClusterTimeoutOptions(kv_timeout=timedelta(seconds=10),query_timeout=timedelta(seconds=120))
#cluster = Cluster.connect('couchbase://couchbase-server', ClusterOptions(auth, timeout_options=timeout_opts))
try:
    hello = Cluster('couchbase://localhost',ClusterOptions(PasswordAuthenticator('Administrator', 'password')),timeout_options=timeout_opts)
except Exception as e:
    print (e)
else:
    bucket = hello.bucket("tarun")
    cb_coll = bucket.scope("my_scope").collection("collection1")
#hello.query_indexes().create_primary_index("tarun",CreatePrimaryQueryIndexOptions(ignore_if_exists=True))
    result=hello.query("SELECT poolId as `pool` FROM `tarun`.`my_scope`.`collection1` WHERE state=$1","available")
    for row in result.rows():
        print("Found row: {}".format(row))



