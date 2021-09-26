// Playwright API is nicer, but it has problems downloading media. See README for details.
const playwright = require('playwright')

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

const launchOptions = {
  headless: false,
  proxy: { server: 'http://127.0.0.1:8080' }
};

async function main() {
  // Wait a little while to give mitmproxy time to start up
  await sleep(2000)
  const browser = await playwright.chromium.launch(launchOptions)
  const context = await browser.newContext()
  const page = await context.newPage()
  await page.goto('https://streetvoice.com/megafeihong')
  page.once('close', async () => {
    await browser.close()
    console.log('\nDone!')
  })
}

main()
