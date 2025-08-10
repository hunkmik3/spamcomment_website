#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel entry point for Flask App
@origin 250724-01 (Plants1.3)
"""

import os
import sys

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, socketio

# For Vercel, we need to export the Flask app
if __name__ == "__main__":
    # Development mode
    socketio.run(app, debug=False)
else:
    # Production mode for Vercel
    application = app
