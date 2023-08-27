FROM mysql:latest

COPY db/setup.sql /docker-entrypoint-initdb.d/setup.sql

EXPOSE 3306
