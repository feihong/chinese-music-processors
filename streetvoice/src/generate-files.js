/*
Supplement track metadata with lyrics, fileId, imageId, etc. Write cover art and
.ts files to disk.
*/
const fs = require('fs')
const Database = require('better-sqlite3')
const paths = require('./path.config')

const db = new Database('dumpfile.db', { fileMustExist: true })

function prepare(whereClause) {
  return db.prepare("SELECT * FROM dump WHERE " + whereClause)
}

const songs = require(paths.songsFile)

for (let song of songs) {
  const stmt = prepare(`path LIKE '%/song/${song.id}/%fields=lyrics%'`)
  const row = stmt.get()
  if (row) {
    song.lyrics = JSON.parse(row.data.toString()).lyrics.replace(/[\r][\n]/g, '\n')
  }

  // Get id of .ts file
  const stmt2 = prepare(`path LIKE '%/song/${song.id}/hls/file/'`)
  const row2 = stmt2.get()
  if (row2) {
    let fileIdRe = /\/([a-zA-Z0-9]+)[.]mp3/
    song.fileId = JSON.parse(row2.data.toString()).file.match(fileIdRe)[1]
  }

  // Write cover art to disk (grab the largest image we downloaded)
  const stmt3 = prepare(
    `path LIKE '%/${song.imageId}%' ORDER BY length(data) DESC`)
  const row3 = stmt3.get()
  if (row3) {
    const extension = row3.content_type.match(/image\/([a-z]+)/)[1]
    song.imageFile = `${paths.assetsDir}/${song.imageId}.${extension}`
    fs.writeFileSync(song.imageFile, row3.data)
  }

  // Create single .ts file by concatenating individual .ts files that have the
  // same fileId
  const stmt4 = prepare(`path LIKE '%/${song.fileId}.mp3%' ORDER BY path`)
  const filename = `${paths.assetsDir}/${song.id}.ts`
  if (fs.existsSync(filename)) {
    fs.unlinkSync(filename)
  }
  const rows = stmt4.all()
  if (rows.length) {
    const stream = fs.createWriteStream(filename, { flags: 'a' })
    for (const row of rows) {
      if (row.data) {
        stream.write(row.data)
      }
    }
    stream.end()
  }
}

fs.writeFileSync(paths.songsFile, JSON.stringify(songs, null, 2))
