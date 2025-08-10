#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Development runner for Facebook Spam Tool Web Edition
@origin 250724-01 (Plants1.3)
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    from app import app, socketio
    
    # Development configuration
    app.config.update(
        DEBUG=True,
        TESTING=False
    )
    
    # Run with SocketIO
    socketio.run(
        app,
        host=os.environ.get('HOST', '0.0.0.0'),
        port=int(os.environ.get('PORT', 5000)),
        debug=True,
        allow_unsafe_werkzeug=True
    )
