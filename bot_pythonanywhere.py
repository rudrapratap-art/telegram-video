import os
import asyncio
import logging
import tempfile
import shutil
import sys
from typing import Optional, Dict, Any
from datetime import datetime

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pyrogram import Client, filters, types
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import yt_dlp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging for PythonAnywhere
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable is not set!")
    sys.exit(1)

if not API_ID or not API_HASH:
    logger.error("API_ID or API_HASH environment variables are not set!")
    sys.exit(1)

# Initialize the bot with session file in current directory
app = Client(
    "video_downloader_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir=os.path.dirname(os.path.abspath(__file__))
)

# Global variables to store user states
user_states = {}

def format_size(size_bytes: int) -> str:
    """Convert bytes to human readable format"""
    if not size_bytes:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def format_duration(seconds: int) -> str:
    """Convert seconds to human readable format"""
    if not seconds:
        return "0s"
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60
        return f"{hours}h {minutes}m {remaining_seconds}s"

async def extract_video_info(url: str) -> Optional[Dict[str, Any]]:
    """Extract video information using yt-dlp"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        logger.error(f"Error extracting info: {e}")
        return None

def get_available_formats(info: Dict[str, Any]) -> list:
    """Get available video formats"""
    formats = []
    
    if 'formats' in info:
        for fmt in info['formats']:
            if fmt.get('url') and fmt.get('ext'):
                format_info = {
                    'format_id': fmt.get('format_id', ''),
                    'ext': fmt.get('ext', ''),
                    'filesize': fmt.get('filesize'),
                    'height': fmt.get('height'),
                    'width': fmt.get('width'),
                    'fps': fmt.get('fps'),
                    'vcodec': fmt.get('vcodec'),
                    'acodec': fmt.get('acodec'),
                    'url': fmt.get('url'),
                    'format_note': fmt.get('format_note', ''),
                }
                formats.append(format_info)
    
    return formats

def create_format_keyboard(formats: list, video_id: str) -> InlineKeyboardMarkup:
    """Create inline keyboard for format selection"""
    keyboard = []
    
    # Group formats by quality
    video_formats = [f for f in formats if f.get('height') and f.get('vcodec') != 'none']
    audio_formats = [f for f in formats if f.get('acodec') and f.get('acodec') != 'none']
    
    # Add video formats
    if video_formats:
        keyboard.append([InlineKeyboardButton("📹 Video Formats", callback_data=f"header_video_{video_id}")])
        
        # Sort by quality (height)
        video_formats.sort(key=lambda x: x.get('height', 0), reverse=True)
        
        for fmt in video_formats[:5]:  # Show top 5 video formats
            height = fmt.get('height', 'N/A')
            ext = fmt.get('ext', 'mp4')
            size = format_size(fmt.get('filesize', 0)) if fmt.get('filesize') else 'Unknown'
            text = f"🎥 {height}p ({ext}) - {size}"
            callback_data = f"download_{video_id}_{fmt['format_id']}"
            keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])
    
    # Add audio formats
    if audio_formats:
        keyboard.append([InlineKeyboardButton("🎵 Audio Formats", callback_data=f"header_audio_{video_id}")])
        
        for fmt in audio_formats[:3]:  # Show top 3 audio formats
            ext = fmt.get('ext', 'mp3')
            size = format_size(fmt.get('filesize', 0)) if fmt.get('filesize') else 'Unknown'
            text = f"🎵 Audio ({ext}) - {size}"
            callback_data = f"download_{video_id}_{fmt['format_id']}"
            keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])
    
    # Add cancel button
    keyboard.append([InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{video_id}")])
    
    return InlineKeyboardMarkup(keyboard)

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Handle /start command"""
    welcome_text = """
🎬 <b>Welcome to Video Downloader Bot!</b>

I can download videos from most popular websites including:
• YouTube
• Instagram
• TikTok
• Twitter/X
• Facebook
• And many more!

<b>How to use:</b>
1. Send me a video URL
2. Choose your preferred format
3. Download your video!

<b>Commands:</b>
/start - Show this message
/help - Show help information
/status - Check bot status

Made with ❤️ using yt-dlp
    """
    
    await message.reply_text(welcome_text, parse_mode="html")

