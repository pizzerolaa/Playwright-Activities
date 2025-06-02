import { test, expect } from '@playwright/test';

test.describe('Harry Potter Character List Tests', () => {
  test('mock API and insert your name and house', async ({ page }) => {
    await page.route('https://hp-api.onrender.com/api/characters', async route => {
      //respuesta original
      const response = await fetch('https://hp-api.onrender.com/api/characters');
      const originalCharacters = await response.json();
      
      //limitamos a 11 personajes en lugar de 12
      const modifiedCharacters = originalCharacters.slice(0, 11);
      
      //agregamos personaje nuevo
      modifiedCharacters.unshift({
        name: 'Fher Garcia',
        house: 'Hufflepuff',
        actor: 'Fernando Garcia',
      });
      
      //devolver la respuesta modificada
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(modifiedCharacters)
      });
    });

    await page.goto('http://127.0.0.1:5500/PlaywrightAPIMocking/Actividad2/harry-potter-list.html');
    
    //checamos q nuevo personaje aparece
    await expect(page.locator('.character-card:first-child')).toContainText('Fher Garcia');
    await expect(page.locator('.character-card:first-child')).toContainText('Hufflepuff');
    
    //checar q haya 12 tarjetas en total (11 originales + la nueva)
    await expect(page.locator('.character-card')).toHaveCount(12);
  });

  test('mock API and remove a character', async ({ page }) => {
    await page.route('https://hp-api.onrender.com/api/characters', async route => {
      const response = await fetch('https://hp-api.onrender.com/api/characters');
      const originalCharacters = await response.json();
      
      //eliminar Potter
      const modifiedCharacters = originalCharacters.filter(char => char.name !== 'Harry Potter');
      
      //tomar los primeros 12
      const finalCharacters = modifiedCharacters.slice(0, 12);
      
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(finalCharacters)
      });
    });

    await page.goto('http://127.0.0.1:5500/PlaywrightAPIMocking/Actividad2/harry-potter-list.html');
    
    //ver que Potter no aparece
    const harryPotterCard = page.locator('.character-card', { hasText: 'Harry Potter' });
    await expect(harryPotterCard).toHaveCount(0);
    
    //ver que si haya 12 tarjetas en total
    await expect(page.locator('.character-card')).toHaveCount(12);
  });
});