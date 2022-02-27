# Docker file for a slim Ubuntu-based Python3 image
# how to run this image
# build the image -> docker image build -t flask_test .
# run the image -> docker run -it -d -p 5000:5000 --name flask_test flask_test

FROM ubuntu:latest
LABEL fnndsc "Michael Barcelo"

ENV DEBIAN_FRONTEND=noninteractive
ENV FLASK_APP="/API/main.py"
ENV FLASK_RUN_HOST="0.0.0.0"
ENV FLASK_RUN_PORT="5000"

RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y python3-pip python3-dev \
  && apt install wget -y \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 --no-cache-dir install --upgrade pip \
  && rm -rf /var/lib/apt/lists/* \
  && pip3 install Flask \ 
  && mkdir /API \
  && cd /API \
  && wget https://raw.githubusercontent.com/MBarc/Chill-Club-Movie-API/main/main.py \
  && wget https://raw.githubusercontent.com/MBarc/Chill-Club-Movie-API/main/database.json

EXPOSE 5000

ENTRYPOINT [ "/bin/bash", "-l", "-c" ]

CMD ["flask run"]
