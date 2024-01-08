FROM python:3.12.1-slim-bookworm
WORKDIR /app
RUN pip install python-dotenv flask requests
COPY ./app .
EXPOSE 5000
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]