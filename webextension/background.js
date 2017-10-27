
// browser.webRequest.onBeforeRequest.addListener(
//   details => {
//     if (details.url.endsWith('.mp3')) {
//       console.log('Before request:', details.requestId, details.url)
//     }
//   },
//   {urls: ['*://*.doubanio.com/*']}
// )

// When an MP3 download completes, download it into ~/Downloads/douban-songs/.
browser.webRequest.onCompleted.addListener(
  async function(details) {
    let url = details.url
    console.log('Request complete:', details.requestId, url)
    let parts = url.split('/')
    let filename = 'douban-songs/' + parts[parts.length - 1]
    let result = await browser.storage.local.get('autoDownload')
    if (result.autoDownload) {
      console.log(`Download ${url} to ${filename}`)
      browser.downloads.download({
        url: url,
        filename: filename,
        conflictAction: 'overwrite'
      })
    }
  },
  {urls: ['*://*/*.mp3']}
)
