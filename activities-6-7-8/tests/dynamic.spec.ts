import { test, expect } from '@playwright/test';
import * as path from 'path';

const htmlPath = path.resolve(__dirname, '../dynamic-form/dynamic-form.html');
const fileUrl = `file://${htmlPath.replace(/\\/g, '/')}`;

test.describe('Dynamic Form', () => {
  test('should complete the entire form flow with auto-waiting', async ({ page }) => {
    await page.goto(fileUrl);
    
    //verificamos que el formulario inicialmente no es visible
    const form = page.locator('#form');
    await expect(form).toBeHidden();
    
    const startButton = page.locator('#start');
    await startButton.click();
    
    //verificamos que el formulario es visible después de hacer clic
    await expect(form).toBeVisible();
    
    //verificar que el botón "Next" está inicialmente deshabilitado
    const nextButton = page.locator('#next');
    await expect(nextButton).toBeDisabled();
    
    const nameInput = page.locator('#name');
    await nameInput.fill('Usuario de Prueba');
    
    //verificamos que el botón "next" ahora está habilitado
    await expect(nextButton).toBeEnabled();
    await nextButton.click();
    
    //verificar que el loader aparece
    const loader = page.locator('#loader');
    await expect(loader).toBeVisible();
    
    //verificar que el select no es visible mientras el loader está activo
    const select = page.locator('#options');
    await expect(select).toBeHidden();
    
    //esperar a que el loader desaparezca (usando auto-waiting)
    await expect(loader).toBeHidden();
    
    //verificar que el select ahora es visible y tiene opciones
    await expect(select).toBeVisible();
    await select.selectOption('2');
    await expect(select).toHaveValue('2');
  });
});