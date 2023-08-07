FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ADD requirements/requirements.txt /

RUN apt-get update \
  && apt-get install -y --no-install-recommends\
    cron

RUN pip install -r /requirements.txt; 
RUN mkdir /src;
COPY ./scripts /scripts
COPY ./src /src
WORKDIR /src
