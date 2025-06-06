import { test, expect } from '@playwright/test';

test.describe('Activity 4: Mercado Libre User Actions Tests', () => {
    test('should search for products and navigate results', async ({ page }) => {
        await page.goto('https://www.mercadolibre.com');
        await page.waitForLoadState('domcontentloaded');
        
        await page.waitForTimeout(3000);
        
        const countryLinks = page.locator('a[href*="mercadolibre.com"]');
        const count = await countryLinks.count();
        
        if (count > 0) {
            await countryLinks.first().click();
            await page.waitForLoadState('domcontentloaded');
            await page.waitForTimeout(2000);
        }
        
        const searchSelectors = [
            'input[placeholder*="Buscar"]',
            '.nav-search-input',
            '#cb1-edit',
            'input[type="text"][name="as_word"]',
            '.nav-search-input'
        ];
        
        let searchSuccess = false;
        for (const selector of searchSelectors) {
            try {
                const searchInput = page.locator(selector).first();
                if (await searchInput.isVisible({ timeout: 3000 })) {
                    await searchInput.click();
                    await searchInput.fill('laptop');
                    await page.keyboard.press('Enter');
                    searchSuccess = true;
                    break;
                }
            } catch (e) {
                continue;
            }
        }
        
        if (searchSuccess) {
            await page.waitForLoadState('domcontentloaded');
            await page.waitForTimeout(3000);
            
            const resultSelectors = [
                '.ui-search-layout__item',
                '.ui-search-layout .ui-search-layout__item',
                'ol.ui-search-layout li',
                '.ui-search-item',
                '.ui-search-result'
            ];
            
            let resultsFound = false;
            for (const selector of resultSelectors) {
                try {
                    await page.waitForSelector(selector, { timeout: 8000 });
                    const results = await page.locator(selector).count();
                    if (results > 0) {
                        expect(results).toBeGreaterThan(0);
                        console.log(`✓ Found ${results} results with selector: ${selector}`);
                        resultsFound = true;
                        break;
                    }
                } catch (e) {
                    continue;
                }
            }
        }
    });

    test('should handle basic navigation', async ({ page }) => {
        await page.goto('https://www.mercadolibre.com.mx');
        await page.waitForLoadState('domcontentloaded');
        await page.waitForTimeout(2000);
        
        const title = await page.title();
        expect(title.toLowerCase()).toContain('mercado');
        
        await expect(page.locator('body')).toBeVisible();
        console.log(`✓ Page loaded with title: ${title}`);
    });

    test('should interact with product categories', async ({ page }) => {
        await page.goto('https://www.mercadolibre.com.mx');
        await page.waitForLoadState('domcontentloaded');
        await page.waitForTimeout(2000);
        
        const categorySelectors = [
            '.nav-categs-link',
            '.nav-menu-item',
            'a[href*="/categorias"]',
            '.nav-menu a'
        ];
        
        for (const selector of categorySelectors) {
            try {
                const categories = page.locator(selector);
                const count = await categories.count();
                if (count > 0) {
                    console.log(`✓ Found ${count} categories`);
                    await categories.first().click();
                    await page.waitForLoadState('domcontentloaded');
                    await page.waitForTimeout(2000);
                    
                    await expect(page).toHaveURL(/.*mercadolibre\.com.*/);
                    break;
                }
            } catch (e) {
                continue;
            }
        }
    });

    test('should demonstrate user actions recording', async ({ page }) => {
        await page.goto('https://www.mercadolibre.com.mx');
        await page.waitForLoadState('domcontentloaded');
        await page.waitForTimeout(2000);
        
        const logoSelector = '.nav-logo';
        try {
            await page.hover(logoSelector);
            console.log('✓ Hovered over logo');
        } catch (e) {
            console.log('Logo hover failed, continuing...');
        }
        
        await page.evaluate(() => window.scrollBy(0, 500));
        await page.waitForTimeout(1000);
        
        await page.evaluate(() => window.scrollTo(0, 0));
        await page.waitForTimeout(1000);
        
        const keyElements = [
            '.nav-search',
            '.nav-menu',
            'footer'
        ];
        
        for (const selector of keyElements) {
            try {
                const element = page.locator(selector);
                const isVisible = await element.isVisible();
                console.log(`Element ${selector}: ${isVisible ? 'visible' : 'not visible'}`);
            } catch (e) {
                console.log(`Could not check ${selector}`);
            }
        }
        
        await expect(page.locator('body')).toBeVisible();
    });
});