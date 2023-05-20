const express = require('express');
const router = express.Router();
const cart = require('../models/CartModel')
const cartSanitizer = require('./helpers/cart-sanitizer');

// Ulančavanje funkcija međuopreme
router.get('/', cartSanitizer, function (req, res, next) {
    //####################### ZADATAK #######################
    // prikaz košarice uz pomoć cart.ejs
    res.render('cart', {
        title: 'Cart',
        linkActive: 'cart',
        user: req.session.user,
        cart: req.session.cart,
        err: undefined
    })
    //#######################################################
});


router.get('/add/:id',async function (req, res, next) {
    //####################### ZADATAK #######################
    //dodavanje jednog artikla u košaricu
    await cart.addItemToCart(req.session.cart, req.params.id, 1)
    res.end()
    //#######################################################


});

router.get('/remove/:id',async function (req, res, next) {
    //####################### ZADATAK #######################
    //brisanje jednog artikla iz košarice
    
        await cart.removeItemFromCart(req.session.cart, req.params.id, 1)
        res.end()
    
    //#######################################################


});

module.exports = router;