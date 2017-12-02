const express = require('express');
const path = require('path');
const favicon = require('serve-favicon');
const logger = require('morgan');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');

const routeIndex = require('./app/routes/index');

const config = require('./config');

const app = express();
mongoose.Promise = global.Promise;
mongoose.connect(config.mongo_connect, {
	  useMongoClient: true
	}, 
	function(err) { 
		if (err) console.log(err); 
		else console.log('Connected to the database successfully.'); 
	} 
);

// view engine setup
app.set('views', path.join(__dirname, 'app/views'));
app.set('view engine', 'pug');

/* ------------------------------------------------------------
    Access-Control-Allow-Origin | Header
------------------------------------------------------------ */
app.use(function(req, res, next) {
    let $strAllowedOrigins = [
        "http://localhost:4200",
    ];

    let $strOrigin = req.headers.origin;
    if($strAllowedOrigins.indexOf($strOrigin) > -1){
        res.setHeader("Access-Control-Allow-Origin", $strOrigin);
    } // if

    res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PATCH');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    res.header('Access-Control-Allow-Credentials', true);
    next();
});

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'app/public')));

app.use(function (req, res, next) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
    res.setHeader('Access-Control-Allow-Methods', 'POST, GET, PATCH, DELETE, OPTIONS');
    next();
});

app.use("/", routeIndex);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  let err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
