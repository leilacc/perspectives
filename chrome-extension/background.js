chrome.browserAction.onClicked.addListener(function(){
    chrome.tabs.executeScript(null, {file: "bower_components/velocity/velocity.js"});
    chrome.tabs.executeScript(null, {file: "bower_components/react/react.min.js"});

    chrome.tabs.insertCSS(null, {file: "style.css"});
    chrome.tabs.executeScript(null, {file: "build/app.js"});
})
