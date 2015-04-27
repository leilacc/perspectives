// if news website loaded then...
//var counter = 0

//
//bal = chrome.browserAction.setBadgeText
//setInterval(function(){
//    counter= counter+1
//    bal({text: ""+counter})},1000)

var data

var startRequest = function(tab){
    console.log("start server request")
    console.time("server request");
    var request = new XMLHttpRequest();
    request.open('GET', 'http://52.1.96.53/analysis/r.php?start_point='+ tab.url, true);

    request.onload = function() {
        console.timeEnd("server request");
        if (request.status >= 200 && request.status < 400) {
            // Success!
            console.log(request)
            var data = request.responseText.match(/\[([^]+)/)

            if (data.length > 0) {
                var parsed = JSON.parse(data[0])

                turning = false

                datawonull = parsed.filter(function (f) {
                    return (f !== null)
                })

                chrome.tabs.insertCSS(null, {file: "style.css"});

                chrome.browserAction.setBadgeText({text: "" + datawonull.length})

                chrome.tabs.sendMessage(tab.id, datawonull, function (response) {
                    console.log(response.farewell)
                });
            } else{
                turning = false
            }
        } else {
            // We reached our target server, but it returned an error
            turning = false
        }
    };

    request.onerror = function() {
        console.timeEnd("server request");
    };

    request.send();
}

var turning = false;

chrome.browserAction.setBadgeBackgroundColor({color:[0, 0, 0, 2]});

chrome.browserAction.onClicked.addListener(function(){
    turning = !turning;


    chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
        startRequest(tabs[0])
    });
    chrome.tabs.executeScript(null, {file: "bower_components/velocity/velocity.js"});
    chrome.tabs.executeScript(null, {file: "bower_components/react/react.js"});
    chrome.tabs.executeScript(null, {file: "build/app.js"});

});

var r = 0
delta = 1;
pImageLoaded = false;
var pImage = new Image(38, 38);
pImage.src = 'p-38x38.png';
pImage.loaded = function(){pImageLoaded = true};

function draw(scale) {
    if (turning === true) {
        r++
        //r += delta;
        //if (r <= 0 || r >= 30) delta = -delta;
    }

    var canvas = document.getElementById('canvas')
    var c2     = canvas.getContext('2d'),
        numberOfSides = 8,
        size   = 8.6*scale,
        Xcenter = 9*scale,
        Ycenter = 9*scale;

    c2.clearRect(0,0,38,38);

    if (!turning) c2.fillStyle = '#333';
    else c2.fillStyle = '#00bbff'

    c2.save();
    c2.translate(Xcenter, Ycenter);
    c2.rotate(r * (Math.PI/45));
    c2.beginPath();


    c2.moveTo (size * Math.cos(0), size *  Math.sin(0));

    for (var i = 1; i <= numberOfSides;i += 1) {
        c2.lineTo (size * Math.cos(i * 2 * Math.PI / numberOfSides), size * Math.sin(i * 2 * Math.PI / numberOfSides));
    }


    c2.closePath();
    c2.fill();
    c2.restore();
    if (scale === 2) c2.drawImage(pImage, 0, 0);
    else c2.drawImage(pImage, 0, 0, 19, 19);

    return c2.getImageData(-3, -2, 19*scale, 19*scale);
}

window.setInterval(function() {
    chrome.browserAction.setIcon({imageData: {'19': draw(1), '38': draw(2)
    }});
}, 50, chrome);
