FROM python:3.12.1-slim-bookworm
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
CMD [ "flask", "run", "--host", "0.0.0.0", "--port", "5000"]