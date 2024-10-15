FROM python:3.11-slim-bookworm

ADD  . .

RUN pip install -U pip
RUN pip install -r requirements.txt

RUN apt-get update \
 && apt-get install -y wget tar

WORKDIR /data

RUN wget -O /data/en_core_med7_lg.tar.gz "https://www.dropbox.com/s/xbgsy6tyctvrqz3/en_core_med7_lg.tar.gz?dl=1"
RUN tar -xvzf /data/en_core_med7_lg.tar.gz
RUN pip install /data/en_core_med7_lg-0.0.3

RUN rm -rf en_core_med7_lg*

WORKDIR /app
EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--port", "80"]