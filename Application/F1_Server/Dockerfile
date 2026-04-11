FROM python:latest

WORKDIR /usr/app/src

#COPY F1_Server/server.py ./
#RUN python3 -m pip install requests
COPY F1_Server/requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt
EXPOSE 8001 
CMD ["uvicorn","server:app","--host","0.0.0.0","--port","8001", "--reload"]