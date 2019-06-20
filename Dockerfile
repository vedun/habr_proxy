FROM python:3.5
WORKDIR /src

COPY ./src ./src
COPY ./proxy.py ./proxy.py
COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

EXPOSE 8080

CMD python proxy.py
