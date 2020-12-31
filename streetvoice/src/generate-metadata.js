/*
Scrape playlist pages and convert the track metadata within to json
*/
const fs = require("fs");
const Database = require("better-sqlite3");
const paths = require("./path.config");

const db = new Database("dumpfile.db", { fileMustExist: true });

function prepare(whereClause) {
  return db.prepare("SELECT * FROM dump WHERE " + whereClause);
}

const genreMap = {
  1: '摇滚 Rock',
  2: '说唱 Rap',
  3: '电子 Electronica',
  4: '流行 Pop',
  5: '民谣 Folk',
  6: 'Singer/Songwriter',
  7: '另类 Alternative',
  8: '后摇滚 Post rock',
  10: '朋克 Punk',
  12: 'R&B/Soul',
  16: 'Soundtrack/New Age',
};

const imageIdRe = /\/([a-zA-Z0-9]+)[.](?:jpg|jpeg|png)/i;

function* getSongs() {
  const stmt = prepare(
    "path LIKE '%song_ids=%' AND content_type LIKE 'application/json%'"
  );
  let count = 0;
  for (const row of stmt.iterate()) {
    count += 1;
    const rowData = JSON.parse(row.data.toString());
    fs.writeFileSync(`./assets/songs_${count}.json`, JSON.stringify(rowData, null, 2));

    const data = JSON.parse(row.data.toString());

    yield* data.results.map((result) => {
      return {
        id: result.id,
        title: result.name,
        artist: result.user.profile.nickname,
        url: `https://streetvoice.com/${result.user.username}/songs/${result.id}/`,
        imageUrl: result.image,
        imageId: result.image.match(imageIdRe)[1],
        album: result.album ? result.album.name : "",
        genre: genreMap[result.genre] || result.genre,
        year: new Date(result.created_at).getFullYear(),
      };
    });
  }
}

const songs = [...getSongs()];
fs.writeFileSync(paths.songsFile, JSON.stringify(songs, null, 2));

songs.forEach((song, i) => {
  console.log(`${i + 1}. ${song.title}`);
});
