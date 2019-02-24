// call the packages we need
var express = require('express'); // call express
var app = express(); // define our app using express
var bodyParser = require('body-parser');
var http = require('http');
var request = require("request");

var validator = require('validate-image-url');

var proj_id = "hackilinois2019-232622";

var {Datastore} = require('@google-cloud/datastore');
const datastore = new Datastore({
    projectId: proj_id,
  });


// configure app to use bodyParser()
// this will let us get the data from a POST
app.use(bodyParser.urlencoded({
    extended: true
}));

app.use(bodyParser.json());

var port = process.env.PORT || 8080; // set our port

// ROUTES FOR OUR API
// =============================================================================
var router = express.Router(); // get an instance of the express Router
var fuel = express.Router();
var money = express.Router();

var state = 'IL'
var zip_code = '61820'
var api_key = '31c809cc5219736cd4194f399101830e'

router.post('/', function (req, res) {
    console.log(req.body);
    var first_name = req.body.first_name;
    var last_name = req.body.last_name;
    var plate = req.body.plate_num;
    console.log(plate);

    var options = { method: 'POST',
    url: 'http://api.reimaginebanking.com/customers',
    qs: { key: api_key },
    headers: 
     { 'Postman-Token': 'ce022f7e-70b4-4e62-b655-912ccc4170c4',
       'cache-control': 'no-cache',
       'Content-Type': 'application/json' },
    body: 
     { first_name: first_name,
       last_name: last_name,
       address: 
        { street_number: '1234',
          street_name: 'anywhere st.',
          city: 'nowhere',
          state: state,
          zip: zip_code } },
    json: true };
  
    request(options, function (error, response, body) {
        if (error) throw new Error(error);

        var account_num = Math.floor(1000000000000000 + Math.random() * 9000000000000000);

        var options = { method: 'POST',
        url: 'http://api.reimaginebanking.com/customers/5c71c9546759394351bee30a/accounts',
        qs: { key: api_key },
        headers: 
        { 'Postman-Token': '85450a41-aff0-4ae9-9388-a12c6fb8a245',
            'cache-control': 'no-cache',
            'Content-Type': 'application/json' },
        body: 
        { type: 'Credit Card',
            nickname: 'Parking Payment',
            rewards: 50000,
            balance: 50000,
            account_number: account_num.toString() },
        json: true };

        request(options, function (error, response, body) {
            if (error) throw new Error(error);
            //pushing to google data store
            // console.log(body)
            var kind = 'plate';
            // console.log(kind);
            var name = body.objectCreated._id;
            // console.log(name);
            const taskKey = datastore.key([kind, name]);
            // console.log(plate)
            const task = {
                key: taskKey,
                data: {
                    plate_id: plate,
                    space_id: 'N/A',
                    balance: 50000,
                    time: -1
                },
            };
            console.log(task);
            datastore.save(task);
            res.json("success!")
            console.log(`Saved ${task.key.name}: ${task.data.plate_id}`);
        });
    });
});


fuel.post('/', async function (req, res) {
    var space_id = req.body.space_id;
    var time = req.body.time;
    var plate = req.body.plate_num;
    console.log(space_id)
    console.log(time)
    console.log(plate)
    if (plate != " "){
        time = time.substring(11, 23)
        time = time.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"");
        // console.log(time);

        var rate = 20.0

        var space_query = datastore
            .createQuery('plate')
            .filter('space_id', '=', space_id);
        var parking_space = await datastore.runQuery(space_query);

        var time_multi = 5;

        if (parking_space[0][0].time != -1){
            time_multi = time - parking_space[0][0].time;
        }
        else{
            parking_space[0][0].time = time;
        }

        if (time_multi > 30){
            time_multi = 5
        }
        console.log(time_multi);
        console.log(parking_space[0][0].balance);
        
        parking_space[0][0].balance = parking_space[0][0].balance + time_multi * rate / 3600.0;
        var final_parking = parking_space[0][0].balance
        datastore.update(parking_space[0][0]);

        var cus_query = datastore
            .createQuery('plate')
            .filter('plate_id', '=', plate);
        var customer = await datastore.runQuery(cus_query);

        var time_multi = 5;
        // console.log(customer);
        if (customer[0][0].time != -1){
            time_multi = time - customer[0][0].time;
        }
        else{
            customer[0][0].time = time;
        }
        if (time_multi > 30){
            time_multi = 5
        }

        customer[0][0].balance = customer[0][0].balance - time_multi * rate / 3600.0;
        var final_customer = customer[0][0].balance;
        datastore.update(customer[0][0]);

        res.json({final_parking, final_customer});
    }
    else{
        res.json("Empty String!");
    }
    
});

money.post('/', async function (req, res) {
    var space_id = req.body.space_id;
    var plate = req.body.plate_num;
    console.log(space_id);
    console.log(plate);

    var space_query = datastore
        .createQuery('plate')
        .filter('space_id', '=', space_id);
    var parking_space = await datastore.runQuery(space_query);
    console.log(parking_space);
    var final_parking = parking_space[0][0].balance;

    var cus_query = datastore
        .createQuery('plate')
        .filter('plate_id', '=', plate);
    var customer = await datastore.runQuery(cus_query);
    console.log(customer);
    var final_customer = customer[0][0].balance;

    res.send({final_parking, final_customer});
});

app.use('/create', router);
app.use('/getFuel', fuel);
app.use('/stats', money)

// START THE SERVER
// =============================================================================
app.listen(port);
console.log('Magic happens on port ' + port);