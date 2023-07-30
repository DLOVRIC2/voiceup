# Use the official PostgreSQL image as the base image
FROM postgres:12

COPY . /db

# Environment variables to configure the PostgreSQL server
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=mydb

# Expose port 5432 for PostgreSQL
EXPOSE 5432
