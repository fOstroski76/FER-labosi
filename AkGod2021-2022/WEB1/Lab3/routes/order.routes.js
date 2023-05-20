// potrebno napisati
var express = require('express');
var router = express.Router();
const bazPod = require('../db');

router.get('/',async function(req, res, next) {

        const [categories, items] = (await Promise.all([
            bazPod.query('SELECT * FROM categories'),
            bazPod.query('SELECT * FROM inventory'),
        ])).map(result => result.rows);

   
        for (const category of categories) {
            category.items = items.filter(item => (item.categoryid === category.id));
        }


        res.render('order', {

        title: 'Order',
        linkActive: 'order',
        categories : categories
        });
        
});

module.exports = router;