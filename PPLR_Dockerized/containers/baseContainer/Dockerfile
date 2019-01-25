FROM python:2.7

RUN apt-get update && apt-get install -y r-base r-base-dev python-pip openjdk-8-jdk openjdk-8-jre x11-apps

RUN mkdir /data

RUN pip install mock pynacl crypto pycrypto pandas seaborn matplotlib numpy recordlinkage
