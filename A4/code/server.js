var express = require("express");
var app = express();
var bodyParser = require('body-parser');
var errorHandler = require('errorhandler');
var methodOverride = require('method-override');
var hostname = process.env.HOSTNAME || '34.204.88.233';
var port = 8080;

<<<<<<< HEAD
// Automatically serve index.html from the public directory
app.use(express.static(__dirname + '/public'));
=======
app.get("/", function (req, res) {
    res.sendFile(__dirname + "/public/index.html")
});
>>>>>>> 7d5ac484702e8c5fdad911aa6cec91b1b0d3ba20

app.use(methodOverride());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(errorHandler());

console.log("Simple static server listening at http://" + hostname + ":" + port);
app.listen(port);
