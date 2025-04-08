# Sudip File Bot

A Telegram bot to save files/media and generate shareable links. Includes force-join and broadcast feature.

## 🔧 Setup Instructions (VPS)

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python & Git
sudo apt install python3-pip git -y

# 3. Clone your GitHub repo or upload files to VPS
git clone https://github.com/your-username/your-repo.git
cd your-repo

# 4. Install required Python packages
pip3 install -r requirements.txt

# 5. Run the bot
python3 main.py
```

---

## ⚙️ Configuration

Edit the following in `main.py`:
- `BOT_TOKEN`
- `channel_username` (your channel ID)
- Optional: developer/contact links

---

## 👤 Admin Broadcast

Only user with ID `5417870023` can use `/broadcast`.
