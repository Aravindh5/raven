# Creates a Docker images with Python that is ready for Raven
FROM ubuntu:14.04

# Update
RUN apt-get -yqq update
RUN apt-get update && apt-get install -yqq software-properties-common
RUN apt-get update && apt-get install -yqq python-software-properties
RUN add-apt-repository -y ppa:jonathonf/python-2.7
RUN apt-get -yqq update
RUN apt-get -yqq install python2.7
RUN apt-get install -y python-pkg-resources=3.3-1ubuntu1
RUN apt-get install -y python-setuptools python-dev build-essential
RUN easy_install pip
RUN apt-get install -y python-mysqldb

# Install app dependencies
RUN pip install flask && \
pip install flask_sqlalchemy && \
pip install pandas && \
pip install numpy && \
pip install six && \
pip install pyyaml && \
pip install wheel && \
#pip install mysql-python && \
pip install -U marshmallow && \
pip install tldextract && \
pip install requests && \
pip install nose
# define command for this image
CMD ["bash"]