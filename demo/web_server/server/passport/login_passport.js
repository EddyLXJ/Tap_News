const jwt = require('jsonwebtoken');
// var user = require('../models/user');
const User = require('../models/user');
const PassportLocalStrategy = require('passport-local').Strategy;
const config = require('../config.json');

module.exports = new PassportLocalStrategy({
    usernameField: 'email',
    passwordField: 'password',
    session: false,
    passReqToCallback: true
}, (req, email, password, done) => {
    const userData = {
        email: email.trim(),
        password: password.trim()
    };


    return User.findOne({email: userData.email }, (err, user) => {
        if (err) {return done(err); }

        if (!user) {
            const error = new Error('Incorrect email or password');
            error.name = 'IncorrectCredentialsError';

            return done(error);
        }

        return user.comparePassword(userData.password, (passwordErr, isMatch) => {
            if (passwordErr) {
                return done(passwordErr);
            }

            if (!isMatch) {
                const error = new Error('Incorrect email or password');
                error.name = 'IncorrectCredentialsError';

                return done(error);
            }

            const payload = {
                sub: user._id
            };

            const token = jwt.sign(payload, config.jwtSecret);
            const data = {
                name: user.email
            };

            return done(null, token, data);
        });
    });
});
