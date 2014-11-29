chrome.browserAction.onClicked.addListener(function(){
    chrome.tabs.insertCSS(null, {file: "style.css"});
    chrome.tabs.executeScript(null, {file: "bower_components/react/react.js"});
    chrome.tabs.executeScript(null, {file: "bower_components/react/JSXTransformer.js"});
    chrome.tabs.executeScript(null, {file: "build/app.js"});
})
