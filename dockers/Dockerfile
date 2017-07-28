FROM python:3

RUN pip3 install tox

ENV PROJECT_PATH=/root/project
WORKDIR $PROJECT_PATH

COPY ./ retail-qrcode/
WORKDIR $PROJECT_PATH/retail-qrcode

RUN pip3 install -r requirements.txt