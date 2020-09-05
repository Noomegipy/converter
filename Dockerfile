FROM python:3.7
COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt && \
    rm -rf /tmp/requirements.txt
COPY . /opt/main/
WORKDIR /opt/main
ENV PYTHONPATH=.
EXPOSE 5000
CMD ["python3", "app/main.py"]

