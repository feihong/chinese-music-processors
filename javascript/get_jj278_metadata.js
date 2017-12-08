var lines = []
for (let link of document.querySelectorAll('a.ytd-playlist-video-renderer')) {
  let url = link.href
  let [_, videoId] = /\/watch\?v=(.*?)&/.exec(url)
  let shareUrl = 'https://youtu.be/' + videoId
  let text = link.querySelector('span.ytd-playlist-video-renderer').innerText
  // console.log(text)
  try {
    let [_, artist, album, title] = /(.*) -《(.*)》- (.*)/.exec(text)
    lines.push(`${album}  ${artist}  ${title}  ${shareUrl}`)
  } catch (e) {
    lines.push(`${text}  ${shareUrl}`)
  }
}
console.log(lines.join('\n'))
