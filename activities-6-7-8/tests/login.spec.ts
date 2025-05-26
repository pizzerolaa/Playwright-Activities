import { test, expect } from '@playwright/test';
import * as path from 'path';

const htmlPath = path.resolve(__dirname, '../test-isolation/login.html');
const fileUrl = `file://${htmlPath.replace(/\\/g, '/')}`;

test.describe('Login functionality', () => {
  test('should login successfully and update localStorage', async ({ page }) => {
    await page.goto(fileUrl);
    
    //verificar que inicialmente no está logueado
    const statusElement = page.locator('#status');
    await expect(statusElement).toHaveText('Not logged in');
    
    //hacer click en el botón de login
    await page.click('#login');
    
    //verificar que el texto cambia correctamente
    await expect(statusElement).toHaveText('Logged in as admin');
    
    //verificar el valor en localStorage usando page.evaluate()
    const userValue = await page.evaluate(() => {
      return localStorage.getItem('user');
    });
    
    expect(userValue).toBe('admin');
  });

  test('should show not logged in status when localStorage is empty', async ({ page, context }) => {
    //crear un nuevo contexto para este test para asegurar aislamiento
    const browser = context.browser();
    if (!browser) throw new Error('Browser instance not available');
    const newContext = await browser.newContext();
    const newPage = await newContext.newPage();
    
    try {
      await newPage.goto(fileUrl);
      
      //verificar que el estado muestra "Not logged in"
      const statusElement = newPage.locator('#status');
      await expect(statusElement).toHaveText('Not logged in');
    } finally {
      await newContext.close();
    }
  });
});