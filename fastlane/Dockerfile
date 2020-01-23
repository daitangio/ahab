#FROM openjdk:8-stretch
FROM circleci/ruby:2.4.5
# GG Taken from 2017's https://github.com/yury-sannikov/android-fastlane-docker/blob/master/Dockerfile
# and modernized
LABEL maintainer "giovanni.giorgi@nttdata.com"

# app volume is for fastlane develop


ARG FASTLANE_VERSION
ARG BUNDLER_VERSION

ENV XAR_VERSION "2.0.0"
USER root
RUN mkdir -p /app

#GG Custom part for node 12 install
RUN apt-get update -y && apt-get install -y  less
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs
RUN node --version | grep 12 || ( echo "WRONG NODE VERSION: $(node --version)" ; exit 1000)
# There is a "WRONG" node on /usr/local/bin/node "by hand"
RUN echo  Node:$( node --version) Npm $( npm --version )
RUN which node 

# iTMSTransporter needs java installed
# We also have to install make to install xar
# And finally shellcheck
RUN echo 'deb http://archive.debian.org/debian jessie-backports main' > /etc/apt/sources.list.d/jessie-backports.list \
  && sed -i '/deb http:\/\/deb.debian.org\/debian jessie-updates main/d' /etc/apt/sources.list \
  && apt-get -o Acquire::Check-Valid-Until=false update \
  && apt-get install --yes   make  shellcheck \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get install --yes libssl-dev


# Needed for fastlane to work
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Required for iTMSTransporter to find Java
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/jre


# GG Mmmm but python is needed too?
# Install Python
ARG BUILDDIR="/tmp/build"
ARG PYTHON_VER="3.6.8"
WORKDIR ${BUILDDIR}

RUN apt-get update -o Acquire::Check-Valid-Until=false -qq && \
apt-get -o Acquire::Check-Valid-Until=false upgrade -y > /dev/null 2>&1 && \
apt-get install wget gcc make zlib1g-dev -y -qq > /dev/null 2>&1 && \
wget --quiet https://www.python.org/ftp/python/${PYTHON_VER}/Python-${PYTHON_VER}.tgz > /dev/null 2>&1 && \
tar zxf Python-${PYTHON_VER}.tgz && \
cd Python-${PYTHON_VER} && \
./configure  > /dev/null 2>&1 && \
make > /dev/null 2>&1 && \
make install > /dev/null 2>&1 && \
rm -rf ${BUILDDIR} 

WORKDIR /tmp

RUN ls
RUN ruby --version
RUN gem install bundler --version "$BUNDLER_VERSION"
# -N, --no-document                Disable documentation generation
# -V, --[no-]verbose
RUN gem install fastlane -NV -v $FASTLANE_VERSION

# NPM Upgrade here
RUN npm install -g npm@6.13.6

WORKDIR /app
# Ruby ruby 2.4.5p335 (2018-10-18 revision 65137) [x86_64-linux] with Node v10.15.3 and npm 6.4.1
# Ruby ruby 2.4.5p335 (2018-10-18 revision 65137) [x86_64-linux] with Node v10.15.3 and npm 6.4.1 and Ruby Bundler Bundler version 2.1.4
RUN echo Fastlane: $(fastlane --version ) 
RUN echo Ruby $(ruby -v) with Node $(node -v ) and npm $(npm -v)  and Ruby Bundler $( bundler -v )

# JDK 8 install
# **Stole openjdk docker build if you dare:
# https://github.com/docker-library/openjdk/blob/master/8/jdk/Dockerfile
RUN apt-get install -y default-jdk
RUN echo java $( java -version )
# ReactNative test