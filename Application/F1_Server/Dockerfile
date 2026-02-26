FROM python:latest

WORKDIR /usr/app/src

#COPY F1_Server/server.py ./
#RUN python3 -m pip install requests
RUN python3 -m pip install --no-cache-dir requests pymongo websockets fastapi uvicorn
EXPOSE 8001
CMD ["uvicorn","server:app","--host","0.0.0.0","--port","8001", "--reload"]