@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """Handle /help command"""
    help_text = """
📖 <b>Help Guide</b>

<b>Supported Sites:</b>
• YouTube (videos, shorts, live streams)
• Instagram (posts, reels, stories)
• TikTok (videos)
• Twitter/X (videos)
• Facebook (videos, reels)
• Reddit (videos)
• Vimeo
• Dailymotion
• And 1000+ more sites!

<b>How to download:</b>
1. Copy the video URL
2. Send it to me
3. Wait for format options
4. Select your preferred quality
5. Download the file

<b>Tips:</b>
• For better quality, choose higher resolution
• Audio-only formats are smaller in size
• Some videos may take time to process
• Large files might be split due to Telegram limits

<b>Need help?</b> Contact @your_username
    """
    
    await message.reply_text(help_text, parse_mode="html")

@app.on_message(filters.command("status"))
async def status_command(client: Client, message: Message):
    """Handle /status command"""
    status_text = """
🤖 <b>Bot Status</b>

✅ <b>Bot is running</b>
✅ <b>yt-dlp is available</b>
✅ <b>Ready to download videos</b>

<b>Uptime:</b> Since last restart
<b>Version:</b> 1.0.0
<b>Powered by:</b> yt-dlp + Pyrogram
<b>Hosted on:</b> PythonAnywhere

Send me a video URL to get started!
    """
    
    await message.reply_text(status_text, parse_mode="html")

@app.on_message(filters.text)
async def handle_url(client: Client, message: Message):
    """Handle video URLs"""
    # Skip if this is a command
    if message.text.startswith('/'):
        return
        
    url = message.text.strip()
    
    # Basic URL validation
    if not any(domain in url.lower() for domain in ['youtube', 'youtu.be', 'instagram', 'tiktok', 'twitter', 'facebook', 'reddit', 'vimeo', 'dailymotion']):
        await message.reply_text("❌ Please send a valid video URL from supported platforms.")
        return
    
    # Send processing message
    processing_msg = await message.reply_text("🔍 <b>Processing your video...</b>\n\nPlease wait while I extract the available formats.", parse_mode="html")
    
    try:
        # Extract video information
        info = await extract_video_info(url)
        
        if not info:
            await processing_msg.edit_text("❌ <b>Error:</b> Could not extract video information.\n\nPlease check if the URL is valid and the video is available.")
            return
        
        # Get video details
        title = info.get('title', 'Unknown Title')
        duration = info.get('duration', 0)
        uploader = info.get('uploader', 'Unknown')
        thumbnail = info.get('thumbnail')
        
        # Get available formats
        formats = get_available_formats(info)
        
        if not formats:
            await processing_msg.edit_text("❌ <b>Error:</b> No downloadable formats found for this video.")
            return
        
        # Generate unique video ID
        video_id = str(hash(url))[:8]
        
        # Create format selection keyboard
        keyboard = create_format_keyboard(formats, video_id)
        
        # Prepare response text
        response_text = f"""
🎬 <b>Video Found!</b>

<b>Title:</b> {title[:100]}{'...' if len(title) > 100 else ''}
<b>Uploader:</b> {uploader}
<b>Duration:</b> {format_duration(duration)}
<b>Available Formats:</b> {len(formats)}

Choose your preferred format below:
        """
        
        # Send video info with format options
        await processing_msg.edit_text(
            response_text,
            reply_markup=keyboard,
            parse_mode="html"
        )
        
        # Store video info for later use
        user_states[video_id] = {
            'url': url,
            'info': info,
            'formats': formats,
            'user_id': message.from_user.id,
            'message_id': message.id
        }
        
    except Exception as e:
        logger.error(f"Error processing URL: {e}")
        await processing_msg.edit_text(f"❌ <b>Error:</b> An unexpected error occurred.\n\nError: {str(e)}")

