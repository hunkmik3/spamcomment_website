#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto deployment script for FB Spam Tool Web Edition
@origin 250724-01 (Plants1.3)
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"   Error: {e.stderr.strip()}")
        return False

def check_git_installed():
    """Check if Git is installed"""
    try:
        subprocess.run(['git', '--version'], check=True, capture_output=True)
        return True
    except:
        print("❌ Git is not installed or not in PATH")
        return False

def check_vercel_cli():
    """Check if Vercel CLI is installed"""
    try:
        subprocess.run(['vercel', '--version'], check=True, capture_output=True)
        return True
    except:
        print("⚠️ Vercel CLI not found. You can install it with: npm i -g vercel")
        return False

def setup_git_repo():
    """Setup Git repository"""
    print("\n📋 Setting up Git repository...")
    
    # Check if already a git repo
    if os.path.exists('.git'):
        print("✅ Git repository already exists")
        return True
    
    commands = [
        ('git init', 'Initialize Git repository'),
        ('git add .', 'Add all files'),
        ('git commit -m "Initial commit: FB Spam Tool Web Edition"', 'Create initial commit')
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    print("\n📝 Next steps:")
    print("1. Create a new repository on GitHub: https://github.com/new")
    print("2. Set repository name: fb-spam-tool-web")
    print("3. Run: git remote add origin https://github.com/YOUR_USERNAME/fb-spam-tool-web.git")
    print("4. Run: git push -u origin main")
    
    return True

def deploy_to_vercel():
    """Deploy to Vercel using CLI"""
    print("\n🚀 Deploying to Vercel...")
    
    if not check_vercel_cli():
        print("\n📝 Manual deployment steps:")
        print("1. Go to https://vercel.com")
        print("2. Login with GitHub")
        print("3. Click 'New Project'")
        print("4. Import your GitHub repository")
        print("5. Set environment variables:")
        print("   SECRET_KEY = your-secret-key")
        print("   FLASK_ENV = production")
        print("6. Click Deploy")
        return False
    
    commands = [
        ('vercel login', 'Login to Vercel'),
        ('vercel', 'Deploy to Vercel'),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    print("✅ Deployment completed!")
    return True

def main():
    """Main deployment function"""
    print("🚀 FB Spam Tool Web Edition - Auto Deployment Script")
    print("=" * 60)
    
    # Check prerequisites
    if not check_git_installed():
        print("\n❌ Please install Git first: https://git-scm.com/")
        sys.exit(1)
    
    # Setup Git repository
    if not setup_git_repo():
        print("\n❌ Failed to setup Git repository")
        sys.exit(1)
    
    # Check if remote is set up
    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Git remote found: {result.stdout.strip()}")
        
        # Push to GitHub
        push_choice = input("\n🤔 Do you want to push to GitHub now? (y/n): ")
        if push_choice.lower() == 'y':
            run_command('git push -u origin main', 'Push to GitHub')
        
    except subprocess.CalledProcessError:
        print("\n⚠️ No Git remote configured yet")
        print("Please follow the steps above to setup GitHub repository")
    
    # Deploy to Vercel
    deploy_choice = input("\n🤔 Do you want to deploy to Vercel now? (y/n): ")
    if deploy_choice.lower() == 'y':
        deploy_to_vercel()
    
    print("\n" + "=" * 60)
    print("🎉 Deployment script completed!")
    print("\n📚 For detailed instructions, see: DEPLOYMENT_GUIDE.md")
    print("🌐 Once deployed, your tool will be available at: https://your-project.vercel.app")

if __name__ == "__main__":
    main()
