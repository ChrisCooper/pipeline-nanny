FROM ubuntu:14.04

RUN apt-get update

RUN apt-get install -y python3-pip python3-dev python3-setuptools nginx supervisor sqlite3

ADD requirements.txt /
RUN pip3 install -r /requirements.txt

ADD pipeline_nanny /pipeline_nanny

RUN python3 /pipeline_nanny/manage.py syncdb --noinput

EXPOSE 8000

CMD ["python3", "/pipeline_nanny/manage.py", "test", "--verbosity=2", "taskmaster"]
#CMD ["python3", "/pipeline_nanny/manage.py", "runserver", "0.0.0.0:8000"]

# sudo docker build -t pnan . && sudo docker run -p 127.0.0.1:8000:8000 pnan