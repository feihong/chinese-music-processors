/*
Download full-size cover art separately.
*/
const fs = require('fs')
const paths = require('./path.config')
const https = require('https')

function downloadArt(song) {
  return new Promise(resolve => {
    const url = song.imageUrl.replace('h_44', 'h_610').replace('w_44', 'w_610')

    https.get(url, response => {
      const contentType = response.headers['content-type']
      const extension = contentType.match(/image\/([a-z]+)/)[1]
      const filename = `${paths.coverArtDir}/${song.title}.${extension}`
      const stream = fs.createWriteStream(filename)
      response.pipe(stream)
      response.on('end', resolve)
    })
  })
}

const songs = require(paths.songsFile)

async function main() {
  for (const song of songs) {
    console.log(song.title);
    await downloadArt(song)
  }
}

main()
