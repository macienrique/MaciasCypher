FROM ubuntu:16.04

RUN apt-get update && apt-get -y install python-pip
RUN echo  "pyhton pip finish======================="
RUN apt-get -y install build-essential
RUN echo  "build-essential finish======================="
RUN apt-get install -y python3-dev libssl-dev libgmp-dev 
RUN echo  "lib-dev finish======================="
RUN apt-get -y install checkinstall
RUN echo  "checkinstall finish ======================="
RUN apt-get -y install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
RUN echo  "libreadline finish======================="
RUN apt-get update && apt-get -y install wget
RUN echo  "wget finish======================="
RUN wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tar.xz
RUN tar xvf Python-3.6.0.tar.xz
RUN cd /Python-3.6.0/
RUN ls -al
RUN /Python-3.6.0/./configure
RUN make altinstall
RUN echo  "python finish======================="
RUN apt-get update && apt-get -y install python3-pip
RUN echo  "python finish======================="
RUN pip3 install flask==1.0.2
RUN pip3 install msgpack-python==0.5.6
RUN echo  "finish======================="
RUN python3 -V

COPY . /usr/bin

WORKDIR /usr/bin

EXPOSE 5000

CMD ["python3", "./app.py"]

# docker build -t us.gcr.io/everisconf/proxycrypto:v1.0 -f Dockerfile .
# gcloud docker -- push us.gcr.io/everisconf/proxycrypto:v1.0

# docker run  -itd  --name proxycrypto -p 5000:5000    us.gcr.io/everisconf/proxycrypto:v1.0
