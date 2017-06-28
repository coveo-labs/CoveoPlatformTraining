const express = require('express'),
  bodyParser = require('body-parser'),
  request = require('request'),
  app = express(),
  port = 8080,

  IMPERSONATE_TOKEN = 'YOUR-IMPERSONATE-TOKEN';

let getCookies = req=>{
  let o = {};
  (req.headers.cookie || '').split(';').forEach(match=> {
    let keyValuePair = match.trim().split('=');
    o[ keyValuePair[0] ] = decodeURIComponent( keyValuePair[1] );
  });
  return o;
};

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false })); // for parsing application/x-www-form-urlencoded

app.use(/\.(html|css|js|png)$/, express.static('public'));

app.use(function (req, res, next) {
  let cookies = getCookies(req);

  if ( !(/\/login/.test(req.url)) && !cookies.login ) {
    res.redirect('/login');
  }
  else {
    next();
  }
});


app.use('/coveo-search-ui', express.static('node_modules/coveo-search-ui'));
app.get('/login', function(req, res){
  res.sendFile(__dirname + '/public/login.html');
});

app.post('/login', function(req, res){
  let email = req.body.email,
    maxAge = {maxAge: 3600000}; // one hour

  // TODO - Define request to get access token for this user.
  let options = {
    method: '',
    url: '',
    headers: {},
    body: ''
  };

  // Request token then return it using cookies
  request(options, (error, response, bodyJson) => {
    let body = JSON.parse(bodyJson || '{}'),
      token = body.token;

    if (body.statusCode) {
      res.clearCookie('login');
      res.clearCookie('accessToken');
      res.status(body.statusCode);

      res.send(bodyJson);
      return;
    }

    res.cookie('login', email, maxAge); // one hour
    res.cookie('accessToken', token, maxAge); // one hour
    res.redirect('/');
  });
});

app.get('/', function(req, res){
  res.sendFile(__dirname + '/public/login_index.html');
});

app.listen(port, function(){
    console.log('Listening on port ', port);
});
