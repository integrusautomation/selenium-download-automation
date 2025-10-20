#!/usr/bin/env python3
"""
Test script to validate the Selenium setup
"""
import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        print("✓ Selenium imported successfully")
    except ImportError as e:
        print(f"✗ Selenium import failed: {e}")
        return False
    
    try:
        import chromedriver_autoinstaller
        print("✓ chromedriver_autoinstaller imported successfully")
    except ImportError as e:
        print(f"✗ chromedriver_autoinstaller import failed: {e}")
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        print("✓ webdriver-manager imported successfully")
    except ImportError as e:
        print(f"✗ webdriver-manager import failed: {e}")
    
    try:
        import dropbox
        print("✓ Dropbox imported successfully")
    except ImportError as e:
        print(f"✗ Dropbox import failed: {e}")
    
    try:
        from dropbox_token_manager import get_token_manager
        print("✓ dropbox_token_manager imported successfully")
    except ImportError as e:
        print(f"✗ dropbox_token_manager import failed: {e}")
    
    return True

def test_chrome_detection():
    """Test Chrome binary detection"""
    print("\nTesting Chrome detection...")
    
    # Check environment variable
    chrome_bin = os.environ.get('CHROME_BIN')
    if chrome_bin:
        print(f"CHROME_BIN environment variable: {chrome_bin}")
        if os.path.exists(chrome_bin):
            print("✓ Chrome binary exists at specified path")
        else:
            print("✗ Chrome binary not found at specified path")
    else:
        print("No CHROME_BIN environment variable set")
    
    # Check common Chrome locations
    possible_paths = [
        '/usr/bin/google-chrome',
        '/usr/bin/google-chrome-stable',
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✓ Found Chrome at: {path}")
            break
    else:
        print("✗ Chrome not found in common locations")

def test_chromedriver_detection():
    """Test ChromeDriver detection"""
    print("\nTesting ChromeDriver detection...")
    
    # Check environment variable
    chromedriver_path = os.environ.get('CHROMEDRIVER')
    if chromedriver_path:
        print(f"CHROMEDRIVER environment variable: {chromedriver_path}")
        if os.path.exists(chromedriver_path):
            print("✓ ChromeDriver exists at specified path")
        else:
            print("✗ ChromeDriver not found at specified path")
    else:
        print("No CHROMEDRIVER environment variable set")
    
    # Check PATH
    import subprocess
    try:
        result = subprocess.run(['which', 'chromedriver'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ ChromeDriver found in PATH: {result.stdout.strip()}")
        else:
            print("✗ ChromeDriver not found in PATH")
    except Exception as e:
        print(f"✗ Error checking PATH: {e}")

def main():
    """Main test function"""
    print("=== Selenium Setup Test ===\n")
    
    # Test imports
    if not test_imports():
        print("\n✗ Import test failed")
        sys.exit(1)
    
    # Test Chrome detection
    test_chrome_detection()
    
    # Test ChromeDriver detection
    test_chromedriver_detection()
    
    print("\n=== Test Complete ===")
    print("If all tests passed, your setup should work with GitHub Actions")

if __name__ == "__main__":
    main()
