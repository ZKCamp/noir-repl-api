FROM tiangolo/uvicorn-gunicorn:python3.8

WORKDIR /app

COPY requirements.txt requirements.txt

COPY install.sh install.sh

RUN apt-get -y install git

RUN curl -L https://raw.githubusercontent.com/noir-lang/noirup/main/install | bash

RUN /root/.nargo/bin/noirup

RUN echo 'export PATH="$PATH:/root/.nargo/bin"' >> /root/.bashrc

RUN cat /root/.bashrc

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ARG PORT=80
ARG HOST=0.0.0.0
ARG APP_MODULE=api.main:app
ARG WORKERS_PER_CORE=1

ENV APP_MODULE=${APP_MODULE}
ENV WORKERS_PER_CORE=${WORKERS_PER_CORE}
ENV HOST=${HOST}
ENV PORT=${PORT}

EXPOSE ${PORT}

WORKDIR /app/api

CMD uvicorn $APP_MODULE --port $PORT --host $HOST