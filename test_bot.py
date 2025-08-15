#!/usr/bin/env python3
"""
Test script for Telegram Video Downloader Bot
This script tests the bot configuration and dependencies
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

def test_imports():
    """Test if all required packages are installed"""
    print("🔍 Testing imports...")
    
    try:
        import pyrogram
        print(f"✅ Pyrogram version: {pyrogram.__version__}")
    except ImportError as e:
        print(f"❌ Pyrogram import failed: {e}")
        return False
    
    try:
        import yt_dlp
        print(f"✅ yt-dlp version: {yt_dlp.version.__version__}")
    except ImportError as e:
        print(f"❌ yt-dlp import failed: {e}")
        return False
    
    try:
        import aiohttp
        print(f"✅ aiohttp version: {aiohttp.__version__}")
    except ImportError as e:
        print(f"❌ aiohttp import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment variables"""
    print("\n🔍 Testing environment variables...")
    
    load_dotenv()
    
    bot_token = os.getenv("BOT_TOKEN")
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")
    
    if not bot_token:
        print("❌ BOT_TOKEN not found in environment variables")
        return False
    else:
        print("✅ BOT_TOKEN found")
    
    if not api_id:
        print("❌ API_ID not found in environment variables")
        return False
    else:
        print("✅ API_ID found")
    
    if not api_hash:
        print("❌ API_HASH not found in environment variables")
        return False
    else:
        print("✅ API_HASH found")
    
    return True

def test_yt_dlp():
    """Test yt-dlp functionality"""
    print("\n🔍 Testing yt-dlp...")
    
    try:
        import yt_dlp
        
        # Test with a simple YouTube URL
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(test_url, download=False)
            
        if info and 'title' in info:
            print(f"✅ yt-dlp working - Test video: {info['title'][:50]}...")
            return True
        else:
            print("❌ yt-dlp failed to extract video info")
            return False
            
    except Exception as e:
        print(f"❌ yt-dlp test failed: {e}")
        return False

async def test_pyrogram():
    """Test Pyrogram connection"""
    print("\n🔍 Testing Pyrogram connection...")
    
    try:
        from pyrogram import Client
        
        bot_token = os.getenv("BOT_TOKEN")
        api_id = os.getenv("API_ID")
        api_hash = os.getenv("API_HASH")
        
        app = Client(
            "test_bot",
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token
        )
        
        await app.start()
        me = await app.get_me()
        print(f"✅ Bot connected successfully: @{me.username}")
        await app.stop()
        return True
        
    except Exception as e:
        print(f"❌ Pyrogram connection failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Telegram Video Downloader Bot - Test Suite")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed. Please install missing dependencies:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Test environment
    if not test_environment():
        print("\n❌ Environment test failed. Please set up your .env file:")
        print("1. Copy config.py to .env")
        print("2. Fill in your BOT_TOKEN, API_ID, and API_HASH")
        sys.exit(1)
    
    # Test yt-dlp
    if not test_yt_dlp():
        print("\n❌ yt-dlp test failed. Please check your internet connection.")
        sys.exit(1)
    
    # Test Pyrogram
    try:
        asyncio.run(test_pyrogram())
    except Exception as e:
        print(f"\n❌ Pyrogram test failed: {e}")
        print("Please check your bot token and API credentials.")
        sys.exit(1)
    
    print("\n🎉 All tests passed! Your bot is ready to run.")
    print("\nTo start the bot, run:")
    print("python bot.py")

if __name__ == "__main__":
    main()
