//middlewear

let port = 82;
let express = require('express');
let app = express();
let bcryptHash = require('bcrypt');
//let mongoose = require("mongoose");
let {MongoClient} = require("mongodb")
//mongoose.pluralize(null);
let cors = require('cors');

app.use(express.json());
app.use(cors({credentials: true, origin: 'http://localhost:3000', methods: ["GET","POST"]}))


//let urlUsers = "mongodb://username:password@database:27017/users?//authSource=admin"
//testing to see if we can use differen urls for git actions and server
let urlUsers = process.env.MONGO_URL;
let urlBooks = process.env.MONGO_URL_BOOKS;

//let urlBooks = "mongodb://username:password@database:27017/Books?authSource=admin"
//let urlUsers = "mongodb://localhost:27017/users"
//let urlBooks = "mongodb://mongodb:27017/books"

//mongoose.connect(urlUsers);

const newUsers = new MongoClient(urlUsers);
const newBooks = new MongoClient(urlBooks);

const database1 = newUsers.db("users")
const collectionUsers = database1.collection("users")
const database2 = newBooks.db("Books")
const collectionBooks = database2.collection("Books")


const connect = async() => {
  
  await newUsers.connect();
  await newBooks.connect();
  try
  { await collectionUsers.createIndex({email: 1},{phonenumber: 1}, {username: 1},{unique: true});
  await collectionUsers.createIndex({phonenumber: 1},{unique: true});
  await collectionUsers.createIndex({username: 1},{unique: true});
  await collectionBooks.createIndex({ISBN: 1}, {unique : true});
  //insert data
  await collectionBooks.insertMany([
  {
   
    ISBN: 2005018,
    'Book-Title': 'Clara Callan',
    'Book-Author': 'Richard Bruce Wright',
    'Year-Of-Publication': 2001,
    Publisher: 'Harper Flamingo Canada',
    'Image-URL-S': 'http://images.amazon.com/images/P/0002005018.01.THUMBZZZ.jpg',
    'Image-URL-M': 'http://images.amazon.com/images/P/0002005018.01.MZZZZZZZ.jpg',
    'Image-URL-L': 'http://images.amazon.com/images/P/0002005018.01.LZZZZZZZ.jpg',
    username: ''
  },
  {
   
    ISBN: 195153448,
    'Book-Title': 'Classical Mythology',
    'Book-Author': 'Mark P. O. Morford',
    'Year-Of-Publication': 2002,
    Publisher: 'Oxford University Press',
    'Image-URL-S': 'http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg',
    'Image-URL-M': 'http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg',
    'Image-URL-L': 'http://images.amazon.com/images/P/0195153448.01.LZZZZZZZ.jpg',
    username: ''
  },
  {
    
    ISBN: 60973129,
    'Book-Title': 'Decision in Normandy',
    'Book-Author': "Carlo D'Este",
    'Year-Of-Publication': 1991,
    Publisher: 'HarperPerennial',
    'Image-URL-S': 'http://images.amazon.com/images/P/0060973129.01.THUMBZZZ.jpg',
    'Image-URL-M': 'http://images.amazon.com/images/P/0060973129.01.MZZZZZZZ.jpg',
    'Image-URL-L': 'http://images.amazon.com/images/P/0060973129.01.LZZZZZZZ.jpg',
    username: ''
  },
  {
   
    ISBN: '0425176428',
    'Book-Title': "What If?: The World's Foremost Military Historians Imagine What Might Have Been",
    'Book-Author': 'Robert Cowley',
    'Year-Of-Publication': 2000,
    Publisher: 'Berkley Publishing Group',
    'Image-URL-S': 'http://images.amazon.com/images/P/0425176428.01.THUMBZZZ.jpg',
    'Image-URL-M': 'http://images.amazon.com/images/P/0425176428.01.MZZZZZZZ.jpg',
    'Image-URL-L': 'http://images.amazon.com/images/P/0425176428.01.LZZZZZZZ.jpg',
    username: ''
  },
  {
    
    ISBN: '0671870432',
    'Book-Title': 'PLEADING GUILTY',
    'Book-Author': 'Scott Turow',
    'Year-Of-Publication': 1993,
    Publisher: 'Audioworks',
    'Image-URL-S': 'http://images.amazon.com/images/P/0671870432.01.THUMBZZZ.jpg',
    'Image-URL-M': 'http://images.amazon.com/images/P/0671870432.01.MZZZZZZZ.jpg',
    'Image-URL-L': 'http://images.amazon.com/images/P/0671870432.01.LZZZZZZZ.jpg',
    username: ''
  },
  {
    
    ISBN: '0679425608',
    'Book-Title': 'Under the Black Flag: The Romance and the Reality of Life Among the Pirates',
    'Book-Author': 'David Cordingly',
    'Year-Of-Publication': 1996,
    Publisher: 'Random House',
    'Image-URL-S': 'http://images.amazon.com/images/P/0679425608.01.THUMBZZZ.jpg',
    'Image-URL-M': 'http://images.amazon.com/images/P/0679425608.01.MZZZZZZZ.jpg',
    'Image-URL-L': 'http://images.amazon.com/images/P/0679425608.01.LZZZZZZZ.jpg',
    username: ''
  },
  {
   
    ISBN: '074322678X',
    'Book-Title': "Where You'll Find Me: And Other Stories",
    'Book-Author': 'Ann Beattie',
    'Year-Of-Publication': 2002,
    Publisher: 'Scribner',
    'Image-URL-S': 'http://images.amazon.com/images/P/074322678X.01.THUMBZZZ.jpg',
    'Image-URL-M': 'http://images.amazon.com/images/P/074322678X.01.MZZZZZZZ.jpg',
    'Image-URL-L': 'http://images.amazon.com/images/P/074322678X.01.LZZZZZZZ.jpg',
    username: ''
  },
  {
   
    ISBN: '0771074670',
    'Book-Title': 'Nights Below Station Street',
    'Book-Author': 'David Adams Richards',
    'Year-Of-Publication': 1988,
    Publisher: 'Emblem Editions',
    'Image-URL-S': 'http://images.amazon.com/images/P/0771074670.01.THUMBZZZ.jpg',
    'Image-URL-M': 'http://images.amazon.com/images/P/0771074670.01.MZZZZZZZ.jpg',
    'Image-URL-L': 'http://images.amazon.com/images/P/0771074670.01.LZZZZZZZ.jpg',
    username: ''
  },
  {
    
    ISBN: '0887841740',
    'Book-Title': 'The Middle Stories',
    'Book-Author': 'Sheila Heti',
    'Year-Of-Publication': 2004,
    Publisher: 'House of Anansi Press',
    'Image-URL-S': 'http://images.amazon.com/images/P/0887841740.01.THUMBZZZ.jpg',
    'Image-URL-M': 'http://images.amazon.com/images/P/0887841740.01.MZZZZZZZ.jpg',
    'Image-URL-L': 'http://images.amazon.com/images/P/0887841740.01.LZZZZZZZ.jpg',
    username: ''
  },
  {
    
    ISBN: '1552041778',
    'Book-Title': 'Jane Doe',
    'Book-Author': 'R. J. Kaiser',
    'Year-Of-Publication': 1999,
    Publisher: 'Mira Books',
    'Image-URL-S': 'http://images.amazon.com/images/P/1552041778.01.THUMBZZZ.jpg',
    'Image-URL-M': 'http://images.amazon.com/images/P/1552041778.01.MZZZZZZZ.jpg',
    'Image-URL-L': 'http://images.amazon.com/images/P/1552041778.01.LZZZZZZZ.jpg',
    username: ''
  },
  {
   
    ISBN: '1558746218',
    'Book-Title': "A Second Chicken Soup for the Woman's Soul (Chicken Soup for the Soul Series)",
    'Book-Author': 'Jack Canfield',
    'Year-Of-Publication': 1998,
    Publisher: 'Health Communications',
    'Image-URL-S': 'http://images.amazon.com/images/P/1558746218.01.THUMBZZZ.jpg',
    'Image-URL-M': 'http://images.amazon.com/images/P/1558746218.01.MZZZZZZZ.jpg',
    'Image-URL-L': 'http://images.amazon.com/images/P/1558746218.01.LZZZZZZZ.jpg',
    username: ''
  },
  {
    
    ISBN: '1567407781',
    'Book-Title': 'The Witchfinder (Amos Walker Mystery Series)',
    'Book-Author': 'Loren D. Estleman',
    'Year-Of-Publication': 1998,
    Publisher: 'Brilliance Audio - Trade',
    'Image-URL-S': 'http://images.amazon.com/images/P/1567407781.01.THUMBZZZ.jpg',
    'Image-URL-M': 'http://images.amazon.com/images/P/1567407781.01.MZZZZZZZ.jpg',
    'Image-URL-L': 'http://images.amazon.com/images/P/1567407781.01.LZZZZZZZ.jpg',
    username: ''
  },
  {
    
    ISBN: '1575663937',
    'Book-Title': 'More Cunning Than Man: A Social History of Rats and Man',
    'Book-Author': 'Robert Hendrickson',
    'Year-Of-Publication': 1999,
    Publisher: 'Kensington Publishing Corp.',
    'Image-URL-S': 'http://images.amazon.com/images/P/1575663937.01.THUMBZZZ.jpg',
    'Image-URL-M': 'http://images.amazon.com/images/P/1575663937.01.MZZZZZZZ.jpg',
    'Image-URL-L': 'http://images.amazon.com/images/P/1575663937.01.LZZZZZZZ.jpg',
    username: ''
  },
  {
    
    ISBN: '1881320189',
    'Book-Title': 'Goodbye to the Buttermilk Sky',
    'Book-Author': 'Julia Oliver',
    'Year-Of-Publication': 1994,
    Publisher: 'River City Pub',
    'Image-URL-S': 'http://images.amazon.com/images/P/1881320189.01.THUMBZZZ.jpg',
    'Image-URL-M': 'http://images.amazon.com/images/P/1881320189.01.MZZZZZZZ.jpg',
    'Image-URL-L': 'http://images.amazon.com/images/P/1881320189.01.LZZZZZZZ.jpg',
    username: ''
  },
  {
   
    ISBN: '0440234743',
    'Book-Title': 'The Testament',
    'Book-Author': 'John Grisham',
    'Year-Of-Publication': 1999,
    Publisher: 'Dell',
    'Image-URL-S': 'http://images.amazon.com/images/P/0440234743.01.THUMBZZZ.jpg',
    'Image-URL-M': 'http://images.amazon.com/images/P/0440234743.01.MZZZZZZZ.jpg',
    'Image-URL-L': 'http://images.amazon.com/images/P/0440234743.01.LZZZZZZZ.jpg',
    username: ''
  },
  {
    
    ISBN: '0452264464',
    'Book-Title': 'Beloved (Plume Contemporary Fiction)',
    'Book-Author': 'Toni Morrison',
    'Year-Of-Publication': 1994,
    Publisher: 'Plume',
    'Image-URL-S': 'http://images.amazon.com/images/P/0452264464.01.THUMBZZZ.jpg',
    'Image-URL-M': 'http://images.amazon.com/images/P/0452264464.01.MZZZZZZZ.jpg',
    'Image-URL-L': 'http://images.amazon.com/images/P/0452264464.01.LZZZZZZZ.jpg',
    username: ''
  }
])
}
catch(error)
{
  console.log("Data has already been inserted into database");
}
 
}



