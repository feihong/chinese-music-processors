const puppeteer = require("puppeteer");

async function main () {
  const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();
  await page.goto('https://feihonghsu.com');
  await page.screenshot({path: 'example.png'});
  await browser.close();
}

main();
