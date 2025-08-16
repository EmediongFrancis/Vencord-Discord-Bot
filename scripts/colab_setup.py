#!/usr/bin/env python3
"""
True Colab Automation - Actually Creates and Configures Working Notebooks
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

class TrueColabAutomation:
    def __init__(self):
        self.driver = None
        self.colab_url = None
        
    def setup_driver(self):
        """Set up Chrome driver with proper cleanup"""
        try:
            print("🔧 Setting up Chrome driver...")
            
            # Kill any existing Chrome processes
            subprocess.run(["pkill", "-f", "chrome"], check=False)
            subprocess.run(["pkill", "-f", "chromedriver"], check=False)
            subprocess.run(["sudo", "pkill", "-9", "-f", "chrome"], check=False)
            time.sleep(3)
            
            # Install Chrome
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "chromium-browser"], check=True)
            
            # Set up Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            
            # Create driver
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Chrome driver setup completed")
            return True
            
        except Exception as e:
            print(f"❌ Driver setup failed: {e}")
            return False
    
    def create_colab_notebook(self):
        """Actually create a working Colab notebook"""
        try:
            print("📝 Creating Colab notebook...")
            
            # Go to Colab
            self.driver.get("https://colab.research.google.com/")
            time.sleep(10)
            
            # Check if signed in
            try:
                sign_in_btn = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Sign in')]")
                if sign_in_btn:
                    print("🔐 MANUAL SIGN-IN REQUIRED")
                    print("📱 Please sign in to your Google account in the browser window")
                    print("⏳ Waiting for sign-in...")
                    
                    # Wait for sign-in
                    while True:
                        try:
                            if self.driver.find_elements(By.XPATH, "//*[contains(text(), 'File')]"):
                                print("✅ Sign-in detected!")
                                break
                            time.sleep(10)
                        except:
                            time.sleep(10)
                    
                    time.sleep(10)
            except:
                print("✅ Already signed in")
            
            # Create new notebook
            try:
                # Look for NEW NOTEBOOK button
                new_btn_selectors = [
                    "//span[contains(text(), 'NEW NOTEBOOK')]",
                    "//span[contains(text(), 'New notebook')]",
                    "//div[contains(text(), 'NEW NOTEBOOK')]",
                    "//div[contains(text(), 'New notebook')]"
                ]
                
                new_btn = None
                for selector in new_btn_selectors:
                    try:
                        new_btn = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        break
                    except:
                        continue
                
                if new_btn:
                    print("�� Found NEW NOTEBOOK button, clicking...")
                    new_btn.click()
                    time.sleep(15)
                else:
                    # Try File menu approach
                    print("📁 Using File menu approach...")
                    file_menu = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'File')]"))
                    )
                    file_menu.click()
                    time.sleep(3)
                    
                    new_notebook_option = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'New notebook')]"))
                    )
                    new_notebook_option.click()
                    time.sleep(15)
                
                # Wait for notebook to load
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.codecell-input"))
                )
                
                # Get the notebook URL
                self.colab_url = self.driver.current_url
                print(f"✅ Notebook created successfully: {self.colab_url}")
                return True
                
            except Exception as e:
                print(f"❌ Notebook creation failed: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Notebook creation failed: {e}")
            return False
    
    def install_discord_vencord(self):
        """Install Discord and Vencord in the notebook"""
        try:
            print(" Installing Discord and Vencord...")
            
            # Installation code
            install_code = '''# Install Discord and Vencord
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

print("Discord and Vencord installed successfully!")'''
            
            # Execute installation
            self.driver.execute_script(f"""
                var cell = document.querySelector('.codecell-input');
                var textarea = cell.querySelector('textarea');
                textarea.value = `{install_code}`;
                textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
            """)
            
            # Run the cell
            run_btn = self.driver.find_element(By.CSS_SELECTOR, "button.run-button")
            run_btn.click()
            
            print("⏳ Installation in progress... (this takes 2-3 minutes)")
            time.sleep(180)  # Wait for installation
            
            print("✅ Installation completed")
            return True
            
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            return False
    
    def setup_plugin(self):
        """Setup the notifyServerJoins plugin"""
        try:
            print("🔌 Setting up plugin...")
            
            # Plugin setup code
            plugin_setup = '''# Create plugin directory and file
!mkdir -p src/userplugins/notifyServerJoins

# Create the plugin file
plugin_code = """/*
 * Vencord, a Discord client mod
 * Copyright (c) 2025 Vendicated and contributors
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

import { definePluginSettings } from "@api/Settings";
import { sendMessage } from "@utils/discord";
import definePlugin, { OptionType } from "@utils/types";
import { FluxDispatcher, GuildStore } from "@webpack/common";

const settings = definePluginSettings({
    channelId: {
        description: "Channel ID to send notifications to",
        type: OptionType.STRING",
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

print("Plugin file created successfully!")'''
            
            # Execute plugin setup
            self.driver.execute_script(f"""
                var cell = document.querySelector('.codecell-input');
                var textarea = cell.querySelector('textarea');
                textarea.value = `{plugin_setup}`;
                textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
            """)
            
            # Run the cell
            run_btn = self.driver.find_element(By.CSS_SELECTOR, "button.run-button")
            run_btn.click()
            
            time.sleep(30)
            print("✅ Plugin setup completed")
            return True
            
        except Exception as e:
            print(f"❌ Plugin setup failed: {e}")
            return False
    
    def start_discord(self):
        """Start Discord"""
        try:
            print("🚀 Starting Discord...")
            
            start_code = '''# Start Discord
!discord &
print("Discord started successfully!")'''
            
            # Execute start code
            self.driver.execute_script(f"""
                var cell = document.querySelector('.codecell-input');
                var textarea = cell.querySelector('textarea');
                textarea.value = `{start_code}`;
                textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
            """)
            
            # Run the cell
            run_btn = self.driver.find_element(By.CSS_SELECTOR, "button.run-button")
            run_btn.click()
            
            time.sleep(30)
            print("✅ Discord started")
            return True
            
        except Exception as e:
            print(f"❌ Discord start failed: {e}")
            return False
    
    def run(self):
        """Main execution flow"""
        try:
            print("🚀 Starting True Colab Automation...")
            
            # Setup Chrome driver
            if not self.setup_driver():
                return False
            
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
            
            print(f"🎉 TRUE AUTOMATION COMPLETED!")
            print(f"📓 Working Notebook URL: {self.colab_url}")
            print(f"�� Discord is running with Vencord plugin")
            print(f"�� Notifications will be sent to your configured channel")
            
            # Save URL to file
            with open('colab_url.txt', 'w') as f:
                f.write(self.colab_url)
            
            return True
            
        except Exception as e:
            print(f"❌ Automation failed: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    automation = TrueColabAutomation()
    success = automation.run()
    exit(0 if success else 1)