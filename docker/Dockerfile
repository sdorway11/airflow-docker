FROM python:3.6-slim
LABEL maintainer="spencer dorway"
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Airflow
ARG AIRFLOW_VERSION=1.10.2
ARG AIRFLOW_HOME=/usr/local/airflow
ENV AIRFLOW_GPL_UNIDECODE yes
ENV AIRFLOW_HOME=${AIRFLOW_HOME}
ENV APP_ENVIRONMENT=${APP_ENVIRONMENT}
ENV AIRFLOW_GPL_UNIDECODE yes
ENV EXECUTOR="CeleryExecutor"
ENV AIRFLOW__CORE__EXECUTOR="CeleryExecutor"
ENV REDIS_PORT=6379

ENV POSTGRES_PORT=5432
# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

# Copy requirements file
COPY docker/requirements.txt ${AIRFLOW_HOME}/requirements.txt

RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        python3-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
        build-essential \
        python3-pip \
        python3-requests \
        default-libmysqlclient-dev \
        apt-utils \
        libpq5 \
        curl \
        rsync \
        netcat \
        locales \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow \
    && pip install -U pip setuptools wheel \
    && pip install -r ${AIRFLOW_HOME}/requirements.txt \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

ENV AIRFLOW__WEBSERVER__DAG_DEFAULT_VIEW=graph
ENV SMTP_STARTTLS=False
ENV AIRFLOW__SMTP__SMTP_STARTTLS=False
ENV SMTP_SSL=False
ENV AIRFLOW__SMTP__SMTP_SSL=False
ENV SMTP_PORT=25
ENV AIRFLOW__SMTP__SMTP_PORT=25

# Disable Loading of example DAGs
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

# Set timezone.
RUN ln -sf "/usr/share/zoneinfo/UTC" /etc/localtime

ARG APP_PATH="/usr/local/airflow/app"

ENV PYTHONPATH=${PYTHONPATH}:${APP_PATH}

# Shell
COPY docker/wait-for-it/wait-for-it.sh /usr/local/bin/wait-for-it
COPY docker/start.sh /usr/local/bin/start

RUN chmod +x /usr/local/bin/start \
    && chmod +x /usr/local/bin/wait-for-it

VOLUME ${AIRFLOW_HOME}/dags
VOLUME ${AIRFLOW_HOME}/plugins
VOLUME ${AIRFLOW_HOME}/sensors
VOLUME ${AIRFLOW_HOME}/app


RUN chown -R airflow: ${AIRFLOW_HOME}


USER airflow
WORKDIR ${AIRFLOW_HOME}
ENTRYPOINT ["/usr/local/bin/start"]

# set default arg for start script
CMD ["webserver"]