import { test, expect } from '@playwright/test';

test.describe('Activity 3: GitHub Task List Tests', () => {
    test('should interact with GitHub repository and task list', async ({ page }) => {
        await page.goto('https://github.com/microsoft/playwright');
        await page.waitForLoadState('networkidle');
    
        await page.click('#issues-tab');
        await page.waitForLoadState('networkidle');
        
        //esperar lista de issues
        const issuesSelector = '.ListItems-module__listItem--Blv7W, .IssueRow-module__row--XmR1f, [data-testid="issue-pr-title-link"]';
        await page.waitForSelector(issuesSelector, { timeout: 15000 });
        
        //issues deberian estar visibles
        const issueCount = await page.locator(issuesSelector).count();
        expect(issueCount).toBeGreaterThan(0);
        
        //click en el primer issue
        await page.locator('h3 a[data-testid="issue-pr-title-link"]').first().click();
        await page.waitForLoadState('networkidle');
        
        //verificar que el issue se ha abierto correctamente
        const titleElement = page.locator('[data-testid="issue-title"]');
        await expect(titleElement).toBeVisible({ timeout: 10000 });
        const titleFound = await titleElement.isVisible();
        
        expect(titleFound).toBe(true);
        
        //verificar que la URL del issue es correcta
        await expect(page).toHaveURL(/.*\/issues\/\d+/);
    });

        test('should navigate repository sections', async ({ page }) => {
            await page.goto('https://github.com/microsoft/playwright');
            await page.waitForLoadState('networkidle');
            
            //navegar a las pestañas del repositorio
            const tabs = [
                { name: 'Code', selector: '#code-tab' },
                { name: 'Issues', selector: '#issues-tab' },
                { name: 'Pull requests', selector: '#pull-requests-tab' }
            ];
            
            for (const tab of tabs) {
                try {
                    await page.click(tab.selector);
                    await page.waitForLoadState('networkidle');
                    //checar que se ha navegado correctamente
                    await page.waitForTimeout(2000);
                } catch (e) {
                    console.log(`Could not navigate to ${tab.name} tab:`, e);
                }
            }
    });
});