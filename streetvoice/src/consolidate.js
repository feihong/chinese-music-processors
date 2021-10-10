/*
Combine metadata, cover art, and audio data into complete .m4a files. Also
apply track gain to balance loudness levels.
*/
const fs = require("fs");
const childProcess = require("child_process");
const sanitize = require("sanitize-filename");
const paths = require("./path.config");

// Convert .ts to .m4a
function convertToM4a(song, outputFile) {
  const tsFile = `${paths.assetsDir}/${song.id}.ts`;
  if (!fs.existsSync(tsFile)) {
    return;
  }

  // Convert and add metadata in one step
  childProcess.spawnSync(
    "ffmpeg",
    [
      "-y", // overwrite if file already exists
      "-i",
      tsFile,
      "-metadata",
      `title=${song.title}`,
      "-metadata",
      `artist=${song.artist}`,
      "-metadata",
      `album=${song.album}`,
      "-metadata",
      `comment=${song.url}`,
      "-metadata",
      `lyrics=${song.lyrics}`,
      "-metadata",
      `genre=${song.genre}`,
      "-metadata",
      `year=${song.year}`,
      "-vn", // ignore video
      "-c:a", "libfdk_aac", // use best encoder
      "-vbr", "4", // use high quality (5 is highest)
      outputFile,
    ],
    { stdio: "inherit" }
  );

  // Balance loudness levels
  childProcess.spawnSync(
    "aacgain",
    [
      "-r", // apply Track gain automatically (all files set to equal loudness)
      "-k", // automatically lower Track/Album gain to not clip audio
      outputFile,
    ],
    { stdio: "inherit" }
  );
}

function addCoverArt(song, outputFile) {
  if (!fs.existsSync(song.imageFile)) {
    return;
  }

  // If the image is webp, convert it to png since AtomicParsley cannot handle
  // webp
  if (song.imageFile.endsWith(".webp")) {
    const pngFile = `${paths.assetsDir}/${song.imageId}.png`;
    childProcess.spawnSync(
      "ffmpeg",
      [
        "-y", // overwrite if file already exists
        "-i",
        song.imageFile,
        pngFile,
      ],
      { stdio: "inherit" }
    );
    song.imageFile = pngFile;
  }

  // We do not add metadata in this step because AtomicParsley is notoriously
  // bad at adding lyrics
  childProcess.spawnSync(
    "AtomicParsley",
    [outputFile, "--artwork", song.imageFile, "--overWrite"],
    { stdio: "inherit" }
  );
}

const songs = require(paths.songsFile);

for (const song of songs) {
  console.log(song.title);

  const name = sanitize(`${song.artist}  ${song.title}.m4a`);
  const outputFile = `${paths.outputDir}/${name}`;

  convertToM4a(song, outputFile);
  addCoverArt(song, outputFile);
}

console.log('\nSearch for lyrics on Google:')
for (const song of songs) {
  const query = `${song.artist}  ${song.title} 歌词`.replace(/ /g, '+');
  console.log(`https://www.google.com/search?q=${query}`);
}
