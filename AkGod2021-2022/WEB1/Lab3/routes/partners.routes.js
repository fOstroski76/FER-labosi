var express = require('express');
var router = express.Router();
const bazPod = require('../db');

router.get('/',async function(req, res, next) {

        var partners = (await
            bazPod.query('SELECT * FROM partners')
            
        ).rows;

   
        res.render('partners', {

        title: 'Partners',
        linkActive: 'partners',
        partners : partners
        });
        
});


router.get('/update-partner',async function(req,res,next){


    var partners = (await
        bazPod.query('SELECT * FROM partners')
        
    ).rows;

    res.render('update-partner', {

        title : 'Update partner',
        linkActive : 'partners',
        partners : partners
    });


});

module.exports = router;