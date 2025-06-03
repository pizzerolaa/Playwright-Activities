#!/usr/bin/env python3
"""
Continuación de la verificación manual para casos pendientes
"""

import requests
from bs4 import BeautifulSoup
import json
import time

class CompleteVerification:
    def __init__(self, base_url="http://localhost"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def login(self):
        """Login a DVWA"""
        login_url = f"{self.base_url}/login.php"
        response = self.session.get(login_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_input = soup.find('input', {'name': 'user_token'})
        csrf_token = csrf_input.get('value', '') if csrf_input else ''
        
        login_data = {
            'username': 'admin',
            'password': 'password',
            'Login': 'Login'
        }
        if csrf_token:
            login_data['user_token'] = csrf_token
            
        response = self.session.post(login_url, data=login_data)
        return "Welcome to Damn Vulnerable Web Application" in response.text
    
    def verify_sql_injection_impossible(self):
        """Investigar específicamente SQL Injection nivel Impossible"""
        print(f"\n🔍 INVESTIGACIÓN ESPECIAL: SQL Injection Impossible")
        print("=" * 60)
        
        self.set_security_level('impossible')
        
        sqli_url = f"{self.base_url}/vulnerabilities/sqli/"
        
        # Obtener página inicial
        response = self.session.get(sqli_url)
        print(f"📝 Página inicial: {len(response.text)} chars")
        
        # Verificar si la página funciona diferente en Impossible
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')
        
        if form:
            print("✅ Formulario encontrado")
        else:
            print("⚠️ No se encontró formulario - posible implementación diferente")
        
        # Probar diferentes enfoques
        test_cases = [
            {'id': '1', 'description': 'Input normal'},
            {'id': "1' OR '1'='1", 'description': 'SQL Injection básico'},
            {'id': '1 UNION SELECT 1,2', 'description': 'UNION attack'},
            {'id': 'abc', 'description': 'Input no numérico'},
        ]
        
        for test in test_cases:
            print(f"\n🧪 Probando: {test['description']}")
            print(f"   Input: {test['id']}")
            
            # Obtener token fresco
            response = self.session.get(sqli_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_input = soup.find('input', {'name': 'user_token'})
            csrf_token = csrf_input.get('value', '') if csrf_input else ''
            
            # Enviar datos
            data = {
                'id': test['id'],
                'Submit': 'Submit'
            }
            if csrf_token:
                data['user_token'] = csrf_token
            
            response = self.session.post(sqli_url, data=data)
            
            # Analizar respuesta
            users_count = response.text.count('First name:')
            surnames_count = response.text.count('Surname:')
            
            print(f"   Respuesta: {users_count} usuarios, {surnames_count} apellidos")
            print(f"   Tamaño: {len(response.text)} chars")
            
            # Buscar patrones específicos
            if 'password' in response.text.lower():
                print(f"   ⚠️ Contiene 'password'")
            if re.search(r'[a-f0-9]{32,64}', response.text):
                print(f"   ⚠️ Contiene posibles hashes")
            if 'error' in response.text.lower():
                print(f"   ⚠️ Contiene errores")
                
        print(f"\n📊 CONCLUSIÓN:")
        print(f"SQL Injection Impossible requiere análisis de código fuente")
        print(f"para determinar implementación exacta.")
    
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
        time.sleep(1)

if __name__ == "__main__":
    print("🔍 Verificación Completa DVWA")
    print("=" * 50)
    
    verifier = CompleteVerification()
    
    if verifier.login():
        print("✅ Login exitoso")
        verifier.verify_sql_injection_impossible()
    else:
        print("❌ Error en login")