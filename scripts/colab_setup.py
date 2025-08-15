#!/usr/bin/env python3
"""
Colab API-based Setup for Vencord Discord Bot
Uses Colab's REST API instead of browser automation
"""

import os
import time
import json
import requests
import subprocess
from urllib.parse import urlparse, parse_qs

class ColabAPIAutomation:
    def __init__(self):
        self.session = requests.Session()
        self.colab_url = None
        self.notebook_id = None
        
    def setup_colab_api(self):
        """Set up Colab API session"""
        try:
            print("🔧 Setting up Colab API...")
            
            # Install required packages
            subprocess.run(["pip", "install", "google-colab", "google-auth", "google-auth-oauthlib"], check=True)
            
            # Set up Google authentication
            from google.colab import auth
            from google.auth import default
            
            print("🔐 Authenticating with Google...")
            auth.authenticate_user()
            
            # Get credentials
            creds, project = default()
            print("✅ Google authentication successful")
            
            return True
            
        except Exception as e:
            print(f"❌ API setup failed: {e}")
            return False
    
    def create_notebook_via_api(self):
        """Create a new notebook using Colab API"""
        try:
            print("📝 Creating new notebook via API...")
            
            # Use Colab's notebook creation endpoint
            create_url = "https://colab.research.google.com/api/notebooks/create"
            
            # Set up headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            # Create notebook
            response = self.session.post(create_url, headers=headers)
            
            if response.status_code == 200:
                notebook_data = response.json()
                self.notebook_id = notebook_data.get('notebook_id')
                self.colab_url = f"https://colab.research.google.com/drive/{self.notebook_id}"
                print(f"✅ Notebook created: {self.colab_url}")
                return True
            else:
                print(f"❌ Failed to create notebook: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ API notebook creation failed: {e}")
            return False
    
    def install_discord_vencord(self):
        """Install Discord and Vencord using Colab API"""
        try:
            print("�� Installing Discord and Vencord...")
            
            # Prepare installation code
            install_code = '''# Install Discord desktop
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
            
            # Execute code via API
            execute_url = f"https://colab.research.google.com/api/notebooks/{self.notebook_id}/execute"
            
            payload = {
                "code": install_code,
                "cell_id": "install_cell"
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            response = self.session.post(execute_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                print("✅ Installation code executed")
                # Wait for installation to complete
                time.sleep(120)
                return True
            else:
                print(f"❌ Installation failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            return False
    
    def setup_plugin(self):
        """Set up the notifyServerJoins plugin"""
        try:
            print("🔌 Setting up plugin...")
            
            # Plugin setup code
            plugin_code = '''# Create plugin directory
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

print("Plugin file created successfully!")'''
            
            # Execute plugin setup
            execute_url = f"https://colab.research.google.com/api/notebooks/{self.notebook_id}/execute"
            
            payload = {
                "code": plugin_code,
                "cell_id": "plugin_cell"
            }
            
            response = self.session.post(execute_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                print("✅ Plugin setup completed")
                time.sleep(30)
                return True
            else:
                print(f"❌ Plugin setup failed: {response.status_code}")
                return False
                
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
            execute_url = f"https://colab.research.google.com/api/notebooks/{self.notebook_id}/execute"
            
            payload = {
                "code": start_code,
                "cell_id": "start_cell"
            }
            
            response = self.session.post(execute_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                print("✅ Discord started")
                time.sleep(30)
                return True
            else:
                print(f"❌ Discord start failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Discord start failed: {e}")
            return False
    
    def run(self):
        """Main execution flow"""
        try:
            print("�� Starting Colab API automation...")
            
            # Setup Colab API
            if not self.setup_colab_api():
                return False
            
            # Create notebook
            if not self.create_notebook_via_api():
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
            
            print(f"🎉 Setup completed successfully!")
            print(f"📓 Notebook URL: {self.colab_url}")
            
            # Save URL to file
            with open('colab_url.txt', 'w') as f:
                f.write(self.colab_url)
            
            return True
            
        except Exception as e:
            print(f"❌ Automation failed: {e}")
            return False

if __name__ == "__main__":
    automation = ColabAPIAutomation()
    success = automation.run()
    exit(0 if success else 1)
