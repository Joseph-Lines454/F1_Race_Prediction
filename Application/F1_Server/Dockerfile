FROM python:latest

WORKDIR /usr/app/src

#COPY F1_Server/server.py ./
#RUN python3 -m pip install requests
RUN python3 -m pip install --no-cache-dir requests pymongo
EXPOSE 8001
CMD ["python3","server.py"]