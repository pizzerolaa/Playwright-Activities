import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

test.describe('Harry Potter Character List with HAR replay', () => {
  test('replay from unmodified HAR file', async ({ page }) => {
    // Cargar el archivo HAR
    const harPath = path.join(__dirname, '..', 'harry-potter-api.har');
    const har = JSON.parse(fs.readFileSync(harPath, 'utf8'));
    
    // Interceptar la solicitud y responder con los datos del HAR
    await page.route('https://hp-api.onrender.com/api/characters', route => {
      // Encontrar la entrada correspondiente en el HAR
      const entry = har.log.entries.find(entry => 
        entry.request.url.includes('hp-api.onrender.com/api/characters'));
      
      if (entry) {
        route.fulfill({
          status: entry.response.status,
          headers: entry.response.headers,
          body: entry.response.content.text
        });
      } else {
        route.continue();
      }
    });

    // Navegar a la página
    await page.goto('http://127.0.0.1:5500/PlaywrightAPIMocking/Actividad2/harry-potter-list.html');
    
    // Verificar que los personajes se cargan
    await expect(page.locator('.character-card')).toHaveCount(12);
  });
  
  test('replay from modified HAR file', async ({ page }) => {
    // Cargar el archivo HAR
    const harPath = path.join(__dirname, '..', 'harry-potter-api.har');
    const har = JSON.parse(fs.readFileSync(harPath, 'utf8'));
    
    // Modificar el HAR
    const entry = har.log.entries.find(entry => 
      entry.request.url.includes('hp-api.onrender.com/api/characters'));
    
    if (entry && entry.response.content.text) {
      // Convertir el texto en un objeto
      const characters = JSON.parse(entry.response.content.text);
      
      // Modificar la respuesta
      characters.unshift({
        name: 'HAR Modified Character',
        house: 'Slytherin',
        actor: 'HAR File'
      });
      
      // Actualizar el texto del HAR
      entry.response.content.text = JSON.stringify(characters);
    }
    
    // Interceptar la solicitud y responder con los datos modificados del HAR
    await page.route('https://hp-api.onrender.com/api/characters', route => {
      const entry = har.log.entries.find(entry => 
        entry.request.url.includes('hp-api.onrender.com/api/characters'));
      
      if (entry) {
        route.fulfill({
          status: entry.response.status,
          headers: entry.response.headers,
          body: entry.response.content.text
        });
      } else {
        route.continue();
      }
    });

    // Navegar a la página
    await page.goto('http://127.0.0.1:5500/PlaywrightAPIMocking/Actividad2/harry-potter-list.html');
    
    // Verificar que el personaje modificado aparece
    await expect(page.locator('.character-card:first-child')).toContainText('HAR Modified Character');
    await expect(page.locator('.character-card:first-child')).toContainText('Slytherin');
  });
});