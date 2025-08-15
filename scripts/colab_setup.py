#!/usr/bin/env python3
"""
Automated Colab Setup for Vencord Discord Bot
This script automatically sets up a Colab environment with Discord + Vencord
"""

import os
import time
import json
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class ColabAutomation:
    def __init__(self):
        self.driver = None
        self.colab_url = None
        
    def setup_driver(self):
        """Set up Chrome driver with manual sign-in support"""
        try:
            # Install Chrome and ChromeDriver manually
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "wget", "unzip"], check=True)
            
            # Download and install Chrome
            subprocess.run(["wget", "-q", "-O", "-", "https://dl.google.com/linux/linux_signing_key.pub"], 
                        stdout=subprocess.PIPE, check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "google-chrome-stable"], check=True)
            
            # Download ChromeDriver
            subprocess.run(["wget", "-O", "chromedriver.zip", 
                        "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/139.0.7258.66/linux64/chromedriver-linux64.zip"], check=True)
            subprocess.run(["unzip", "chromedriver.zip"], check=True)
            subprocess.run(["chmod", "+x", "chromedriver-linux64/chromedriver"], check=True)
            subprocess.run(["sudo", "mv", "chromedriver-linux64/chromedriver", "/usr/local/bin/"], check=True)
            
            # Set up Chrome options with unique user data directory
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data-" + str(int(time.time())))
            chrome_options.add_argument("--remote-debugging-port=9222")
            
            # Create service with explicit path
            service = Service("/usr/local/bin/chromedriver")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            print("✅ Chrome driver setup completed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up Chrome driver: {e}")
            return False
        
    def create_colab_notebook(self):
        """Create a new Colab notebook with manual sign-in support"""
        try:
            # Go to Colab
            self.driver.get("https://colab.research.google.com/")
            time.sleep(5)
            
            # Check if signed in
            try:
                # Look for sign-in button
                sign_in_btn = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Sign in')]")
                if sign_in_btn:
                    print("=" * 60)
                    print("🔐 MANUAL SIGN-IN REQUIRED")
                    print("=" * 60)
                    print("Please sign in to your Google account in the browser window.")
                    print("The automation will wait for you to complete sign-in.")
                    print("=" * 60)
                    
                    # Wait for user to sign in manually
                    while True:
                        try:
                            # Check if we're now signed in by looking for user avatar or notebook creation options
                            signed_in_indicators = [
                                "//*[contains(text(), 'NEW NOTEBOOK')]",
                                "//*[contains(text(), 'File')]",
                                "//*[contains(text(), 'Runtime')]",
                                "//*[contains(text(), 'Tools')]"
                            ]
                            
                            signed_in = False
                            for indicator in signed_in_indicators:
                                if self.driver.find_elements(By.XPATH, indicator):
                                    signed_in = True
                                    break
                            
                            if signed_in:
                                print("✅ Sign-in detected! Proceeding with automation...")
                                break
                            
                            # Also check if sign-in button is gone
                            if not self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Sign in')]"):
                                print("✅ Sign-in button disappeared, proceeding...")
                                break
                            
                            print("⏳ Waiting for sign-in... (check browser window)")
                            time.sleep(10)
                            
                        except Exception as e:
                            print(f"⏳ Still waiting for sign-in... ({e})")
                            time.sleep(10)
                    
                    # Give extra time for page to fully load after sign-in
                    print("�� Page loading after sign-in...")
                    time.sleep(10)
                    
            except:
                print("✅ Already signed in or sign-in not required")
            
            # Now create new notebook via File menu
            print("📝 Creating new notebook...")
            try:
                # Try File menu approach first
                file_menu = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'File')]"))
                )
                print("📁 Found File menu, clicking...")
                file_menu.click()
                time.sleep(3)
                
                # Look for "New notebook" option
                new_notebook_option = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'New notebook')]"))
                )
                print("�� Found New notebook option, clicking...")
                new_notebook_option.click()
                time.sleep(15)
                
            except Exception as e:
                print(f"⚠️ File menu approach failed: {e}")
                print("�� Trying alternative method...")
                
                # Alternative: try direct new notebook URL
                try:
                    self.driver.get("https://colab.research.google.com/notebooks/create")
                    time.sleep(15)
                    print("✅ Used direct URL method")
                except Exception as fallback_error:
                    print(f"❌ Fallback also failed: {fallback_error}")
                    return False
            
            # Wait for code cells to appear
            print("🔍 Waiting for code cells to load...")
            try:
                WebDriverWait(self.driver, 45).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.codecell-input"))
                )
                print("✅ Code cells found - new notebook created successfully!")
            except Exception as e:
                print(f"❌ No code cells found: {e}")
                return False
            
            # Get the new notebook URL
            self.colab_url = self.driver.current_url
            print(f"🔗 New notebook URL: {self.colab_url}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating notebook: {e}")
            return False
            
    def install_discord_vencord(self):
        """Install Discord and Vencord in Colab"""
        try:
            # Wait for code cell to be ready
            code_cell = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.codecell-input"))
            )
            
            # Install Discord and Vencord
            install_script = '''
# Install Discord desktop
!wget -O discord.deb "https://discord.com/api/downloads/distro/app/linux/x64/stable"
!dpkg -i discord.deb
!apt install -f -y

# Install Vencord dependencies
!apt update
!apt install -y git nodejs npm
!npm install -g npm@latest

# Clone and build Vencord
!git clone https://github.com/Vendicated/Vencord.git
%cd Vencord
!npm install
!npm run build

print("Discord and Vencord installed successfully!")
'''
            
            # Execute the installation
            self.driver.execute_script(f"""
                var cell = document.querySelector('.codecell-input');
                var textarea = cell.querySelector('textarea');
                textarea.value = `{install_script}`;
                textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
            """)
            
            # Run the cell
            run_btn = self.driver.find_element(By.CSS_SELECTOR, "button.run-button")
            run_btn.click()
            
            # Wait for installation to complete
            time.sleep(120)  # 2 minutes for installation
            
            print("Discord and Vencord installation completed")
            return True
            
        except Exception as e:
            print(f"Error during installation: {e}")
            return False
            
    def setup_plugin(self):
        """Set up the notifyServerJoins plugin"""
        try:
            # Create plugin directory and file
            plugin_script = '''# Create plugin directory
!mkdir -p src/userplugins/notifyServerJoins

# Create the plugin file
plugin_code = """/*
 * Vencord, a Discord client mod
 * Copyright (c) 2025 Emediong Francis
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

import { definePluginSettings } from "@api/Settings";
import { sendMessage } from "@utils/discord";
import definePlugin, { OptionType } from "@utils/types";
import { FluxDispatcher, GuildStore } from "@webpack/common";

const settings = definePluginSettings({
    channelId: {
        description: "Channel ID to send notifications to",
        type: OptionType.STRING,
        default: "''' + os.getenv('DISCORD_CHANNEL_ID', 'YOUR_CHANNEL_ID_HERE') + '''"
    }
});

let lastSent = 0;
function rateLimitedSend(channelId: string, content: string) {
    const now = Date.now();
    if (now - lastSent < 2000) {
        console.log("Rate limiter: message skipped.");
        return;
    }
    lastSent = now;
    console.log("Sending message:", content, "to channel:", channelId);
    sendMessage(channelId, { content });
}

function onMemberJoin(event: any) {
    console.log("onMemberJoin called:", event);
    const { channelId } = settings.store;
    if (!channelId) {
        console.log("No channelId set in settings.");
        return;
    }

    const username =
        event.user?.globalName ||
        event.user?.username ||
        "Unknown User";
    let guildName = event.guildId;
    try {
        const guilds = GuildStore.getGuilds?.();
        console.log("Guilds from GuildStore:", guilds);
        if (guilds && guilds[event.guildId]?.name) {
            guildName = guilds[event.guildId].name;
        }
    } catch (err) {
        console.log("Error getting guild name:", err);
    }

    const message = `🟢 **${username}** joined **${guildName}**`;
    rateLimitedSend(channelId, message);
}

export default definePlugin({
    name: "notifyServerJoins",
    description: "Notify when a user joins a server by sending a message to a designated channel.",
    authors: [{ name: "Emediong Francis", id: 4723456780n }],
    settings,
    start() {
        console.log("Subscribing to GUILD_MEMBER_ADD event via FluxDispatcher.");
        FluxDispatcher.subscribe("GUILD_MEMBER_ADD", onMemberJoin);
    },
    stop() {
        console.log("Unsubscribing from GUILD_MEMBER_ADD event via FluxDispatcher.");
        FluxDispatcher.unsubscribe("GUILD_MEMBER_ADD", onMemberJoin);
    }
});"""

with open('src/userplugins/notifyServerJoins/index.ts', 'w') as f:
    f.write(plugin_code)

print("Plugin file created successfully!")
'''
            
            # Execute plugin setup
            self.driver.execute_script(f"""
                var cell = document.querySelector('.codecell-input');
                var textarea = cell.querySelector('textarea');
                textarea.value = `{plugin_script}`;
                textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
            """)
            
            # Run the cell
            run_btn = self.driver.find_element(By.CSS_SELECTOR, "button.run-button")
            run_btn.click()
            
            time.sleep(30)
            print("Plugin setup completed")
            return True
            
        except Exception as e:
            print(f"Error setting up plugin: {e}")
            return False
            
    def start_discord(self):
        """Start Discord in Colab"""
        try:
            start_script = '''
# Start Discord
!discord &
print("Discord started successfully!")
'''
            
            # Execute start script
            self.driver.execute_script(f"""
                var cell = document.querySelector('.codecell-input');
                var textarea = cell.querySelector('textarea');
                textarea.value = `{start_script}`;
                textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
            """)
            
            # Run the cell
            run_btn = self.driver.find_element(By.CSS_SELECTOR, "button.run-button")
            run_btn.click()
            
            time.sleep(30)
            print("Discord started successfully")
            return True
            
        except Exception as e:
            print(f"Error starting Discord: {e}")
            return False
            
    def run(self):
        """Main execution flow"""
        try:
            print("Starting Colab automation...")
            
            # Setup Chrome driver
            self.setup_driver()
            
            # Create notebook
            if not self.create_colab_notebook():
                return False
                
            # Install Discord and Vencord
            if not self.install_discord_vencord():
                return False
                
            # Setup plugin
            if not self.setup_plugin():
                return False
                
            # Start Discord
            if not self.start_discord():
                return False
                
            print(f"Setup completed successfully! Colab URL: {self.colab_url}")
            
            # Save URL to file for GitHub Actions
            with open('colab_url.txt', 'w') as f:
                f.write(self.colab_url)
                
            return True
            
        except Exception as e:
            print(f"Automation failed: {e}")
            return False
            
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    automation = ColabAutomation()
    success = automation.run()
    exit(0 if success else 1)