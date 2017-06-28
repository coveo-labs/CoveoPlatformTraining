const express = require('express'),
  bodyParser = require('body-parser'),
  request = require('request'),
  GoogleAuth = require('google-auth-library'),
  app = express(),
  port = 8080,

  GOOGLE_CLIENT_ID = 'YOUR-GOOGLE-CLIENT-ID',
  IMPERSONATE_TOKEN = 'YOUR-IMPERSONATE-TOKEN';

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false })); // for parsing application/x-www-form-urlencoded

app.use(/\.(html|css|js|png)$/, express.static('public'));
app.use('/coveo-search-ui', express.static('node_modules/coveo-search-ui'));

app.post('/token', function(req, res){

  // See https://developers.google.com/identity/sign-in/android/backend-auth
  let token = req.body.idtoken,
    auth = new GoogleAuth(),
    client = new auth.OAuth2(GOOGLE_CLIENT_ID, '', '');

  client.verifyIdToken(
      token,
      GOOGLE_CLIENT_ID,
      function(e, login) {

        let payload = login.getPayload(),
          email = payload.email,

          // TODO - Define request to get access token for this user.
          options = {
            method: '',
            url: '',
            headers: {
            },
            body: ''
          };

        // Request the Search Token from the Coveo Search API.
        request(options, (error, response, bodyJson) => {
          // send response as is.
          res.send( bodyJson );
        });
      });
});

app.get('/', function(req, res){
  res.sendFile(__dirname + '/public/google_signin.html');
});

app.listen(port, function(){
    console.log('Listening on port ', port);
});