const cookie = require("cookie");
const serverVar = app.listen(port, () => {
  connect();
  console.log("Running on port: " + port)
})

const sockets = require("socket.io");
let io = sockets(serverVar,  {cors: {origin: 'http://localhost:3000', methods: ["GET","POST"], credentials: true, secret: 'testsecret'}});




//some verification will need to be implemented to allow for phone numbers to be accurate ect.

//let Users = mongoose.model("users", UsersCheckSchema)
//let Books = mongoose.model("books", BooksSchema)
let session = require("express-session");
const cookieParser = require('cookie-parser');





const MiddleWearForSocketsandExpress = session({
  
  secret: 'testsecret',
  saveUninitialized: false,
  resave: false,
  cookie: {
    httpOnly: true,
    maxAge: 30 * 24 * 60 * 60 * 1000,
    sameSite: 'lax',
    secure: false,
    path: "/"
  }
})



app.use(MiddleWearForSocketsandExpress)
app.use(cookieParser('testsecret'))
io.use((socket,next) => {
  // {} because nothing in response
  cookieParser('testsecret')(socket.request, {}, function(){
    next();
  });

  
})



app.get("/", async(req,res) => {
  res.send("The send has sent a response!!")
})

app.get("/CookiesRequest", async(req,res) => {
  console.log(req.cookies)
  if (await CheckCookies(req.cookies) == true)
  {
    res.status(200).send("Cookies have been found")
  }
  else{
    res.status(404).send("No Cookie has bene found")
  }
  
})

