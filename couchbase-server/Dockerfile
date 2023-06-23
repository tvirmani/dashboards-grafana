FROM couchbase/server:latest AS stage_base
# FROM couchbase:latest AS stage_base 
COPY init-cbserver.sh /opt/couchbase/init/
RUN chmod 777 /opt/couchbase/init/init-cbserver.sh
COPY sample-data.json /opt/couchbase/init/
RUN apt-get update && \
    apt-get install dos2unix && \
    apt-get clean
RUN dos2unix /opt/couchbase/init/init-cbserver.sh