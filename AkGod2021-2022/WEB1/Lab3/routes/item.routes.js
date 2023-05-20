// potrebno napisati

var express = require("express");
var router = express.Router();
const bazPod = require('../db');

router.get('/:id',async function(req, res, next) {

    let id = parseInt(req.params.id);

    let [categories, items] = (await Promise.all([
        bazPod.query('SELECT * FROM categories'),
        bazPod.query('SELECT * FROM inventory'),
    ])).map(result => result.rows);

    var partners = (await
        bazPod.query('SELECT * FROM partners')
        
    ).rows;

    items = items.filter( item => (item.id == id));
    categories = categories.filter(category => (category.id == items[0].categoryid))
    
    for (category of categories){
        for (partner of partners) {
            partner = partners.filter(category => (category.id == partner.partnerfor))
        }
    }
    
    

   

    res.render('item', {

    title: items[0].name,
    linkActive: 'order',
    item : items[0],
    category : categories[0],
    partners : partners
    });
    
});

module.exports = router;































