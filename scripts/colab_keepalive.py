#!/usr/bin/env python3
"""
Colab Keep-Alive Script
Keeps the Colab session active and monitors Discord status
"""

import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class ColabKeepAlive:
    def __init__(self):
        self.driver = None
        self.colab_url = os.getenv('COLAB_URL')
        
    def setup_driver(self):
        """Set up Chrome driver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def check_session_status(self):
        """Check if Colab session is still active"""
        try:
            self.driver.get(self.colab_url)
            
            # Check for session timeout message
            timeout_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'timeout') or contains(text(), 'disconnected')]")
            
            if timeout_elements:
                print("Session timeout detected, reconnecting...")
                return False
                
            # Check if Discord is still running
            discord_status = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Discord started successfully')]")
            
            if not discord_status:
                print("Discord not running, restarting...")
                return False
                
            print("Session is healthy")
            return True
            
        except Exception as e:
            print(f"Error checking session: {e}")
            return False
            
    def reconnect_session(self):
        """Reconnect the Colab session"""
        try:
            print("Reconnecting Colab session...")
            
            # Go to Colab
            self.driver.get("https://colab.research.google.com/")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )
            
            # Create new notebook
            new_notebook_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'NEW NOTEBOOK')]"))
            )
            new_notebook_btn.click()
            
            time.sleep(5)
            
            # Quick setup script
            quick_setup = '''
# Quick Discord + Vencord setup
!wget -O discord.deb "https://discord.com/api/downloads/distro/app/linux/x64/stable"
!dpkg -i discord.deb
!apt install -f -y
!apt install -y git nodejs npm
!git clone https://github.com/Vendicated/Vencord.git
%cd Vencord
!npm install
!npm run build

# Setup plugin
!mkdir -p src/userplugins/notifyServerJoins
# Plugin code would go here...

# Start Discord
!discord &
print("Quick setup completed!")
'''
            
            # Execute quick setup
            self.driver.execute_script(f"""
                var cell = document.querySelector('.codecell-input');
                var textarea = cell.querySelector('textarea');
                textarea.value = `{quick_setup}`;
                textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
            """)
            
            # Run the cell
            run_btn = self.driver.find_element(By.CSS_SELECTOR, "button.run-button")
            run_btn.click()
            
            time.sleep(120)
            print("Reconnection completed")
            return True
            
        except Exception as e:
            print(f"Error reconnecting: {e}")
            return False
            
    def run(self):
        """Main keep-alive loop"""
        try:
            if not self.colab_url:
                print("No Colab URL provided")
                return False
                
            self.setup_driver()
            
            while True:
                if not self.check_session_status():
                    self.reconnect_session()
                    
                # Wait 30 minutes before next check
                time.sleep(1800)
                
        except KeyboardInterrupt:
            print("Keep-alive stopped by user")
        except Exception as e:
            print(f"Keep-alive error: {e}")
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    keepalive = ColabKeepAlive()
    keepalive.run()
