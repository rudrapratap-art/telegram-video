# 🎬 Telegram Video Downloader Bot

A powerful Telegram bot that can download videos from most popular websites using yt-dlp. Supports YouTube, Instagram, TikTok, Twitter/X, Facebook, Reddit, and 1000+ more sites!

## ✨ Features

- **Multi-Platform Support**: Download from YouTube, Instagram, TikTok, Twitter/X, Facebook, Reddit, Vimeo, Dailymotion, and many more
- **Multiple Formats**: Choose from various video and audio formats
- **Quality Selection**: Select your preferred video quality (720p, 1080p, etc.)
- **Audio Downloads**: Extract audio-only files (MP3, M4A, etc.)
- **User-Friendly Interface**: Interactive inline keyboards for easy format selection
- **Progress Tracking**: Real-time download progress updates
- **File Size Display**: Shows file size before downloading
- **Error Handling**: Comprehensive error handling and user feedback

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Telegram Bot Token** (Get from [@BotFather](https://t.me/BotFather))
3. **Telegram API Credentials** (Get from [my.telegram.org](https://my.telegram.org/apps))

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd telegram-video-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   cp config.py .env
   # Edit .env with your actual values
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

### Deploy on Render

1. **Fork this repository** to your GitHub account

2. **Create a new service on Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure environment variables**
   - `BOT_TOKEN`: Your Telegram bot token
   - `API_ID`: Your Telegram API ID
   - `API_HASH`: Your Telegram API hash

4. **Deploy**
   - Render will automatically detect the `render.yaml` configuration
   - The bot will be deployed as a background worker

## 📋 Commands

- `/start` - Welcome message and bot introduction
- `/help` - Detailed help guide and supported sites
- `/status` - Check bot status and uptime

## 🎯 How to Use

1. **Start the bot** by sending `/start`
2. **Send a video URL** from any supported platform
3. **Wait for processing** - the bot will extract available formats
4. **Choose your format** using the inline keyboard
5. **Download** - the bot will send you the video file

## 🔧 Supported Platforms

### Video Platforms
- **YouTube** (videos, shorts, live streams)
- **Instagram** (posts, reels, stories)
- **TikTok** (videos)
- **Twitter/X** (videos)
- **Facebook** (videos, reels)
- **Reddit** (videos)
- **Vimeo**
- **Dailymotion**
- **Twitch** (clips)
- **LinkedIn** (videos)

### Audio Platforms
- **Spotify** (tracks, playlists)
- **SoundCloud** (tracks)
- **Apple Music** (tracks)
- **Amazon Music** (tracks)

### And 1000+ more sites supported by yt-dlp!

## 🛠️ Technical Details

### Dependencies
- **pyrogram**: Modern Telegram API library
- **yt-dlp**: Powerful video downloader (youtube-dl fork)
- **python-dotenv**: Environment variable management
- **aiohttp**: Async HTTP client

### Architecture
- **Async/Await**: Non-blocking operations for better performance
- **State Management**: User session management for download tracking
- **Error Handling**: Comprehensive error handling and logging
- **File Management**: Temporary file handling and cleanup

## 🔒 Security Features

- **User Session Validation**: Users can only access their own downloads
- **Format Validation**: Secure format selection and validation
- **File Size Limits**: Respects Telegram's file size limits
- **Temporary Files**: Automatic cleanup of downloaded files

## 📊 Performance

- **Fast Processing**: Quick video information extraction
- **Memory Efficient**: Minimal memory usage with streaming downloads
- **Concurrent Downloads**: Supports multiple users simultaneously
- **Caching**: Efficient format caching for better performance

## 🐛 Troubleshooting

### Common Issues

1. **"No downloadable formats found"**
   - The video might be private or region-restricted
   - Try a different video or platform

2. **"Download failed"**
   - Check your internet connection
   - The video might be too large for Telegram
   - Try a lower quality format

3. **"Bot not responding"**
   - Check if the bot is running
   - Verify your environment variables
   - Check the logs for errors

### Debug Mode

Enable debug logging by setting `DEBUG = True` in your environment variables.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The amazing video downloader
- [Pyrogram](https://github.com/pyrogram/pyrogram) - Modern Telegram API library
- [Render](https://render.com) - Free hosting platform

## 📞 Support

If you need help or have questions:
- Create an issue on GitHub
- Contact the bot developer
- Check the troubleshooting section

---

**Made with ❤️ using yt-dlp and Pyrogram**