app.post("/CheckLogin", async(req,res) => {
    connect();
    //Query the database to make sure that the SessionID is valid
    console.log(req.SessionID);
    try{
      //const collectionBooks = newBooks.db("books")

        console.log("here")
        //Set sessionID here

        //Add the SessonID to the database
      
        //find a way to generate a new sessionID just incase
        console.log("object is being printed")
        //const finddata = await collectionUsers.findOne({username: "somenewtestdata3"});
        
       
      
      if (await CheckLogin(req.body) == true)
      {
        
        const insert = await collectionUsers.updateOne({username: req.body[0].username}, {$set:  {SessionID: req.sessionID}})
        //Redirect user to the next page
        //res.cookie(req.sessionID)
        let username = await insert.username;
        //Because we dont send a cookie by default, we need to modify it to allow for it to be sent.
        req.session.user = {username};
        res.status(200).send("Valid");
      }
      else{
        console.log("We have queried the server invalid creds");
        res.status(401).send("Invalid Creds");
      }
    //code to redirect to other page
    }
    catch(e)
    {
      res.status(402).send("somthing when wrong")
    }    
})

app.post("/CheckRegistration", async(req,res) => {
  connect();
  console.log("CheckRegistration: " + req.body)
  if (await CheckRegistration(req.body, req.sessionID) == true)
  {
    let username = req.body[0].username
    console.log(req.SessionID);
    req.session.user = {username};
    res.status(200).send("Worked");
  }
  else
  {
    res.status(401).send("Unauthorised")
  }
})

