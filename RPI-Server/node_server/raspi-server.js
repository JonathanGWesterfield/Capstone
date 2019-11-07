let http = require('http');
let express = require('express');
let app = express();
let spawn = require('child_process').spawn;


let httpServer = http.createServer(app);
httpServer.listen(9876);
console.log('started');

app.route('/flash').get((req, res) => {
    console.log('flashing light for 500 milliseconds');

    let light_process = spawn('python', ['./flash.py']);

    light_process.stdout.on('data', (data) => {
        res.status(200).send(data).end();
        console.log('data: ' + data);
        console.log('response sent');
    });

});

app.route('/disconnect').get((req, res) => {
    res.send("DISCONNECT_ACKNOWLEDGE");

    let shutdown_process = spawn('sh', ['./shutdown_pi.sh']);

});