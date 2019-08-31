const path = require('path')

const here = __dirname

exports.assetsDir = path.join(here, '../assets')
exports.outputDir = path.join(here, '../output')
exports.coverArtDir = path.join(here, '../cover-art')
exports.songsFile = path.join(exports.assetsDir, 'songs.json')
