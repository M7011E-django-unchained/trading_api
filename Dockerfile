FROM python:3.12

#RUN apt-get update && apt-get install -y python-pip
RUN pip install --upgrade pip

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

#RUN python manage.py makemigrations
#RUN python manage.py migrate

# Bundle app source
COPY . .

EXPOSE 8000
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]