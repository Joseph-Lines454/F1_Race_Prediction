FROM python:3.14-slim
WORKDIR /app
COPY ML_Model/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ML_Model/NewModel.py NewModel.py
COPY ML_Model/F1_Data/Prerace_Prediction.csv Prerace_Prediction.csv
COPY ML_Model/F1_Data/Circuit_Conversion.csv Circuit_Conversion.csv
COPY ML_Model/F1_Data/Driver_Conversion.csv Driver_Conversion.csv
COPY ML_Model/F1_Data/Team_Conversion.csv Team_Conversion.csv
RUN python3 -m pip install --no-cache-dir requests pymongo websockets fastapi uvicorn paho-mqtt

#CMD ["python", "NewModel.py"]
CMD ["uvicorn","NewModel:app","--host","0.0.0.0","--port","2000", "--reload"]