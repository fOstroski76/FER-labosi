const express = require('express');
const router = express.Router();
const Helper = require('./helpers/helper');
const authHandler = require("./helpers/auth-handler");

router.get('/', authHandler, function (req, res, next) {
    res.render('view', {
        title: 'Newsletter Subscription',
        linkActive: 'cart',
        user: req.session.user,
        helper: new Helper(req.session.params),
        err: req.session.err
    });
});

router.post('/save',function(req,res,next){

    if (!req.session.params) {
        req.session.params = {};
    }

    req.session.params.email = req.body['e-mail'];
    req.session.params.newsletters = req.body.newsletters;
    req.session.params.statements = req.body.statements;

    res.redirect('/cart');

});

router.post('/reset',function(req,res,next){

    req.session.params = undefined

    res.redirect('/on-site');



});
router.post('/order',function(req,res,next){

    req.session.params = undefined

    res.redirect('/checkout');


});

module.exports = router;