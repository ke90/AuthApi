FROM mcr.microsoft.com/mssql/server:2019-latest

USER root
RUN mkdir -p /usr/config && chmod -R 777 /usr/config

USER mssql
WORKDIR /usr/config



COPY . /usr/config
USER root
RUN chmod +x /usr/config/entrypoint.sh
RUN chmod +x /usr/config/configure-db.sh
USER mssql


ENTRYPOINT [ "./entrypoint.sh" ]


# RUN chmod +r /tmp/docker-entrypoint-initdb.d/script.sql