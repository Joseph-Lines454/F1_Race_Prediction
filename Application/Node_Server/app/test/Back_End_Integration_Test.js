const chai = require('chai')
const chaiHttp = require('chai-http');
const server = require('../server');
let should = chai.should();
let bcryptHash = require('bcrypt');
const {expect} = chai;
chai.use(chaiHttp);

let urlUsers = process.env.MONGO_URL;
let {MongoClient} = require("mongodb")
const newUsers = new MongoClient(urlUsers);
const database1 = newUsers.db("users")
const collectionUsers = database1.collection("users")

//testing database
let SaltRounds = 10;
var credentialsObj = {
  username: "somenewtestdata",
  password: "username2"
}

//we plant data in the database for testing no volumes


describe('Checking if the user should Login', function(){
  before(async function(){
    await newUsers.connect();
    await collectionUsers.createIndex({username: 1, email: 1, phonenumber: 1},{unique: true});
    //we need to insert the data before hand
    
    
    //do hashing for password
    let hashFinal = await bcryptHash.hash("newtestuser",SaltRounds)
    //might need to find records which contain the phone number, username, password ect
    await collectionUsers.insertOne({username: "newtestuser",password: hashFinal, email: "newtestuser", phonenumber: "newtestuser"})
    
  })

  it('Login without username and password', function(done)
  {
    
    chai.request(server)
    .post('/CheckLogin')
    .end((err,res) => {
      //should be 401 because the user should not be valid due to lack of credentials
      expect(res).to.have.status(401);
    })
    done();
  })
  
  it('Login with credentials', function(done) {
    
    chai.request(server)
    .post('/CheckLogin')
    .set('connection','keep alive')
    .set('Content-Type', "application/json")
    .send(JSON.stringify([{username: "newtestuser", password: "newtestuser"}]))
    .end((err,res) => {
      //should be status of 200 because valid username and password
      expect(res).to.have.status(200);
    })
    done();

  })
  
  it('Login with incorrect credentials', function(done) {
    
    chai.request(server)
    .post('/CheckLogin')
    .set('connection','keep alive')
    .set('Content-Type', "application/json")
    .send(JSON.stringify([{username: "cred", password: "usa"}]))
    .end((err,res) => {
      //should be status of 200 because valid username and password
      expect(res).to.have.status(401);
    })
    done();
  })

  after(async function(){
     //we need to insert the data before hand
    await newUsers.connect();
    //do hashing for password
    await collectionUsers.deleteOne({username: "newtestuser"})
    
  })
})

describe('Checking Registration Works', function(){
  before(async function(){
    
    await newUsers.connect();
    //collectionUsers.createIndexes({username: 1, email: 1, phonenumber: 1},{unique: true});
    await collectionUsers.deleteOne({username: "newtestdataV2a"})
    //do hashing for password
    let hashFinal = await bcryptHash.hash("newtestdataV2a",SaltRounds)
    //might need to find records which contain the phone number, username, password ect

    //need to sort contrainsts because some tests wont work
    await collectionUsers.insertOne({username: "newtestdataV2a",password: hashFinal, email: "newtestdataV2a", phonenumber: "newtestdataV2a"})

  })

  it('Correct Details', function(done)
  {
    
    chai.request(server)
    .post('/CheckRegistration')
    .set('connection','keep alive')
    .set('Content-Type', "application/json")
    //should work however no validation
    .send(JSON.stringify([{username: "somenewtestdataaawdawd", password: "username2wadawd", email: "email", phonenumber: "something"}]))
    .end((err,res) => {
      //should be 401 because the user should not be valid due to lack of credentials
      
      expect(res).to.have.status(200);
    
    })
    done();
  })
  
  it('Insert details which are already in database (such as username) - shoud throw error', function(done)
  {
    
    chai.request(server)
    .post('/CheckRegistration')
    .set('connection','keep alive')
    .set('Content-Type', "application/json")
    //should work however no validation
    .send(JSON.stringify([{username: "somenewtestdataaawdawd", password: "username2wadawd", email: "email", phonenumber: "something"}]))
    .end((err,res) => {
      //should be 401 because the user should not be valid due to lack of credentials
      expect(res).to.have.status(401);
      
    })
    done();
  })
  
  after(async function(){
    await newUsers.connect();
    //do hashing for password
    await collectionUsers.deleteOne({username: "somenewtestdataaawdawd"})
    await collectionUsers.deleteOne({username: "newtestdataV2a"})
    
  })
})  