@app.on_callback_query()
async def handle_callback(client: Client, callback_query: CallbackQuery):
    """Handle callback queries for format selection"""
    data = callback_query.data
    user_id = callback_query.from_user.id
    
    try:
        if data.startswith("download_"):
            # Parse download request
            parts = data.split("_")
            video_id = parts[1]
            format_id = parts[2]
            
            if video_id not in user_states:
                await callback_query.answer("❌ Video session expired. Please send the URL again.")
                return
            
            video_info = user_states[video_id]
            
            # Check if user owns this session
            if video_info['user_id'] != user_id:
                await callback_query.answer("❌ This download session is not yours.")
                return
            
            # Find the selected format
            selected_format = None
            for fmt in video_info['formats']:
                if fmt['format_id'] == format_id:
                    selected_format = fmt
                    break
            
            if not selected_format:
                await callback_query.answer("❌ Format not found.")
                return
            
            # Start download process
            await start_download(client, callback_query, video_info, selected_format)
            
        elif data.startswith("cancel_"):
            video_id = data.split("_")[1]
            
            if video_id in user_states:
                del user_states[video_id]
            
            await callback_query.message.edit_text("❌ <b>Download cancelled.</b>\n\nSend me another video URL to try again.", parse_mode="html")
            await callback_query.answer("Download cancelled")
            
        elif data.startswith("header_"):
            # Just acknowledge header buttons
            await callback_query.answer()
            
    except Exception as e:
        logger.error(f"Error handling callback: {e}")
        await callback_query.answer("❌ An error occurred.")

async def start_download(client: Client, callback_query: CallbackQuery, video_info: dict, selected_format: dict):
    """Start the download process"""
    try:
        # Update message to show download progress
        progress_text = f"""
⏳ <b>Downloading...</b>

<b>Format:</b> {selected_format.get('ext', 'mp4')}
<b>Quality:</b> {selected_format.get('height', 'N/A')}p
<b>Size:</b> {format_size(selected_format.get('filesize', 0)) if selected_format.get('filesize') else 'Unknown'}

Please wait while I download your video...
        """
        
        await callback_query.message.edit_text(progress_text, parse_mode="html")
        
        # Download the video
        downloaded_file = await download_video(video_info['url'], selected_format)
        
        if not downloaded_file:
            await callback_query.message.edit_text("❌ <b>Download failed.</b>\n\nPlease try again or choose a different format.")
            return
        
        # Send the video file
        caption = f"""
✅ <b>Download Complete!</b>

<b>Title:</b> {video_info['info'].get('title', 'Unknown')[:50]}
<b>Format:</b> {selected_format.get('ext', 'mp4')}
<b>Quality:</b> {selected_format.get('height', 'N/A')}p
<b>Size:</b> {format_size(os.path.getsize(downloaded_file))}

Downloaded with ❤️ by Video Downloader Bot
        """
        
        # Send file based on type
        if selected_format.get('ext') in ['mp3', 'm4a', 'wav', 'ogg']:
            await client.send_audio(
                chat_id=callback_query.message.chat.id,
                audio=downloaded_file,
                caption=caption,
                parse_mode="html"
            )
        else:
            await client.send_video(
                chat_id=callback_query.message.chat.id,
                video=downloaded_file,
                caption=caption,
                parse_mode="html"
            )
        
        # Clean up
        os.remove(downloaded_file)
        
        # Update message
        await callback_query.message.edit_text("✅ <b>Download completed successfully!</b>\n\nSend me another video URL to download more videos.", parse_mode="html")
        
    except Exception as e:
        logger.error(f"Error in download process: {e}")
        await callback_query.message.edit_text(f"❌ <b>Download failed.</b>\n\nError: {str(e)}")

async def download_video(url: str, format_info: dict) -> Optional[str]:
    """Download video using yt-dlp"""
    temp_dir = tempfile.mkdtemp()
    
    try:
        ydl_opts = {
            'format': format_info['format_id'],
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Find the downloaded file
        files = os.listdir(temp_dir)
        if files:
            return os.path.join(temp_dir, files[0])
        
        return None
        
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Starting Video Downloader Bot on PythonAnywhere...")
    print(f"Bot Token: {'✅ Set' if BOT_TOKEN else '❌ Missing'}")
    print(f"API ID: {'✅ Set' if API_ID else '❌ Missing'}")
    print(f"API Hash: {'✅ Set' if API_HASH else '❌ Missing'}")
    
    if not all([BOT_TOKEN, API_ID, API_HASH]):
        print("❌ Missing required environment variables. Please check your .env file.")
        sys.exit(1)
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        print(f"❌ Bot crashed: {e}")
