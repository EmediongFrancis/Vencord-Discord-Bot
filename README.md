# Vencord Discord Bot - Automated Server Join Notifications

This repository contains an automated Discord bot that notifies when users join servers, built using Vencord and Google Colab.

## Features

- 🤖 **Fully Automated**: Runs 24/7 using GitHub Actions
- �� **Auto-Recovery**: Automatically reconnects when Colab disconnects
- 📱 **Cross-Platform**: Works on all devices through Discord sync
- 💰 **100% Free**: Uses Google Colab + GitHub Actions free tiers

## Setup

1. **Fork this repository**
2. **Set GitHub Secrets**:
   - `DISCORD_CHANNEL_ID`: Your Discord channel ID
   - `DISCORD_TOKEN`: Your Discord bot token (optional)
   - `COLAB_URL`: Will be auto-generated

3. **Enable GitHub Actions** in your repository settings

## How It Works

1. GitHub Actions runs every 4 hours
2. Automatically sets up Google Colab with Discord + Vencord
3. Installs your custom plugin for server join notifications
4. Keeps the session alive and monitors for disconnections
5. Automatically reconnects if needed

## Files

- `.github/workflows/colab-automation.yml` - GitHub Actions automation
- `scripts/colab_setup.py` - Automated Colab setup
- `scripts/colab_keepalive.py` - Session monitoring and recovery
- `config/discord_config.json` - Configuration file

## Maintenance

- **Zero manual intervention** required
- Automatically handles Colab disconnections
- Self-healing system with multiple fallbacks
- GitHub Actions run every 4 hours for reliability

## Troubleshooting

If notifications stop working:
1. Check GitHub Actions logs
2. Verify Discord channel ID is correct
3. Ensure your Discord account is logged into Colab

## License

MIT License - Feel free to modify and distribute!