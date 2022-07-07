FROM python:3.6

# Update APT
RUN apt-get update

# Install Node JS
RUN apt-get install -y nodejs npm apache2

# Setup apache
RUN a2enmod headers cgi rewrite ssl socache_shmcb setenvif

# Make work directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# Install required packaged for Dijango projects
COPY ./server/requirements.txt ./server/requirements.txt
RUN pip install -r ./server/requirements.txt

# Clone source code
COPY . .

# Expose Dijango Server Port
EXPOSE 8000
# Expose Static File Port
EXPOSE 8081

# Start webserver
CMD ["python", "server/manage.py", "runserver", "0.0.0.0:8000"]
