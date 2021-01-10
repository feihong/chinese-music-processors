const puppeteer = require("puppeteer-core");

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function main () {
  // Wait a second to give mitmproxy time to start up
  await sleep(1000);

  const browser = await puppeteer.launch({
    headless: false,
    executablePath: "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome",
    args: [ '--proxy-server=http://127.0.0.1:8080' ],
  });
  const page = await browser.newPage();
  await page.goto('https://streetvoice.com/megafeihong');
  page.once("close", async () => {
     await browser.close();
     console.log("\nDone!");
  });
}

main();
