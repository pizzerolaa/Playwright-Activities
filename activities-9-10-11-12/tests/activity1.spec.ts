import { test, expect } from '@playwright/test';

test.describe('Activity 1: GitHub Login Tests', () => {
    const fakeUsers = [
        { username: 'fakepepinito', password: 'holahola123' },
        { username: 'brokeassniga', password: 'fakepass0972' },
        { username: 'realfresasgdl', password: 'Holajaaj978@' },
        { username: 'oraclezzz', password: 'fazepepino987' },
        { username: 'tilininsano', password: 'wrongcreds202' }
    ];

    fakeUsers.forEach((user, index) => {
        test(`should show error for invalid credentials - User ${index + 1}`, async ({ page }) => {
            await page.goto('https://github.com/login');
            
            await page.waitForLoadState('networkidle');
            
            await page.fill('#login_field', user.username);
            
            await page.waitForSelector('#password:not([disabled])');
            await page.fill('#password', user.password);
            
            await page.click('input[type="submit"], button[type="submit"]');
            
            const errorSelectors = [
                '.js-flash-alert:visible',
                '.flash-error:visible', 
                '[role="alert"]:visible',
                '.Banner--error:visible'
            ];
            
            let errorFound = false;
            for (const selector of errorSelectors) {
                try {
                    await page.waitForSelector(selector, { timeout: 10000 });
                    const errorElement = page.locator(selector).first();
                    await expect(errorElement).toBeVisible();
                    errorFound = true;
                    break;
                } catch (e) {
                    continue;
                }
            }
            
            if (!errorFound) {
                await expect(page).toHaveURL(/.*login.*/);
            }
        });
    });
});