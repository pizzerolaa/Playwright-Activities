import { test, expect } from '@playwright/test';

test.describe('Activity 2: Weather App Simulation Tests', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('http://127.0.0.1:5500/activities-9-10-11-12/Actividad1/weather.html');
    });

    test('should display weather information for valid city', async ({ page }) => {
        await page.route('**/api.weatherapp.com/data**', route => {
            route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify({
                    city: 'Madrid',
                    temperature: 25,
                    condition: 'Partly Cloudy'
                })
            });
        });

        await page.fill('#cityInput', 'Madrid');
        await page.click('#searchBtn');

        await expect(page.locator('#result')).toBeVisible();
        await expect(page.locator('#result')).toContainText('Madrid');
        await expect(page.locator('#result')).toContainText('25°C');
        await expect(page.locator('#result')).toContainText('Partly Cloudy');
    });

    test('should handle API error gracefully', async ({ page }) => {
        await page.route('**/api.weatherapp.com/data**', route => {
            route.fulfill({
                status: 500,
                contentType: 'application/json',
                body: JSON.stringify({ error: 'Internal Server Error' })
            });
        });

        await page.fill('#cityInput', 'InvalidCity');
        await page.click('#searchBtn');

        await expect(page.locator('#error')).toBeVisible();
        await expect(page.locator('#error')).toContainText('Error: 500');
        await expect(page.locator('#result')).not.toBeVisible();
    });

    test('should validate empty city input', async ({ page }) => {
        await page.click('#searchBtn');
        
        page.on('dialog', async dialog => {
            expect(dialog.message()).toContain('Please enter a city name');
            await dialog.accept();
        });
    });
});

test.describe('Activity 2: Video Recording Setup', () => {
    test('weather app complete workflow for video recording', async ({ page }) => {
        await page.goto('http://127.0.0.1:5500/activities-9-10-11-12/Actividad1/weather.html');
        
        let requestCount = 0;
        await page.route('**/api.weatherapp.com/data**', route => {
            requestCount++;
            if (requestCount <= 2) {
                route.fulfill({
                    status: 200,
                    contentType: 'application/json',
                    body: JSON.stringify({
                        city: requestCount === 1 ? 'Barcelona' : 'Tokyo',
                        temperature: requestCount === 1 ? 23 : 18,
                        condition: requestCount === 1 ? 'Sunny' : 'Rainy'
                    })
                });
            } else {
                route.fulfill({
                    status: 404,
                    contentType: 'application/json',
                    body: JSON.stringify({ error: 'City not found' })
                });
            }
        });

        await page.fill('#cityInput', 'Barcelona');
        await page.click('#searchBtn');
        await expect(page.locator('#result')).toContainText('Barcelona');
        await page.waitForTimeout(2000);
        
        await page.fill('#cityInput', 'Tokyo');
        await page.click('#searchBtn');
        await expect(page.locator('#result')).toContainText('Tokyo');
        await page.waitForTimeout(2000);
        
        await page.fill('#cityInput', 'InvalidCityName');
        await page.click('#searchBtn');
        await expect(page.locator('#error')).toBeVisible();
        await page.waitForTimeout(2000);
    });
});