#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Easy start script for Facebook Spam Tool Web Edition
@origin 250724-01 (Plants1.3)
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required!")
        print(f"Current version: {sys.version}")
        return False
    return True

def install_requirements():
    """Install requirements if needed"""
    print("🔍 Checking dependencies...")
    
    try:
        import flask
        import flask_socketio
        import requests
        print("✅ All dependencies are installed")
        return True
    except ImportError:
        print("📦 Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "uploads/images",
        "uploads/temp",
        "static/css",
        "static/js",
        "static/images",
        "templates/modals"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created")

def check_files():
    """Check if all necessary files exist"""
    print("🔍 Checking files...")
    
    required_files = [
        "app.py",
        "models/__init__.py",
        "models/facebook_api.py", 
        "models/token_manager.py",
        "models/spam_manager.py",
        "templates/base.html",
        "templates/index.html",
        "static/css/main.css",
        "static/js/main.js",
        "requirements.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All files present")
    return True

def start_app():
    """Start the Flask application"""
    print("🚀 Starting Facebook Spam Tool Web Edition...")
    print("=" * 50)
    
    # Set environment variables
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('PORT', '5000')
    
    try:
        # Import and start app
        from app import app, socketio
        
        # Configure for development
        app.config.update(
            DEBUG=True,
            TESTING=False
        )
        
        port = int(os.environ.get('PORT', 5000))
        
        print(f"🌐 Starting server on http://localhost:{port}")
        print("💡 Use Ctrl+C to stop the server")
        print("=" * 50)
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open(f'http://localhost:{port}')
        
        import threading
        threading.Thread(target=open_browser, daemon=True).start()
        
        # Start the app
        socketio.run(
            app,
            host='0.0.0.0',
            port=port,
            debug=True,
            allow_unsafe_werkzeug=True
        )
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🚀 Facebook Spam Tool - Professional Web Edition")
    print("=" * 50)
    
    # Check requirements
    if not check_python_version():
        sys.exit(1)
    
    if not check_files():
        print("\n❌ Missing required files. Please ensure all files are present.")
        sys.exit(1)
    
    if not install_requirements():
        print("\n❌ Failed to install dependencies. Please run: pip install -r requirements.txt")
        sys.exit(1)
    
    create_directories()
    
    print("\n✅ All checks passed! Starting web application...")
    print("\n📋 Features available:")
    print("   🔑 Token Management")
    print("   🚀 Auto Spam Comments") 

    print("   📁 Image Upload")
    print("   📊 Real-time Monitoring")
    print("   🌐 Responsive Web Interface")
    
    print("\n⚠️ Important:")
    print("   - Use responsibly and follow Facebook ToS")
    print("   - For educational purposes only")
    print("   - Test with small amounts first")
    
    print("\n" + "=" * 50)
    
    # Start the application
    if not start_app():
        sys.exit(1)

if __name__ == '__main__':
    main()
