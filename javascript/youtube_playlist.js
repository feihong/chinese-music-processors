/*
Run this code in the console on a YouTube playlist page to get a semi-formatted
list of input lines.
*/
var lines = []
for (let link of document.querySelectorAll('a.ytd-playlist-video-renderer')) {
  let url = link.href
  let [_, videoId] = /\/watch\?v=(.*?)&/.exec(url)
  let shareUrl = 'https://youtu.be/' + videoId
  let text = link.querySelector('span.ytd-playlist-video-renderer').innerText
  lines.push(`${text}  ${shareUrl}`)
}
console.log(lines.join('\n'))
