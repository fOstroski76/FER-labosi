const {Pool} = require('pg');

const pool = new Pool({
    user: 'postgres',
    host: 'localhost',
    database: 'web1-lab3',
    password: 'bazepodataka',
    port: 5432,
});

const sql_create_inventory = `DROP TABLE IF EXISTS inventory;
    CREATE TABLE inventory (
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL UNIQUE,
    price numeric NOT NULL,
    categoryId int NOT NULL,
    imageUrl text NOT NULL,
    colors text NOT NULL
)`;

const sql_create_categories = `DROP TABLE IF EXISTS categories;
    CREATE TABLE categories (
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL UNIQUE,
    description text NOT NULL,
    seasonal text NOT NULL
)`;

const sql_insert_inventory = `INSERT INTO inventory (
    name, price, categoryId, imageUrl, colors)
    VALUES 
    ('Tulip', 10, 1, 'https://i.imgur.com/Ttir6mp.jpg', 'white, red, yellow'),
    ('Lavender', 15, 1, 'https://i.imgur.com/gH33WyT.jpg', 'blue'),
    ('Fuchsia', 50, 1, 'https://i.imgur.com/s27QJBL.jpg', 'red-purple, white-purple, white-pink'),
    ('Daisy', 30, 1, 'https://i.imgur.com/Agarl4v.jpg', 'white'),
    ('Orchid', 90, 2, 'https://i.imgur.com/Dx4q8uE.jpg', 'green, white, purple'),
    ('Fittonia', 80, 2, 'https://i.imgur.com/G9JfR3S.jpg', 'green, red'),
    ('Showel', 150, 3, 'https://i.imgur.com/BcjgzeT.jpg', 'metal'),
    ('Small showel', 50, 3, 'https://i.imgur.com/L80eL1e.jpg', 'metal'),
    ('Rake', 100, 3, 'https://i.imgur.com/I5ctUan.jpg', 'metal'),
    ('Tulip (1 kg)', 200, 4, 'https://i.imgur.com/WUYYzBG.jpg', 'white, mix, yellow');
`;

const sql_insert_category = `INSERT INTO categories (name, description, seasonal) VALUES 
    ('Flowers', 'Flowers make us smile', 'Yes'),
    ('Indoor plants', 'Bring nature inside', 'No'),
    ('Tools', 'Every gardener needs good tools', 'No'),
    ('Seeds', 'Grow your own plants', 'No'),
    ('Pots', 'Many sizes and styles', 'No'),
    ('Fertilizers', 'Essential nutrients', 'No');
`;

const sql_create_partners = `DROP TABLE IF EXISTS partners;
    CREATE TABLE partners (
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL,
    owner_name text NOT NULL,
    owner_surname text NOT NULL,
    email text NOT NULL,
    partnerSince numeric NOT NULL,
    partnerFor int NOT NULL
)`;

const sql_insert_partners = `INSERT INTO partners (name, owner_name, owner_surname, email, partnerSince, partnerFor) VALUES 
    ('Vesela rotkvica', 'Roko', 'Rotkvić', 'roko.rotkvic@vesela.rotkvica.hr', 2012, 1),
    ('Urbani vrt d.o.o.', 'Vrtić', 'Ferić', 'urbani.vrt@fer.hr', 2021, 7),
    ('Trnovit put', 'Ružica', 'Ružić', 'ruzica.ruzic@trn.hr', 1999, 3),
    ('Cvjetko j.d.o.o.', 'Ivančica', 'Cvjetić', 'ivancica.cvjetic@flowershop.hr', 2013, 2),
    ('Sunce', 'Sunčica', 'Horvat', 'suncica.horvat@sunce.hr', 2005, 5),
    ('Proljeće101', 'Hrvoje', 'Hortenzijo', 'hrvoje.hortenzijo@proljece.hr', 1990, 7),
    ('Jagodica d.o.o.', 'Jagoda', 'Jagodić', 'jagoda.jagodic@jagodica.hr', 2019, 8),
    ('Leptir d.0.0.', 'Iris', 'Leptirić', 'iris.leptiric1989@leptir.hr', 2000, 2),
    ('Šareni vrt, d.o.o.', 'Narcisa', 'Spring', 'narcisa.spring@sarenivrt.hr', 1998, 4),
    ('Jabuka Granny Smith', 'Lily Rose', 'Žutić Kljutić', 'lily.zutic-k22@grannysmith.jabuka.hr', 1997, 1);
`;

pool.query(sql_create_inventory, [], (err, result) => {
    if (err) {
        return console.error(err.message);
    }
    console.log("Successful creation of the 'inventory' table");
    pool.query(sql_insert_inventory, [], (err, result) => {
        if (err) {
            return console.error(err.message);
        }
    });
});

pool.query(sql_create_categories, [], (err, result) => {
    if (err) {
        return console.error(err.message);
    }
    console.log("Successful creation of the 'categories' table");
    pool.query(sql_insert_category, [], (err, result) => {
        if (err) {
            return console.error(err.message);
        }
    });
});

pool.query(sql_create_partners, [], (err, result) => {
    if (err) {
        return console.error(err.message);
    }
    console.log("Successful creation of the 'partners' table");
    pool.query(sql_insert_partners, [], (err, result) => {
        if (err) {
            return console.error(err.message);
        }
    });
});