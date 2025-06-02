import { test, expect } from '@playwright/test';

test.describe('Weather App Tests', () => {
  test('mock successful API request for Paris weather', async ({ page }) => {
    // Interceptar y simular la respuesta de la API para Paris
    await page.route('**/api.weatherapp.com/data?city=Paris', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          city: 'Paris',
          temperature: 22,
          condition: 'Sunny'
        })
      });
    });

    // Navegar a la página
    await page.goto('http://127.0.0.1:5500/PlaywrightAPIMocking/Actividad1/weather.html');
    
    // Introducir "Paris" y hacer clic en el botón
    await page.fill('#cityInput', 'Paris');
    await page.click('#searchBtn');
    
    // Verificar que los resultados se muestran correctamente
    await expect(page.locator('#result')).toBeVisible();
    await expect(page.locator('#result')).toContainText('Paris');
    await expect(page.locator('#result')).toContainText('22°C');
    await expect(page.locator('#result')).toContainText('Sunny');
  });

  test('mock 500 Internal Server Error for weather API', async ({ page }) => {
    // Interceptar y simular un error 500 para cualquier ciudad
    await page.route('**/api.weatherapp.com/data**', route => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal Server Error' })
      });
    });

    // Navegar a la página
    await page.goto('http://127.0.0.1:5500/PlaywrightAPIMocking/Actividad1/weather.html');
    
    // Introducir una ciudad y hacer clic en el botón
    await page.fill('#cityInput', 'London');
    await page.click('#searchBtn');
    
    // Verificar que se muestra el mensaje de error
    await expect(page.locator('#error')).toBeVisible();
    await expect(page.locator('#error')).toContainText('Error: 500');
    
    // Verificar que el div de resultados no es visible
    await expect(page.locator('#result')).not.toBeVisible();
  });
});