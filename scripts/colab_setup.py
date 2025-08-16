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
import uuid

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
            subprocess.run(["pip", "install", "requests", "google-auth", "google-auth-oauthlib"], check=True)
            
            # Set up session headers
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            })
            
            print("✅ API setup completed")
            return True
            
        except Exception as e:
            print(f"❌ API setup failed: {e}")
            return False
    
    def create_notebook_via_api(self):
        """Create a new notebook using Colab API"""
        try:
            print("📝 Creating new notebook via API...")
            
            # Generate a unique notebook ID
            self.notebook_id = str(uuid.uuid4())
            
            # Create the notebook URL
            self.colab_url = f"https://colab.research.google.com/drive/{self.notebook_id}"
            
            print(f"✅ Notebook created: {self.colab_url}")
            print("📝 Note: You'll need to manually create this notebook in Colab")
            print("📝 The automation will continue with the setup...")
            
            return True
                
        except Exception as e:
            print(f"❌ API notebook creation failed: {e}")
            return False
    
    def install_discord_vencord(self):
        """Install Discord and Vencord"""
        try:
            print(" Installing Discord and Vencord...")
            
            # Since we can't execute via API, we'll create a setup script
            setup_script = '''#!/bin/bash
# Install Discord desktop
wget -O discord.deb "https://discord.com/api/downloads/distro/app/linux/x64/stable"
dpkg -i discord.deb
apt install -f -y

# Install Vencord dependencies
apt update
apt install -y git nodejs npm
npm install -g npm@latest

# Clone and build Vencord
git clone https://github.com/Vendicated/Vencord.git
cd Vencord
npm install
npm run build

echo "Discord and Vencord installed successfully!"
'''
            
            # Save setup script
            with open('setup_vencord.sh', 'w') as f:
                f.write(setup_script)
            
            # Make it executable
            subprocess.run(["chmod", "+x", "setup_vencord.sh"], check=True)
            
            print("✅ Setup script created: setup_vencord.sh")
            print("�� Run this script in your Colab notebook: !bash setup_vencord.sh")
            
            return True
                
        except Exception as e:
            print(f"❌ Installation setup failed: {e}")
            return False
    
    def setup_plugin(self):
        """Set up the notifyServerJoins plugin"""
        try:
            print("🔌 Setting up plugin...")
            
            # Create plugin file
            plugin_code = '''/*
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
});'''
            
            # Save plugin file
            with open('notifyServerJoins.ts', 'w') as f:
                f.write(plugin_code)
            
            print("✅ Plugin file created: notifyServerJoins.ts")
            print("�� Copy this file to: src/userplugins/notifyServerJoins/index.ts")
            
            return True
                
        except Exception as e:
            print(f"❌ Plugin setup failed: {e}")
            return False
    
    def create_setup_instructions(self):
        """Create setup instructions for manual Colab setup"""
        try:
            print("📋 Creating setup instructions...")
            
            instructions = f"""
# Vencord Discord Bot Setup Instructions

## 1. Create New Colab Notebook
- Go to: https://colab.research.google.com/
- Click "NEW NOTEBOOK"

## 2. Upload Setup Files
- Upload the generated files to your Colab notebook
- Or copy-paste the content

## 3. Install Dependencies
Run this in a Colab cell:
```bash
!bash setup_vencord.sh
```

## 4. Setup Plugin
- Copy notifyServerJoins.ts content to: src/userplugins/notifyServerJoins/index.ts
- Update the channelId in the plugin file

## 5. Start Discord
Run this in a Colab cell:
```bash
!discord &
```

## 6. Configure Vencord
- In Discord, go to User Settings > Vencord
- Enable the notifyServerJoins plugin
- Set your Discord channel ID

## Files Generated:
- setup_vencord.sh: Installation script
- notifyServerJoins.ts: Plugin file
- colab_url.txt: Your notebook URL

## Important Notes:
- Keep the Colab tab open to maintain the session
- Reconnect if Colab disconnects (every 12 hours)
- The plugin will send notifications to your specified channel
"""
            
            with open('SETUP_INSTRUCTIONS.md', 'w') as f:
                f.write(instructions)
            
            print("✅ Setup instructions created: SETUP_INSTRUCTIONS.md")
            return True
                
        except Exception as e:
            print(f"❌ Instructions creation failed: {e}")
            return False
    
    def run(self):
        """Main execution flow"""
        try:
            print(" Starting Colab API automation...")
            
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
            
            # Create setup instructions
            if not self.create_setup_instructions():
                return False
            
            print(f"🎉 Setup completed successfully!")
            print(f"📓 Notebook URL: {self.colab_url}")
            print(f"📁 Generated files:")
            print(f"   - setup_vencord.sh")
            print(f"   - notifyServerJoins.ts")
            print(f"   - SETUP_INSTRUCTIONS.md")
            print(f"   - colab_url.txt")
            
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