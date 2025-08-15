# 🚀 PythonAnywhere Setup Guide

This guide will help you deploy your Telegram Video Downloader Bot on PythonAnywhere.

## 📋 Prerequisites

1. **PythonAnywhere Account** (Free tier works)
2. **Telegram Bot Token** (from @BotFather)
3. **Telegram API Credentials** (from my.telegram.org)

## 🎯 Step-by-Step Setup

### Step 1: Create PythonAnywhere Account
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free account
3. Access your dashboard

### Step 2: Upload Your Bot Code

#### Option A: Using Git (Recommended)
1. **Open a Bash console** in PythonAnywhere
2. **Clone your repository**:
```bash
git clone https://github.com/rudrapratap-art/telegram-video.git
cd telegram-video
```

#### Option B: Manual Upload
1. Go to **Files** tab in PythonAnywhere
2. Create a new directory: `telegram-video`
3. Upload these files:
   - `bot_pythonanywhere.py` (use this instead of bot.py)
   - `requirements.txt`
   - `.env` (create this)

### Step 3: Install Dependencies
In the Bash console:
```bash
cd telegram-video
pip install --user -r requirements.txt
```

### Step 4: Set Up Environment Variables
1. **Go to Files tab**
2. **Create `.env` file** in your bot directory:
```bash
nano .env
```

3. **Add your credentials**:
```env
BOT_TOKEN=your_bot_token_here
API_ID=your_api_id_here
API_HASH=your_api_hash_here
```

4. **Save the file** (Ctrl+X, then Y, then Enter)

### Step 5: Test Your Bot
In the Bash console:
```bash
cd telegram-video
python bot_pythonanywhere.py
```

You should see:
```
🚀 Starting Video Downloader Bot on PythonAnywhere...
Bot Token: ✅ Set
API ID: ✅ Set
API Hash: ✅ Set
```

### Step 6: Set Up Always-On Task (Free Tier)

Since PythonAnywhere free tier has limitations, you have a few options:

#### Option A: Manual Restart (Free Tier)
- The bot will run as long as you keep the console open
- You'll need to restart it manually if it stops

#### Option B: Upgrade to Paid Plan
- Paid plans allow always-on tasks
- More reliable for production use

#### Option C: Use External Monitoring
- Set up a simple monitoring script
- Restart the bot if it goes down

## 🔧 Configuration Details

### Files Used:
- **`bot_pythonanywhere.py`** - Optimized for PythonAnywhere
- **`requirements.txt`** - Python dependencies
- **`.env`** - Environment variables

### Key Features:
- ✅ **File logging** - Logs saved to `bot.log`
- ✅ **Error handling** - Better error messages
- ✅ **Session management** - Session files in current directory
- ✅ **Environment validation** - Checks all required variables

## 🐛 Troubleshooting

### Common Issues:

1. **"Module not found" errors**
   ```bash
   pip install --user -r requirements.txt
   ```

2. **"Permission denied" errors**
   - Make sure you're in your home directory
   - Use `--user` flag with pip

3. **"Bot token not set" error**
   - Check your `.env` file
   - Make sure it's in the same directory as the bot

4. **"Connection timeout" errors**
   - PythonAnywhere free tier has network restrictions
   - Some video sites might be blocked

### Logs:
- Check `bot.log` file for detailed error messages
- Use `tail -f bot.log` to monitor logs in real-time

## 📊 Monitoring

### Check Bot Status:
```bash
ps aux | grep python
```

### View Logs:
```bash
tail -f bot.log
```

### Restart Bot:
```bash
pkill -f bot_pythonanywhere.py
python bot_pythonanywhere.py
```

## 🎯 Testing Your Bot

1. **Send `/start`** to your bot
2. **Send a video URL** (YouTube, Instagram, etc.)
3. **Select a format** from the inline keyboard
4. **Download the video**

## 💡 Tips for PythonAnywhere

1. **Free Tier Limitations**:
   - No always-on tasks
   - Limited CPU time
   - Network restrictions

2. **Best Practices**:
   - Keep console sessions open
   - Monitor logs regularly
   - Restart bot if needed

3. **Upgrading**:
   - Consider paid plan for production
   - Better reliability and features

## 🔗 Useful Links

- [PythonAnywhere](https://www.pythonanywhere.com)
- [@BotFather](https://t.me/BotFather)
- [my.telegram.org](https://my.telegram.org/apps)
- [GitHub Repository](https://github.com/rudrapratap-art/telegram-video)

## 🎉 Success!

Once your bot is running, you should see:
- ✅ Bot connects to Telegram
- ✅ Commands work (`/start`, `/help`, `/status`)
- ✅ Video downloading works
- ✅ Logs are being written to `bot.log`

Your Telegram Video Downloader Bot is now hosted on PythonAnywhere! 🚀
