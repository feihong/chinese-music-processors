function addEventListener(selector, eventName, fn) {
  let node = document.querySelector(selector)
  node.addEventListener('click', fn)
}


addEventListener('.show', 'click', evt => {
  browser.tabs.executeScript({
    code: 'showMetadata()'
  }).then(window.close)
})

// addEventListener('.copy', 'click', evt => {
//   browser.tabs.executeScript({code: 'copyMetadata()'})
//     .then(() => console.log('done'))
// })

addEventListener('input[type=checkbox]', 'click', evt => {
  // console.log(!!evt.target.checked)
  browser.storage.local.set({autoDownload: !!evt.target.checked})
    .then(window.close)
})

browser.storage.local.get('autoDownload').then(result => {
  // console.log(result)
  // Set the value of the checkbox
  let checkbox = document.querySelector('input[type=checkbox]')
  checkbox.checked = !!result.autoDownload
})
