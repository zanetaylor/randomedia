FROM python:3.11.7-slim-bookworm
WORKDIR /app
RUN pip install flask requests
COPY ./app .
EXPOSE 5000
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]