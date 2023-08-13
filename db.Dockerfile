FROM mysql:latest

COPY db/schema.sql /docker-entrypoint-initdb.d/data.sql

EXPOSE 3306
