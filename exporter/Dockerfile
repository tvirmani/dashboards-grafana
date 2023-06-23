FROM python:3.11

ADD code /code
RUN pip install -r /code/pip-requirements.txt

# Install software 
RUN apt-get install -y git
RUN apt-get update -y
RUN apt-get install -y iputils-ping
#RUN apt-get install -y openssl
#RUN wget wget https://www.openssl.org/source/openssl-1.1.1o.tar.gz && tar -zxvf openssl-1.1.1o.tar.gz
#RUN sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2.17_amd64.deb
# Clone the conf files into the docker container
RUN git clone https://github.com/couchbase/couchbase-python-client.git
#RUN cd /couchbase-python-client && python -m pip install .

WORKDIR /code
ENV PYTHONPATH '/code/'

CMD ["python" , "/code/exporter.py"]