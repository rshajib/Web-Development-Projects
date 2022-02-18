const http = require("http");
const https = require("https");
const url = require("url");
const fs = require("fs")
// const auth = require("./auth/auth.json");
const port = 3000;
const queryString = require("querystring");
const {client_id, apiKey} = require("./auth/auth.json"); // getting api key and secret id
const server = http.createServer();
let tokken;
server.on("request", connection_handler);

function connection_handler(req, res){
    console.log(`New Request Received from ${req.url}`);
    if(req.url === '/'){
      let formStream =  fs.createReadStream("./html/home.html"); // was form.html
      res.writeHead(200, {"Content-Type": "text/html"});
      formStream.pipe(res);
     
    } 
    else if(req.url.startsWith("/get_pet")){ // request urls
      const pet_type = url.parse(req.url, true).query;
      callCatApi(pet_type, res);
    }
}

function callCatApi (pet_type, ret) {

  var options = {
    'method': 'GET',
    'hostname': 'thatcopy.pw',
    'path': '/catapi/rest/',
    'headers': {
    },
    'maxRedirects': 20
  };

  var req = https.request(options, function (res) {
    var chunks = [];

    res.on("data", function (chunk) {
      chunks.push(chunk);
    });

    res.on("end", function (chunk) {
      var body = Buffer.concat(chunks);
      console.log(body.toString());
      get_access_tokken(pet_type, ret);
    });

    res.on("error", function (error) {
      console.error(error);
    });
  });

  req.end();
}

function get_access_tokken(value, ret) {   // for getting tokken un submitting client id and client secret

console.log("<====First api call initiated===>");
const options = {
  'method': 'POST',
  'hostname': 'api.petfinder.com',
  'path': '/v2/oauth2/token',
  'headers': {
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  'maxRedirects': 20
};

const req = https.request(options, function (res) {
  const chunks = [];

  res.on("data", function (chunk) { //get data chunk by chunk and merge in sing array
    chunks.push(chunk);
  });

  res.on("end", function (chunk) { //when data recieved from the server 
    const body = Buffer.concat(chunks);
    console.log(body.toString());
    const data = JSON.parse(body.toString());
    tokken = data.access_token;
    //call to another api after recieving tokken
    get_animal(value.petType, ret);
  });

  res.on("error", function (error) {
    console.error(error);
  });
});

const postData = queryString.stringify({
  'grant_type': 'client_credentials',
  'client_id': apiKey,
  'client_secret': client_id
});

req.write(postData);
req.end();
}

function get_animal(petId, ret){
console.log("<====Second api call initiated===>");
const options = {
  'method': 'GET',
  'hostname': 'api.petfinder.com',
  'path': `/v2/animals/${petId}`,
  'headers': {
    'Authorization': `Bearer ${tokken}`
  },
  'maxRedirects': 20
};

var req = https.request(options, function (res) {
  const chunks = [];

  res.on("data", function (chunk) {
    chunks.push(chunk);
  });

  res.on("end", function (chunk) {
    const body = Buffer.concat(chunks);
    console.log(body.toString());
    ret.writeHead(200, { 'Content-Type': 'text/html' });
    ret.write(htmlDoc(body.toString()));
  });

  res.on("error", function (error) {
    console.error(error);
  });
});

req.end();
}

function htmlDoc(data) {
  const pet = JSON.parse(data);
  const doc = `<!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Document</title>
  </head>
  <style>
      body {
          background-color: white;
          
      }
      h1{
          color: red;
          text-align: center;
          
      }
      h2{
          color:royalblue;
          text-align: center;
          
      }
   
  </style>
  <body>
      <h1>SUCCESS</h1>
      <h2>YOUR PET FOUND</h2>

      <p>PET NAME: ${pet.animal.name}</P>
      <img src=${pet.animal.primary_photo_cropped.small} />
      <a href="http://localhost:3000/">RETURN TO APP!</a>
      
  </body>
  </html>`
  return doc;
}
server.on("listening", () => console.log(`Now Listening on Port ${port}`));
server.listen(port);


 