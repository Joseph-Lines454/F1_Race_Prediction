import pytest
from server import app
from fastapi.testclient import TestClient
from pymongo import MongoClient
from server import CheckCookies
import os
import bcrypt
client = TestClient(app)
#Testing is done on a test database
clientDatabase = MongoClient(os.getenv("MONGO_URL"))
newdatabase = clientDatabase["f1db"]
Driver_Lap_Times = newdatabase["Driver_Lap_Times"]
Races = newdatabase['Races']
#we need to store the standings after each race in the database
Drivers_Standings = newdatabase["Drivers_Standings"]
Teams_Standings = newdatabase["Teams_Standings"]
Driver_Names = newdatabase["Driver_Names"]
Team_Names = newdatabase["Team_Names"]
SessionData = newdatabase["SessionData"]
RaceResults = newdatabase["RaceResults"]
UserData = newdatabase["loginInfo"]


@pytest.fixture(scope = "session", autouse=True)
def userdel():
  yield
  UserData.delete_one({'username': 'usernameTwo'})

@pytest.fixture(scope = "session", autouse=True)
def insertUser():
  hashed_password = bcrypt.hashpw('usernameIn'.encode("utf-8"), bcrypt.gensalt())
  UserData.insert_one({'username': 'usernameIn', 'password': hashed_password, 'email': 'randomEmail'})
  yield
  UserData.delete_one({'username': 'usernameIn', "password": hashed_password})



@pytest.fixture()
def userCookie():
  response = client.post("/Login", json = {
    "username": "usernameIn",
    "password": "usernameIn"})
  
  return response.cookies
  
  
#now we need to get a cookie for a valid test

def test_RegisterWrong():
  response = client.post("/Register")
  
  assert response.status_code == 422

def test_LoginCorrect():
  response = client.post("/Login", json = {
    "username": "usernameIn",
    "password": "usernameIn"})
  assert response.status_code == 200

def test_LoginWrong():
  response = client.post("/Login", json = {
    "username": "username8",
    "password": "usernameawd"})
  assert response.status_code == 401


def test_RegisterCorrect():
  response = client.post("/Register", json = {
    "username": "usernameTwo",
    "password": "usernameTwo",
    "email": "usernameTwo"})
  #Need to connect to database and delete this
  assert response.status_code == 200

def test_F1_StatisticsCorrect(userCookie):
  response = client.get("/F1_Statistics", cookies = userCookie)
  #Need to connect to database and delete this
  assert response.status_code == 200

def test_F1_StatisticsFalse():
  client.cookies.clear()
  response = client.get("/F1_Statistics",cookies ={})
  #Need to connect to database and delete this
  print("CheckHeaders: " + str(response.request.headers))
  assert response.status_code == 401


def test_Unit_CheckCookiesFalse():
  assert CheckCookies(None) == False


def test_Unit_CheckCookiesTrue(userCookie):
  print("Cookie_Test: " + str(userCookie))
  assert CheckCookies(userCookie["session_cookie"]) == True