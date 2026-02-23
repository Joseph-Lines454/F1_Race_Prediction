FROM python:latest

WORKDIR /usr/app/src

COPY F1_Server/server.py ./
RUN python3 -m pip install requests

EXPOSE 8001
CMD ["python3","server.py"]