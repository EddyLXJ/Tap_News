var createError = require('http-errors');
var config = require('./config');
require('./models/main').connect(config.mongoDbUri);
var passport = require('passport');
var express = require('express');
var path = require('path');
var indexRouter = require('./routes/index');
var newsRouter = require('./routes/news');
var authRouter = require('./routes/auth');
var app = express();
var cors = require('cors');


// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use('/static', express.static(path.join(__dirname, '../client/build/static/')));

app.use(cors());



app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup_passport');
var localLoginStrategy = require('./passport/login_passport');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);

const authCheckMiddleware = require('./middleware/auth_checker');
app.use('/news', authCheckMiddleware());

app.use('/', indexRouter);
app.use('/auth', authRouter);
app.use('/news', newsRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});
module.exports = app;
