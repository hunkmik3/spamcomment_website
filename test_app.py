#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Facebook Spam Tool Web Edition
@origin 250724-01 (Plants1.3)
"""

import os
import sys
import requests
import time

# Test configuration
BASE_URL = 'http://localhost:5000'
TEST_TOKEN = 'EAAG_TEST_TOKEN_FOR_TESTING_PURPOSE_ONLY'

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f'{BASE_URL}/health')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_main_page():
    """Test main page loads"""
    print("🔍 Testing main page...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            if 'Tool Spam FB Token' in response.text:
                print("✅ Main page loads successfully")
                return True
            else:
                print("❌ Main page missing expected content")
                return False
        else:
            print(f"❌ Main page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Main page error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("🔍 Testing API endpoints...")
    
    # Create session for persistent cookies
    session = requests.Session()
    
    # Test get tokens (should return empty initially)
    try:
        response = session.get(f'{BASE_URL}/api/tokens')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ GET /api/tokens: {data['total']} tokens")
        else:
            print(f"❌ GET /api/tokens failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ GET /api/tokens error: {e}")
        return False
    
    # Test add tokens
    try:
        response = session.post(
            f'{BASE_URL}/api/tokens',
            json={'tokens': TEST_TOKEN},
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ POST /api/tokens: {data['message']}")
            else:
                print(f"⚠️ POST /api/tokens: {data['message']}")
        else:
            print(f"❌ POST /api/tokens failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ POST /api/tokens error: {e}")
        return False
    
    # Test get images
    try:
        response = session.get(f'{BASE_URL}/api/images')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ GET /api/images: {len(data['images'])} images")
        else:
            print(f"❌ GET /api/images failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ GET /api/images error: {e}")
        return False
    
    return True

def test_static_files():
    """Test static files load"""
    print("🔍 Testing static files...")
    
    static_files = [
        '/static/css/main.css',
        '/static/js/main.js'
    ]
    
    for file_path in static_files:
        try:
            response = requests.get(f'{BASE_URL}{file_path}')
            if response.status_code == 200:
                print(f"✅ Static file {file_path}: OK")
            else:
                print(f"❌ Static file {file_path}: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Static file {file_path} error: {e}")
            return False
    
    return True

def run_tests():
    """Run all tests"""
    print("🚀 Starting Facebook Spam Tool Web Edition Tests")
    print("=" * 50)
    
    tests = [
        test_health_check,
        test_main_page,
        test_static_files,
        test_api_endpoints,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test error: {e}")
            print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Web app is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        return False

if __name__ == '__main__':
    print("📋 Facebook Spam Tool Web Edition - Test Suite")
    print("⚠️ Make sure the web app is running on http://localhost:5000")
    print()
    
    input("Press Enter to start tests...")
    print()
    
    success = run_tests()
    sys.exit(0 if success else 1)
