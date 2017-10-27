
function showMetadata() {
  populateList()

  if ($('#douban-metadata button').length === 0) {
    $('<button>')
      .text('Copy to clipboard')
      .appendTo('#douban-metadata')
      .on('click', copyMetadata)
  }
}

function copyMetadata() {
  let json = JSON.stringify(getPlaylist(), null, 2)
  console.log(json)
  copyToClipboard(json)
}

function getPlaylist() {
  console.log('Get playlist')
  let scripts = $('script').filter(function() {
    return this.innerText.includes('var __bootstrap_data = ')
  })

  if (scripts.length) {
    let text = scripts[0].innerText
    let start = text.indexOf('{"playlist": ')
    let end = text.lastIndexOf(';')
    let data = JSON.parse(text.substring(start, end))
    let playlist = data.playlist
    // console.log(`Found ${playlist.length} songs in playlist`)
    return playlist
  } else {
    console.log('No playlist found')
    return []
  }
}

function populateList() {
  let ol = $('#douban-metadata ol')
  if (ol.length === 0) {
    ol = $('<ol>').appendTo('#douban-metadata')
  } else {
    ol.empty()
  }
  for (let song of getPlaylist()) {
    let li = $('<li>').appendTo(ol)
    $('<a>').text(song.filename).attr('href', song.url).appendTo(li)

    $('<a style="margin: 0 1rem">')
      .attr('href', song.artist.url)
      .attr('target', '_blank')
      .html(song.artist.name)
      .appendTo(li)

    $('<span style="margin-right: 1rem">').html(song.title).appendTo(li)
  }
}

// Source: https://github.com/mdn/webextensions-examples/tree/master/context-menu-copy-link-with-types
function copyToClipboard(text) {
    function onCopy(event) {
        document.removeEventListener('copy', onCopy, true)
        // Hide the event from the page to prevent tampering.
        event.stopImmediatePropagation()
        // Overwrite the clipboard content.
        event.preventDefault()
        event.clipboardData.setData('text/plain', text)
    }
    document.addEventListener('copy', onCopy, true)

    // Requires the clipboardWrite permission, or a user gesture:
    document.execCommand('copy')
}

// Add the #douban-metadata div
$(document).ready(() => {
  if ($('#douban-metadata').length === 0) {
    $('<div id="douban-metadata"></div>').prependTo(document.body)
  }
})
