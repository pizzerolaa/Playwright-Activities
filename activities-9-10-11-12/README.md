# Playwright Activities 9-10-11-12

## Estructura del Proyecto

```
activities-9-10-11-12/
├── .gitignore
├── package.json
├── playwright.config.ts
├── tsconfig.json
├── Readme.md
├── Actividad1/
│   └── weather.html              # App de clima para Activity 2
├── tests/
│   ├── activity1.spec.ts         # Tests parametrizados de login GitHub
│   ├── activity2.spec.ts         # Tests con grabación de video
│   ├── activity3.spec.ts         # Tests generados con Codegen
│   └── activity4.spec.ts         # Tests generados con Inspector
├── playwright-report/            # Reportes HTML generados
└── test-results/                 # Screenshots, videos y traces
```

## Instalación y Configuración

### 1. Instalación de dependencias
```bash
npm install
```

### 2. Instalar navegadores de Playwright
```bash
npx playwright install
```

### 3. Verificar instalación
```bash
npx playwright --version
```

## Actividades del Proyecto

### Activity 1: Tests Parametrizados de Login GitHub
**Objetivo:** Crear tests parametrizados con usuarios falsos para GitHub login

```bash
# Ejecutar Activity 1
npx playwright test activity1.spec.ts

# Ejecutar con interfaz visual
npx playwright test activity1.spec.ts --headed

# Ejecutar solo en Chrome
npx playwright test activity1.spec.ts --project=chromium
```

### Activity 2: Grabación de Video - Weather App
**Objetivo:** Simular weather.html y grabar videos de los tests

```bash
# Ejecutar Activity 2 con grabación de video
npx playwright test activity2.spec.ts --headed

# Solo grabar videos cuando fallan
npx playwright test activity2.spec.ts --project=chromium

# Ver videos generados en: test-results/*/video.webm
```

**Nota:** Los videos se guardan automáticamente en la carpeta `test-results/`

### Activity 3: Tests con Playwright Codegen
**Objetivo:** Generar tests usando Playwright Codegen en GitHub

```bash
# Ejecutar Activity 3
npx playwright test activity3.spec.ts

# Para generar nuevos tests con Codegen:
npx playwright codegen https://github.com/microsoft/playwright

# Ejecutar con debug
npx playwright test activity3.spec.ts --headed --slowMo=1000
```

### Activity 4: Tests con Playwright Inspector
**Objetivo:** Grabar acciones de usuario en MercadoLibre usando Inspector

```bash
# Ejecutar Activity 4
npx playwright test activity4.spec.ts

# Para usar Inspector (modo debug):
npx playwright test activity4.spec.ts --debug

# Ejecutar solo en un navegador
npx playwright test activity4.spec.ts --project=chromium --headed
```