#!/usr/bin/env python
"""
Setup script for EB Calculator Django-MongoDB project
"""
import os
import sys
import subprocess


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def check_mongodb():
    """Check if MongoDB is running"""
    try:
        import pymongo
        client = pymongo.MongoClient('localhost', 27017, serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✓ MongoDB is running and accessible")
        return True
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        print("Please make sure MongoDB is installed and running on localhost:27017")
        return False


def main():
    """Main setup function"""
    print("=" * 60)
    print("EB Calculator Django-MongoDB Project Setup")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("Please install dependencies manually: pip install -r requirements.txt")
        return False
    
    # Check MongoDB
    if not check_mongodb():
        print("\nPlease install and start MongoDB:")
        print("- Windows: Download from https://www.mongodb.com/try/download/community")
        print("- macOS: brew install mongodb-community")
        print("- Linux: sudo apt-get install mongodb")
        return False
    
    # Run Django migrations (even though we use MongoDB, some Django apps need it)
    run_command("python manage.py migrate", "Running Django migrations")
    
    # Collect static files
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    print("\n" + "=" * 60)
    print("Setup completed successfully!")
    print("=" * 60)
    print("\nTo start the development server:")
    print("python manage.py runserver")
    print("\nThen open your browser to: http://127.0.0.1:8000")
    print("\nDefault features:")
    print("- User registration and login")
    print("- Daily electricity usage tracking")
    print("- Tamil Nadu EB tariff-based bill calculation")
    print("- MongoDB data storage")
    
    return True


if __name__ == "__main__":
    main()
