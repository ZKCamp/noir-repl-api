FROM tiangolo/uvicorn-gunicorn:python3.8

WORKDIR /app

COPY requirements.txt requirements.txt

COPY install.sh install.sh

RUN apt-get -y install git

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN mkdir -p $HOME/.nargo/bin && \
    curl -o $HOME/.nargo/bin/nargo-x86_64-unknown-linux-gnu.tar.gz -L https://github.com/noir-lang/noir/releases/download/v0.5.1/nargo-x86_64-unknown-linux-gnu.tar.gz && \
    tar -xvf $HOME/.nargo/bin/nargo-x86_64-unknown-linux-gnu.tar.gz -C $HOME/.nargo/bin/ && \
    echo -e '\nexport PATH=$PATH:$HOME/.nargo/bin' >> ~/.bashrc && \
    source ~/.bashrc

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