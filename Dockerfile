FROM ubuntu:16.04

RUN apt-get update && apt-get -y install python-pip
RUN echo  "pyhton pip finish======================="
RUN apt-get -y install build-essential
RUN echo  "build-essential finish======================="
RUN apt-get install python3-dev libssl-dev libgmp-dev 
RUN echo  "lib-dev finish======================="
RUN add-apt-repository ppa:jonathonf/python-3.6 && apt-get update && apt-get -y install python3.6
RUN echo  "python finish======================="
RUN pip install flask==1.0.2
RUN pip install msgpack-python==0.5.6
RUN echo  "finish======================="


COPY . /usr/bin

WORKDIR /usr/bin

EXPOSE 5000

CMD ["python", "./app.py"]

#docker build -t reencryption . 
