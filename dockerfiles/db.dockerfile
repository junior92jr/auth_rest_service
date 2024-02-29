FROM postgres:16.2-alpine

ADD db/create_db.sql /docker-entrypoint-initdb.d
