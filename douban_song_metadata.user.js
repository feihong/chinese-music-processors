// ==UserScript==
// @name        Get Douban song metadata
// @namespace   https://github.com/feihong/
// @description Adds a button to the Douban player page that puts the song metadata onto the clipboard.
// @include     http://music.douban.com/artists/player/*
// @version     1
// @grant       GM_setClipboard
// ==/UserScript==

var playlist = unsafeWindow.__bootstrap_data['playlist'];

var div = document.createElement('div');
div.style =  "z-index: 10000; position: relative;";
document.body.insertBefore(div, document.body.firstChild);

// Add a button that puts song metadata on the clipboard.
var button = document.createElement('button');
button.innerHTML = 'Copy song metadata to clipboard';
div.appendChild(button);
button.onclick = function() {
    var text = JSON.stringify(unsafeWindow.__bootstrap_data);
    GM_setClipboard(text);  
};

// Add button that inserts a list of download links into page.
button = document.createElement('button');
button.innerHTML = 'Show metadata';
div.appendChild(button);
button.onclick = function() {
    ol.innerHTML = '';
    for (var i=0; i < playlist.length; i++) {
        var song = playlist[i];
        var li = document.createElement('li');
        li.setAttribute('data-id', i.toString());
        var parts = song.url.split('/');
        var fileName = parts[parts.length - 1];
        fileName = fileName.split('.')[0]
        var html = [
            '<a href="#" data-id=', i.toString(), '>',
            fileName, '  &nbsp;',
            song.title, '  &nbsp;',
            song.artist.name,
            '</a>'
        ];
        li.innerHTML = html.join('');
        ol.appendChild(li);
    }
};

// Add an unordered list that contains download links.
var ol = document.createElement('ol');
div.appendChild(ol);
ol.onclick = function(evt) {
    evt.preventDefault();
    var index = evt.target.attributes['data-id'].value;
    index = parseInt(index);
    var song = playlist[index];
    var text = JSON.stringify(song);
    GM_setClipboard(text);
    console.log('On clipboard: ' + text);
};
