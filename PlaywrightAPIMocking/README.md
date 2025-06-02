# Mocking de API con Playwright

Este repo contiene la actividad en clase del dia 02 de junio de 2025 de mocking de API utilizando Playwright para tres actividades diferentes:

1. Simulación de peticiones a una API de clima
2. Modificación de respuestas de API para una lista de personajes de Harry Potter
3. Mocking con archivos HAR

## Requisitos previos

- Node.js (versión 16 o superior)
- npm (incluido con Node.js)
- Visual Studio Code (recomendado)
- Extensión Live Server para VS Code

## Instalación

1. Clona o descarga este repo
2. Instala las dependencias:

```bash
npm install
```

3. Instala los navegadores necesarios para Playwright:

```bash
npx playwright install
```

## Estructura del proyecto

```
PlaywrightAPIMocking/
├── Actividad1/
│   └── weather.html             # Aplicación del clima para la Actividad 1
├── Actividad2/
│   └── harry-potter-list.html   # Lista de personajes para la Actividad 2
├── tests/
│   ├── weather.spec.ts          # Tests para la Actividad 1
│   ├── harry-potter.spec.ts     # Tests para la Actividad 2
│   ├── record-har.js            # Script para grabar archivo HAR
│   └── har-replay.spec.ts       # Tests con archivo HAR para la Actividad 3
├── harry-potter-api.har         # Archivo HAR grabado (generado al ejecutar record-har.js)
├── package.json
├── playwright.config.js
└── tsconfig.json
```

## Ejecutar las pruebas

### Preparación

1. Abre el proyecto en Visual Studio Code
2. Inicia el servidor Live Server:
   - Haz clic derecho en el archivo HTML que deseas servir
   - Selecciona "Open with Live Server"
   - El servidor se iniciará en http://127.0.0.1:5500 (o un puerto similar)

> **Nota importante**: La URL del servidor Live Server puede variar dependiendo de tu configuración. Si no es `http://127.0.0.1:5500`, deberás ajustar las URLs en los archivos de prueba.

### Actividad 1: Mock API requests (Clima)

1. Abre `Actividad1/weather.html` con Live Server
2. Ejecuta las pruebas:

```bash
npx playwright test weather.spec.ts
```

Este test:
- Simula una respuesta exitosa para la búsqueda del clima de París
- Simula un error 500 y verifica el manejo de errores

### Actividad 2: Modifying API response (Harry Potter)

1. Abre `Actividad2/harry-potter-list.html` con Live Server
2. Ejecuta las pruebas:

```bash
npx playwright test harry-potter.spec.ts
```

Este test:
- Modifica la respuesta de la API para insertar un personaje personalizado
- Modifica la respuesta para eliminar un personaje

### Actividad 3: Mocking with HAR Files

1. Primero, graba un archivo HAR:

```bash
node tests/record-har.js
```

> **Nota**: Asegúrate de que `Actividad2/harry-potter-list.html` esté abierto con Live Server al ejecutar este comando.

2. Ejecuta las pruebas con el archivo HAR:

```bash
npx playwright test har-replay.spec.ts
```

Este test:
- Reproduce las respuestas desde el archivo HAR sin modificaciones
- Modifica el archivo HAR en memoria y usa la respuesta modificada

## Ajustar la URL del servidor

Si tu servidor Live Server utiliza una URL diferente a `http://127.0.0.1:5500`, deberás modificar las URLs en los archivos de prueba:

1. Abre los archivos `.spec.ts` en la carpeta `tests/`
2. Busca todas las instancias de `http://127.0.0.1:5500` y reemplázalas con tu URL
3. También deberás ajustar la URL en `tests/record-har.js`

## Ver los resultados de las pruebas

Para ver un informe detallado de las pruebas:

```bash
npx playwright show-report
```

## Solución de problemas

### Error al ejecutar archivos TypeScript

Si obtienes un error como `Unknown file extension ".ts"` al intentar ejecutar directamente un archivo TypeScript, utiliza alguna de estas soluciones:

1. Usar ts-node:
```bash
npx ts-node tests/archivo.ts
```

2. Usar Playwright test (para archivos de prueba):
```bash
npx playwright test tests/archivo.spec.ts
```

### Error de conexión al servidor

Si los tests fallan con errores de conexión, verifica:
1. Que el servidor Live Server esté funcionando
2. Que las URLs en los tests coincidan con tu servidor
3. Que no haya problemas de red o firewall bloqueando las conexiones
