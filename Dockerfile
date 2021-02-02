FROM python:3.7
MAINTAINER dziugas.tornau@gmail.com

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create and set work directory
RUN mkdir /lunchvote
WORKDIR /lunchvote

# copy and install dependencies
COPY ./requirements.txt /lunchvote/requirements.txt
RUN pip install -r requirements.txt

# copy the rest of the application files
COPY . /lunchvote