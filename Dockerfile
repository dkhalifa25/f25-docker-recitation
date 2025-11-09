# specifies the Parent Image from which you are building.
FROM python:3.9

# specify the working directory for the image
WORKDIR /code

# copy requirements.txt to working directory
COPY ./requirements.txt /code/requirements.txt

# install dependencies into working environment
RUN pip install -r /code/requirements.txt

# copy the ./app directory into the code directory
COPY ./app /code/app

# run uvicorn and tell it to import the app object from main
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]