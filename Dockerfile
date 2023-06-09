FROM python:3.10.6-buster

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY Makefile Makefile
COPY hatescan /hatescan
COPY model_scale /model_scale
COPY model_topic /model_topic
COPY token_pickle /token_pickle

CMD uvicorn hatescan.api.model_api:app --host 0.0.0.0 --port $PORT