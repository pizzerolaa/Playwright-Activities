const { chromium } = require('@playwright/test');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    recordHar: { path: 'harry-potter-api.har' }
  });
  
  const page = await context.newPage();
  
  await page.goto('http://127.0.0.1:5500/PlaywrightAPIMocking/Actividad2/harry-potter-list.html');
  
  await page.waitForSelector('.character-card');
  
  await context.close();
  await browser.close();
  
  console.log('HAR file has been recorded to: harry-potter-api.har');
})();