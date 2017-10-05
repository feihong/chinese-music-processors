/*
Run this code in the console on a YouTube playlist page that contains Sing China
videos to get the data formatted in a way that can be directly fed to the
YouTube processor.
*/
let lines = []
for (let link of document.querySelectorAll('a.ytd-playlist-video-renderer')) {
  let url = link.href
  url = url.substring(0, url.indexOf('&list='))
  let text = link.querySelector('span.ytd-playlist-video-renderer').innerText
  let [_, artist, title] = /】(.*?)《(.*?)》/.exec(text)
  lines.push(`中心歌声  ${artist}  ${title}  ${url}`)
}
console.log(lines.join('\n'))
