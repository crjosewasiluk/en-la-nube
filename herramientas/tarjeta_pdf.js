// Convierte tarjeta/_pdf.html en tarjeta/Tarjeta Wasiluk Yasinsky.pdf, del tamaño exacto de la tarjeta.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = path.resolve(__dirname, '..', 'tarjeta');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 440, height: 800 } });
  await p.goto('file://' + path.join(dir, '_pdf.html'));
  await p.waitForTimeout(1500);
  const box = await p.locator('.tarjeta').boundingBox();
  await p.pdf({ path: path.join(dir, 'tarjeta-sin-adjuntos.pdf'), width: '440px',
    height: Math.ceil(box.height) + 1 + 'px', printBackground: true, pageRanges: '1' });
  await b.close();
})();