app.get("/GetUserBooks", async(req,res) => {
  connect();

  //Get the book data
  let data = await GetUsersBooks(req.signedCookies['connect.sid']);
  if (data != false)
  {
    res.status(200).send(data);
  }
  else{
    res.status(400).send("Invalid");
  }
})

app.post("/PasswordChange", async(req,res) => {
  connect();



  //Get the book data
  console.log(req.body);
  if(await CheckPasswordValid(req.body[0].password, req.body[0].NewPassword,req.signedCookies['connect.sid']) == true)
  {
    res.status(200).send("Valid Password!");
  }
  else{
    res.status(401).send("Invalid Check password");


  }
})

//Get Cookies

async function CheckPasswordValid(passwordFirst,PasswordChange,cookie)
{
  console.log("THIS IS THE PASSWORD INPUTTED!!! " + passwordFirst);
  console.log(cookie);
  //Find Cookie
  //const insert = await collectionUsers.findOne({SessionID: cookie});
  let SaltRounds = 10;
  try{
  //let hashFinal = await bcryptHash.hash(passwordFirst,SaltRounds);
    
    
    //Check if password is correct
    const CheckPasswordValid = await collectionUsers.findOne({SessionID: cookie});
    console.log(CheckPasswordValid.password);
     if(await bcryptHash.compare(passwordFirst, CheckPasswordValid.password))
    {
      //User was authenticated sucessfully
      console.log("here! working")
      
      console.log("Got past this bit!!");
      await collectionUsers.updateOne({SessionID: cookie}, {$set: {password: await bcryptHash.hash(PasswordChange, SaltRounds)}});
      return true;
    }
    
    
    else{
      //inalid password
      console.log("Invalid");
      return false;
    }
   

    
    
    

  }
  catch(error){
    console.error(error);
    return false;
  }

}

async function GetUsersBooks(cookie)
{
  console.log("This Cookie!" + cookie);
  try{
     const insert = await collectionUsers.findOne({SessionID: cookie});
     console.log(insert);
    //Check if book exists and check that the username is null
    const checkBooks = await collectionBooks.find({username: insert.username}).toArray();
    console.log("CHECK BOOKS FUNC>>>>>>")
    console.log(checkBooks);
    return checkBooks;
  }
  catch(error)
  {
    console.log(error);
    return false;
  }
}

