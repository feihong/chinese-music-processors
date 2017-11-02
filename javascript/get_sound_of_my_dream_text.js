/*
Run this code in the console on a YouTube playlist page that contains 梦想的声音
videos to get the data formatted in a way that can be directly fed to the
YouTube processor.
*/
let lines = []
for (let link of document.querySelectorAll('a.ytd-playlist-video-renderer')) {
  let url = link.href
  let [_, videoId] = /\/watch\?v=(.*?)&/.exec(url)
  let shareUrl = 'https://youtu.be/' + videoId
  let text = link.querySelector('span.ytd-playlist-video-renderer').innerText
  // console.log(text)
  try {
    let [_, artist, title] = /]\s+(.*?)《(.*?)》/.exec(text)
    lines.push(`梦想的声音  ${artist}  ${title}  ${shareUrl}`)
  } catch (e) {
    continue
  }
}
console.log(lines.join('\n'))
