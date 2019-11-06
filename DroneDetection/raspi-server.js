let http = require('http');
let express = require('express');

let app = express();


let httpServer = http.createServer(app);
httpServer.listen(9876);
console.log('started');

app.route('/flash').get((req, res) => {
    console.log('endpoint hit');

    res.status(200).send("FLASH_ACKNOWLEDGE").end();

});

app.route('/disconnect').get((req, res) => {
    res.send("DISCONNECT_ACKNOWLEDGE");

})