io.on("connection", socket => {
 
  socket.on("GetLibaryData", async function(msg){
    
   
    let getCookie = await CheckCookies(socket.request.signedCookies["connect.sid"])
    let data = await GetBooksAvailable();
    console.log("Cookie Value: " + getCookie + " and dataval" + data);
    if ((getCookie == true && data != false)|| (getCookie == true && data != null))
    {
      socket.emit("GetLibaryDataClient", data)
    }
    else{
      //get books which have not been taken out by users
      //GetBooksAvailable();

      socket.emit("GetLibaryDataClient", "No_Cookie")
    }
  })  
  //Post Libary dataa
  socket.on("ReserveBook", async function(msg){
    console.log("Reserve_Book");
    //Check that the book hasnt been reserved already (prevents people from inputting a ISBN number and just submitting)
    
    // if the result is correct, emit a response back
    console.log(socket.request.signedCookies["connect.sid"])
    if (await ReserveBook(socket.request.signedCookies["connect.sid"], msg) == true) 
    {
      let data = await GetBooksAvailable();
      console.log("Reserve Data: " + data);
      //my is broadcast not working?
      io.emit("GetLibaryDataClient", data);
      //Emit libary data back to user
      //console.log(data);
    }
    else
    {
      console.log("Somthing has gone wrong here");
    }


  })

})
async function ReserveBook(cookie, ISBN_Search)
{
  //Check that the cookie is valid
  console.log("Cookie: " + cookie + " and ISBN: " + ISBN_Search);
  try
  {
    //Checking if sessionID is valid
    const insert = await collectionUsers.findOne({SessionID: cookie});
    //Check if book exists and check that the username is null
    console.log(" /////////// Bug when updating Books ///////////////////");
    const checkBooks = await collectionBooks.findOne({ISBN: ISBN_Search});
    if (checkBooks.username == '')
    {
      
      console.log("The username of this book is null!");
      console.log(insert.username);
      //insert username into the record
      try{
        await collectionBooks.updateOne({ISBN: ISBN_Search}, {$set: {username: insert.username}});
      }
      catch{
        console.log("Somthing wrong with insert");
      }
      return true;
    }
    else{
      console.log("Issue is here something is wrong")
      return false;
    }
  }
  catch
  {
    console.log("WRONG HERE")
    return null;
  }
  //process
  //find sessionID - check if valid and return 
}

async function CheckCookies(Cookie)
{
  try
  {
    if (Cookie)
    {
    console.log(cookie)
    const insert = await collectionUsers.findOne({SessionID: Cookie})
    console.log("Cookies has been found" + insert.SessionID)
    return true;
    }
    else
    {
      return false;
    }
  }
  catch(e)
  {
    return false;
  }

}

async function GetBooksAvailable()
{
  console.log("We are in the correct function")
  
  //Get data using Mongodb
  try{
    const insert = await collectionBooks.find({username: ''}).toArray();
    JSON.stringify(insert)
    //console.log(insert)
    return insert;
  }
  catch(error){
    console.error(error)
    return false;
  } 
}


async function CheckLogin(msg)
{
  //hashed password
  console.log("Made it here??")
  try{
    const insert = await collectionUsers.findOne({username: msg[0].username})
    console.log(insert.password + "and the inputted: " + msg[0].password);
    if(await bcryptHash.compare(msg[0].password, insert.password))
    {
      //User was authenticated sucessfully
      console.log("here! working")
      return true;
    }
    else
    {
      return false;
    //Send message saying incorrect cookie
    }
  }
  catch{
    return false;
  } 
}


async function CheckRegistration(msg, SessionIDIn) {
  connect();
  let SaltRounds = 10;
  try {
    let hashFinal = await bcryptHash.hash(msg[0].password,SaltRounds)
    console.log(hashFinal)
    //might need to find records which contain the phone number, username, password ect
    const insert = await collectionUsers.insertOne({username: msg[0].username,password: hashFinal, email: msg[0].email, phonenumber: msg[0].phonenumber})
    // this runs of the origonal insert does not work because if the username is a duplicate it still inserts the sessionID which we dont want
    const insertSession = await collectionUsers.updateOne({username: msg[0].username}, {$set : {SessionID: SessionIDIn}})
    return true;
  }
  catch(e)
  {
    //console.error(e + "Here, somthing wrong with mongodb connection")
    return false;
  }
}


module.exports = app;