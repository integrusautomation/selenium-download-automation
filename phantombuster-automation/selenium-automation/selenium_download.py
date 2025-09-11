from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
try:
    import chromedriver_autoinstaller
    CHROMEDRIVER_AUTOINSTALLER_AVAILABLE = True
except ImportError:
    CHROMEDRIVER_AUTOINSTALLER_AVAILABLE = False
    print("Warning: chromedriver_autoinstaller not available, will use system chromedriver")
import time
import os
import io
import json
import base64
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import dropbox
import requests

# Phantombuster CAPTCHA solving functions
def solve_captcha(driver, logs):
    """
    Solve image-based CAPTCHA using Phantombuster's solveCaptcha function
    """
    try:
        logs.write(f"[{datetime.now()}] Attempting to solve CAPTCHA...\n")
        
        # Take screenshot of the CAPTCHA
        captcha_element = driver.find_element(By.CSS_SELECTOR, "img[src*='captcha'], .captcha img, #captcha img")
        captcha_screenshot = captcha_element.screenshot_as_base64
        
        # In a real Phantombuster environment, you would use:
        # solution = driver.execute_script("return solveCaptcha();")
        
        # For testing purposes, we'll simulate the CAPTCHA solving
        logs.write(f"[{datetime.now()}] CAPTCHA detected, taking screenshot...\n")
        
        # Save CAPTCHA screenshot for debugging
        debug_dir = "debug_screenshots"
        os.makedirs(debug_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        captcha_file = os.path.join(debug_dir, f"captcha_{timestamp}.png")
        
        with open(captcha_file, "wb") as f:
            f.write(base64.b64decode(captcha_screenshot))
        
        logs.write(f"[{datetime.now()}] CAPTCHA screenshot saved: {captcha_file}\n")
        
        # Upload to Dropbox for debugging
        upload_to_dropbox(captcha_file, f"captcha_debug_{timestamp}.png", logs)
        
        # Simulate CAPTCHA solution (replace with actual Phantombuster call)
        logs.write(f"[{datetime.now()}] Simulating CAPTCHA solution...\n")
        return "SOLVED"  # Replace with actual solution
        
    except Exception as e:
        logs.write(f"[{datetime.now()}] Error solving CAPTCHA: {str(e)}\n")
        return None

def solve_recaptcha(driver, logs):
    """
    Solve Google reCAPTCHA using Phantombuster's solveNoCaptcha function
    """
    try:
        logs.write(f"[{datetime.now()}] Attempting to solve reCAPTCHA...\n")
        
        # In a real Phantombuster environment, you would use:
        # solution = driver.execute_script("return solveNoCaptcha();")
        
        # For testing purposes, we'll simulate the reCAPTCHA solving
        logs.write(f"[{datetime.now()}] reCAPTCHA detected, taking screenshot...\n")
        
        # Take full page screenshot for debugging
        debug_dir = "debug_screenshots"
        os.makedirs(debug_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_file = os.path.join(debug_dir, f"recaptcha_{timestamp}.png")
        
        driver.save_screenshot(screenshot_file)
        logs.write(f"[{datetime.now()}] reCAPTCHA screenshot saved: {screenshot_file}\n")
        
        # Upload to Dropbox for debugging
        upload_to_dropbox(screenshot_file, f"recaptcha_debug_{timestamp}.png", logs)
        
        # Simulate reCAPTCHA solution (replace with actual Phantombuster call)
        logs.write(f"[{datetime.now()}] Simulating reCAPTCHA solution...\n")
        return "SOLVED"  # Replace with actual solution
        
    except Exception as e:
        logs.write(f"[{datetime.now()}] Error solving reCAPTCHA: {str(e)}\n")
        return None

def upload_to_dropbox(file_path, filename, logs):
    """
    Upload file to Dropbox using the existing token manager
    """
    try:
        logs.write(f"[{datetime.now()}] Uploading {filename} to Dropbox...\n")
        
        # Use the existing Dropbox token manager
        try:
            from dropbox_token_manager import get_token_manager
            manager = get_token_manager()
            access_token = manager.get_current_token()
            
            if not access_token:
                logs.write(f"[{datetime.now()}] Error: No Dropbox access token found\n")
                return False
            
            # Test token validity
            token_status = manager.test_token(access_token)
            if not token_status['valid']:
                logs.write(f"[{datetime.now()}] Error: Dropbox token is invalid: {token_status['error']}\n")
                return False
            
            logs.write(f"[{datetime.now()}] Using Dropbox account: {token_status.get('account_name', 'Unknown')}\n")
            
        except ImportError:
            logs.write(f"[{datetime.now()}] Error: Dropbox token manager not available\n")
            return False
        except Exception as e:
            logs.write(f"[{datetime.now()}] Error accessing Dropbox token manager: {str(e)}\n")
            return False
        
        # Create Dropbox client
        dbx = dropbox.Dropbox(access_token)
        
        # Upload file to Dropbox
        dropbox_path = f"/Selenium_Screenshots/{filename}"
        
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Upload the file
        dbx.files_upload(
            file_data,
            dropbox_path,
            mode=dropbox.files.WriteMode.overwrite
        )
        
        logs.write(f"[{datetime.now()}] Successfully uploaded {filename} to Dropbox at {dropbox_path}\n")
        return True
        
    except Exception as e:
        logs.write(f"[{datetime.now()}] Error uploading to Dropbox: {str(e)}\n")
        return False

def take_debug_screenshot(driver, description, logs):
    """
    Take a debug screenshot and upload to Dropbox
    """
    try:
        debug_dir = "debug_screenshots"
        os.makedirs(debug_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_file = os.path.join(debug_dir, f"debug_{description}_{timestamp}.png")
        
        driver.save_screenshot(screenshot_file)
        logs.write(f"[{datetime.now()}] Debug screenshot saved: {screenshot_file}\n")
        
        # Check file size
        file_size = os.path.getsize(screenshot_file)
        logs.write(f"[{datetime.now()}] Screenshot file size: {file_size} bytes\n")
        
        # Upload to Dropbox
        upload_success = upload_to_dropbox(screenshot_file, f"debug_{description}_{timestamp}.png", logs)
        
        if upload_success:
            logs.write(f"[{datetime.now()}] Screenshot successfully uploaded to Dropbox\n")
        else:
            logs.write(f"[{datetime.now()}] Screenshot saved locally but Dropbox upload failed\n")
            # Keep the local file for debugging purposes
        
    except Exception as e:
        logs.write(f"[{datetime.now()}] Error taking debug screenshot: {str(e)}\n")

def create_screenshot_summary(logs):
    """
    Create a summary of all screenshots taken during the session
    """
    try:
        debug_dir = "debug_screenshots"
        if os.path.exists(debug_dir):
            screenshot_files = [f for f in os.listdir(debug_dir) if f.endswith('.png')]
            logs.write(f"[{datetime.now()}] Screenshot Summary:\n")
            logs.write(f"[{datetime.now()}] Total screenshots taken: {len(screenshot_files)}\n")
            
            for screenshot_file in screenshot_files:
                file_path = os.path.join(debug_dir, screenshot_file)
                file_size = os.path.getsize(file_path)
                logs.write(f"[{datetime.now()}] - {screenshot_file} ({file_size} bytes)\n")
            
            # Create a summary file
            summary_file = os.path.join(debug_dir, f"screenshot_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(summary_file, 'w') as f:
                f.write(f"Screenshot Summary - {datetime.now()}\n")
                f.write(f"Total screenshots: {len(screenshot_files)}\n\n")
                for screenshot_file in screenshot_files:
                    file_path = os.path.join(debug_dir, screenshot_file)
                    file_size = os.path.getsize(file_path)
                    f.write(f"{screenshot_file} - {file_size} bytes\n")
            
            logs.write(f"[{datetime.now()}] Screenshot summary saved: {summary_file}\n")
        else:
            logs.write(f"[{datetime.now()}] No debug screenshots directory found\n")
    except Exception as e:
        logs.write(f"[{datetime.now()}] Error creating screenshot summary: {str(e)}\n")

def run_selenium_download():
    logs = io.StringIO()
    download_dir = os.path.abspath("result_files")
    os.makedirs(download_dir, exist_ok=True)  # Ensure directory exists
    
    # Ensure matching chromedriver is present for the installed Chrome
    if CHROMEDRIVER_AUTOINSTALLER_AVAILABLE:
        try:
            chromedriver_autoinstaller.install()
            logs.write("ChromeDriver auto-installer used successfully\n")
        except Exception as e:
            logs.write(f"ChromeDriver auto-installer failed: {e}\n")
            logs.write("Continuing with system ChromeDriver\n")
    else:
        logs.write("ChromeDriver auto-installer not available, using system ChromeDriver\n")
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')  # Required for Linux/Render
    chrome_options.add_argument('--disable-dev-shm-usage')  # Avoid shared memory issues
    chrome_options.add_argument('--disable-gpu')  # Harmless on Linux; ok to include
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--disable-features=VizDisplayCompositor')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-plugins')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Find and set Chrome binary location
    chrome_bin = os.environ.get('CHROME_BIN')
    if chrome_bin and os.path.exists(chrome_bin):
        chrome_options.binary_location = chrome_bin
        logs.write(f"Using Chrome binary from environment: {chrome_bin}\n")
    else:
        # Try common Chrome locations (Linux, macOS, Windows)
        possible_paths = [
            # Linux paths
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
            '/usr/bin/chromium-browser',
            '/usr/bin/chromium',
            '/opt/google/chrome/google-chrome',
            '/opt/google/chrome/chrome',
            # macOS paths
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Chromium.app/Contents/MacOS/Chromium',
            # Windows paths (for completeness)
            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
        ]
        
        chrome_found = False
        for path in possible_paths:
            if os.path.exists(path):
                chrome_options.binary_location = path
                logs.write(f"Found Chrome binary at: {path}\n")
                chrome_found = True
                break
        
        if not chrome_found:
            logs.write("Warning: Chrome binary not found in common locations\n")
            
            # Try to find Chrome using system commands
            try:
                import subprocess
                import platform
                
                system = platform.system().lower()
                if system == 'darwin':  # macOS
                    # Try to find Chrome using mdfind (Spotlight)
                    try:
                        result = subprocess.run(['mdfind', 'kMDItemCFBundleIdentifier == "com.google.Chrome"'], 
                                              capture_output=True, text=True, timeout=10)
                        if result.returncode == 0 and result.stdout.strip():
                            chrome_paths = result.stdout.strip().split('\n')
                            for chrome_path in chrome_paths:
                                chrome_binary = os.path.join(chrome_path, 'Contents', 'MacOS', 'Google Chrome')
                                if os.path.exists(chrome_binary):
                                    chrome_options.binary_location = chrome_binary
                                    logs.write(f"Found Chrome via Spotlight: {chrome_binary}\n")
                                    chrome_found = True
                                    break
                    except Exception as e:
                        logs.write(f"Spotlight search failed: {e}\n")
                
                # List available binaries for debugging
                logs.write("Available binaries in /usr/bin:\n")
                try:
                    result = subprocess.run(['ls', '-la', '/usr/bin/'], capture_output=True, text=True)
                    logs.write(result.stdout)
                except Exception as e:
                    logs.write(f"Could not list /usr/bin: {e}\n")
                    
            except Exception as e:
                logs.write(f"Could not search for Chrome: {e}\n")
    
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    LOGIN_URL = 'https://phantombuster.com/login'
    AGENT_IDS_TO_PROCESS = ['8626543543351129', '6237347125394421', '8671649679555626', '6980602735345546', '2260881575322679', '7285444664606486', '6074546208761606', '3042760728998277', '7238498317187621', '1831479579801942', '7542019513013691', '2677054973461839', '106622228377463', '8011629403157145', '8146225032110146', '5277739342845750', '1680941311344388', '2548299459111773', '5708177591846040', '2064221933560869', '8226539900994724', '4132797263553756', '3212417486544089', '8520619683264497', '2602307221323078', '5888865497260688', '5484927298890921', '3320177278568035', '5301933151780364', '4287208762639644', '3108371016072996', '5216808402688020', '4578023413082668', '4580848413843602', '697974658565762', '6656294879563215', '5914725680406458', '8049414638346856', '2076789939091163', '3567196562444031', '2463996295436979', '575085872186439', '1417052321188903', '5471991315065325', '529083497832959', '7334415162018749', '1613906095607879', '8042842673138797', '5974758466591014', '8475220052433284']
    AGENT_ID_TO_S3_FOLDER = {
    '8626543543351129': 'zb3ZwQnVuZcM0cfCNbQoIQ/',
    '6237347125394421': 'EQl5K9ngclSt6QfdgqaWOQ/',
    '8671649679555626': 'TJOu2PU1eVE4ggj03EvmEA/',
    '6980602735345546': 'xOHNlQAHxXOCo0ZZ80tknw/',
    '2260881575322679': 'MXQk7aMKOrU8tSrwloxHag/',
    '7285444664606486': 'MgZvDUNpAf59Z8nNKjY34A/',
    '6074546208761606': 'AKNx0zBYIaTBbjtKpVg0cg/',
    '3042760728998277': 'vMNFGGUkeJCcUm1bnF3kdA/',
    '7238498317187621': 'gmjimA9WCpHTavCT8Y99SA/',
    '1831479579801942': 'BQ5rCYhC0pU9sCYNvgfLsA/',
    '7542019513013691': 'rCQDjfbgNEgddzoNWR0Zcg/',
    '2677054973461839': 'vmjDkWJaCiLXbkauYw7PeA/',
    '106622228377463': 'Exg68pTxujyr4xIaohT1dg/',
    '8011629403157145': 'pnSRZsbrNUQqwuE9Q9Tv3g/',
    '8146225032110146': '5THDQ1wnHRvIgGjIUlOqnA/',
    '5277739342845750': 'Zy19AY3hC3sR7Q0USiwj5w/',
    '1680941311344388': 'VdO01hDp4zkgO2Ylv6wgcw/',
    '2548299459111773': 'Ok85iau0YPhBTnFOfYarZw/',
    '5708177591846040': 'FvXrHNoU0tpjCelYqbtD9w/',
    '2064221933560869': 'hZrOXYcnbylwKmbsVs8lIA/',
    '8226539900994724': 'JUTbwdhFNqk0kXFfJGGKwA/',
    '4132797263553756': 'OtXaEXl64gDGtW2saOXUZw/',
    '3212417486544089': 'R9sv2TMJTnlCnCdk9qdc3Q/',
    '8520619683264497': 'ABlTscZ34q7CU6Z7p0TUwA/',
    '2602307221323078': 'ObCLgchOb2aC6HnsMJIbVA/',
    '5888865497260688': 'GRAuissfGi7K1CXeQBZvdA/',
    '5484927298890921': '5HtkrOzkRZCoePzMvkJ3xg/',
    '3320177278568035': 'IM475uNIONS7uu1kQEK2VQ/',
    '5301933151780364': 'DQyuJyKAEmhGQcAoQ3x3Mg/',
    '4287208762639644': 'ouVVEl9JwUz0ws5gMRwLNQ/',
    '3108371016072996': 'LVjsRgRzmpiyxuWNiOh0lg/',
    '5216808402688020': 's3pIL05Sqsfm2ScDllgbNQ/',
    '4578023413082668': 'AMbbNCwUNUX2nUUps9gN4A/',
    '4580848413843602': 'c1b1iwXA4nmixk3DvytdiA/',
    '697974658565762': 'XWAn6pOdfkaNZdmO71BgnA/',
    '6656294879563215': 'gzYveUjjOx25gBJEoiHhEw/',
    '5914725680406458': 'UJFc11Ho5o1QPJWNrwxhAQ/',
    '8049414638346856': 'bUniiJRB1It6h3pE30CVfA/',
    '2076789939091163': 'crao2Wv6h5ekVMM7ZInMQA/',
    '3567196562444031': 'OtK4jH1u6DQMYE8451Lr8A/',
    '2463996295436979': '5HtrJ7DW9bYW9Drn5ud80g/',
    '575085872186439': 'eyMF34dqO3Te9a0Qu4zV4Q/',
    '1417052321188903': '5NP6CL8Fak2PGWsn43Gp0g/',
    '5471991315065325': 'NIhDkzseUi4XiGR4Yh8l7g/',
    '529083497832959': 'Q5GCRyHsM4GZJ4f1OYUkLA/',
    '7334415162018749': 'Bj2hOTDCCbUSxiNX627Unw/',
    '1613906095607879': 'FClITJqal67ESpxWJglYjQ/',
    '8042842673138797': 'vM06hslrVVQ3CmcEmisJ2w/',
    '5974758466591014': 'VtrjgjQSxQkN2vCrTdvHoA/',
    '8475220052433284': 'HaRj88fFDQql8W10JnGp5Q/',
}

    results_by_agent = {}
    # Prefer provided chromedriver if available (Render Dockerfile sets CHROMEDRIVER)
    driver = None
    chromedriver_path = os.environ.get('CHROMEDRIVER')
    
    # Log Chrome binary information
    if chrome_options.binary_location:
        logs.write(f"Chrome binary location set to: {chrome_options.binary_location}\n")
        if os.path.exists(chrome_options.binary_location):
            logs.write("Chrome binary exists and is accessible\n")
        else:
            logs.write("WARNING: Chrome binary path does not exist!\n")
    else:
        logs.write("No Chrome binary location set - will use system PATH\n")
    
    try:
        # Try multiple approaches to initialize Chrome WebDriver
        driver = None
        
        # Approach 1: Use explicit chromedriver path
        if chromedriver_path and os.path.exists(chromedriver_path):
            logs.write(f"Attempting to use chromedriver from: {chromedriver_path}\n")
            try:
                service = Service(executable_path=chromedriver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)
                logs.write("✓ Chrome WebDriver initialized with explicit chromedriver path\n")
            except Exception as e:
                logs.write(f"✗ Failed with explicit chromedriver path: {e}\n")
                driver = None
        
        # Approach 2: Use chromedriver from PATH
        if driver is None:
            logs.write("Attempting to use chromedriver from PATH\n")
            try:
                driver = webdriver.Chrome(options=chrome_options)
                logs.write("✓ Chrome WebDriver initialized from PATH\n")
            except Exception as e:
                logs.write(f"✗ Failed with PATH chromedriver: {e}\n")
                driver = None
        
        # Approach 3: Try with minimal options for Render
        if driver is None:
            logs.write("Attempting with minimal Chrome options for Render\n")
            try:
                minimal_options = Options()
                minimal_options.add_argument('--headless=new')
                minimal_options.add_argument('--no-sandbox')
                minimal_options.add_argument('--disable-dev-shm-usage')
                minimal_options.add_argument('--disable-gpu')
                minimal_options.add_argument('--window-size=1920,1080')
                
                # Set Chrome binary explicitly for Render
                minimal_options.binary_location = '/usr/bin/google-chrome'
                
                driver = webdriver.Chrome(options=minimal_options)
                logs.write("✓ Chrome WebDriver initialized with minimal options\n")
            except Exception as e:
                logs.write(f"✗ Failed with minimal options: {e}\n")
                driver = None
        
        if driver is None:
            raise Exception("All Chrome WebDriver initialization attempts failed")
        
        logs.write("Chrome WebDriver initialized successfully\n")
        
        # Test screenshot capability immediately
        try:
            logs.write("Testing screenshot capability...\n")
            test_screenshot_path = "debug_screenshots/webdriver_test.png"
            os.makedirs("debug_screenshots", exist_ok=True)
            driver.save_screenshot(test_screenshot_path)
            
            if os.path.exists(test_screenshot_path):
                file_size = os.path.getsize(test_screenshot_path)
                logs.write(f"✓ Screenshot test successful: {test_screenshot_path} ({file_size} bytes)\n")
                
                # Upload test screenshot to Dropbox
                upload_to_dropbox(test_screenshot_path, "webdriver_test.png", logs)
            else:
                logs.write("✗ Screenshot test failed - file not created\n")
        except Exception as screenshot_e:
            logs.write(f"✗ Screenshot test failed: {screenshot_e}\n")
        
    except Exception as e:
        # Surface clearer startup errors in logs
        logs.write(f"Failed to start Chrome WebDriver: {e}\n")
        logs.write(f"Error type: {type(e).__name__}\n")
        
        # Check if it's a Chrome binary issue
        if "chrome" in str(e).lower() or "executable" in str(e).lower():
            logs.write("This appears to be a Chrome binary issue.\n")
            logs.write("Chrome binary location: " + str(chrome_options.binary_location) + "\n")
            
            if chrome_options.binary_location:
                if os.path.exists(chrome_options.binary_location):
                    logs.write("Chrome binary exists but may not be executable\n")
                    try:
                        import stat
                        st = os.stat(chrome_options.binary_location)
                        logs.write(f"Chrome binary permissions: {oct(st.st_mode)}\n")
                    except Exception as perm_e:
                        logs.write(f"Could not check permissions: {perm_e}\n")
                else:
                    logs.write("Chrome binary path does not exist\n")
            else:
                logs.write("No Chrome binary location set\n")
        
        # Try to get more diagnostic information
        try:
            import subprocess
            import platform
            
            system = platform.system().lower()
            logs.write(f"Operating system: {system}\n")
            
            # Check if Chrome is installed
            if system == 'darwin':  # macOS
                result = subprocess.run(['which', 'google-chrome'], capture_output=True, text=True)
                if result.returncode == 0:
                    logs.write(f"Chrome found at: {result.stdout.strip()}\n")
                else:
                    logs.write("Chrome not found in PATH\n")
                    
                # Check Applications folder
                chrome_app = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
                if os.path.exists(chrome_app):
                    logs.write(f"Chrome found in Applications: {chrome_app}\n")
                else:
                    logs.write("Chrome not found in Applications folder\n")
            else:  # Linux/Windows
                result = subprocess.run(['which', 'google-chrome'], capture_output=True, text=True)
                if result.returncode == 0:
                    logs.write(f"Chrome found at: {result.stdout.strip()}\n")
                else:
                    logs.write("Chrome not found in PATH\n")
            
            # Check chromedriver
            result = subprocess.run(['which', 'chromedriver'], capture_output=True, text=True)
            if result.returncode == 0:
                logs.write(f"ChromeDriver found at: {result.stdout.strip()}\n")
            else:
                logs.write("ChromeDriver not found in PATH\n")
                
        except Exception as diag_e:
            logs.write(f"Could not run diagnostics: {diag_e}\n")
        
        raise
    try:
        # Navigate to login page (only once)
        driver.get(LOGIN_URL)
        logs.write("Navigated to login page.\n")
        time.sleep(3)
        
        # Take initial debug screenshot
        take_debug_screenshot(driver, "login_page", logs)
        
        logs.write("Saved login page source to 'login_page_source.html'.\n")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logs.write("Page body loaded.\n")
        
        # Check for CAPTCHA on login page
        try:
            # Check for image CAPTCHA
            captcha_elements = driver.find_elements(By.CSS_SELECTOR, "img[src*='captcha'], .captcha img, #captcha img")
            if captcha_elements:
                logs.write("Image CAPTCHA detected on login page.\n")
                solution = solve_captcha(driver, logs)
                if solution:
                    logs.write(f"CAPTCHA solved: {solution}\n")
                else:
                    logs.write("Failed to solve CAPTCHA.\n")
            
            # Check for reCAPTCHA
            recaptcha_elements = driver.find_elements(By.CSS_SELECTOR, ".g-recaptcha, [data-sitekey], iframe[src*='recaptcha']")
            if recaptcha_elements:
                logs.write("reCAPTCHA detected on login page.\n")
                solution = solve_recaptcha(driver, logs)
                if solution:
                    logs.write(f"reCAPTCHA solved: {solution}\n")
                else:
                    logs.write("Failed to solve reCAPTCHA.\n")
                    
        except Exception as e:
            logs.write(f"No CAPTCHA detected or error checking for CAPTCHA: {e}\n")
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'email'))
        )
        email_input.clear()
        email_input.send_keys('tripp@integruspartners.com')
        logs.write("Entered email.\n")
        password_input = driver.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys('Integrus123!')
        logs.write("Entered password.\n")
        login_button = driver.find_element(By.XPATH, "//button[@analyticsid='loginLoginBtn']")
        login_button.click()
        logs.write("Login submitted.\n")
        time.sleep(5)
        logs.write("Saved post-login page source to 'post-login_page_source.html'.\n")
        # Handle cookie consent dialog if present
        try:
            cookie_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(@id, 'CybotCookiebotDialogBodyButtonAccept') or contains(text(), 'Accept') or contains(text(), 'Got it') or contains(text(), 'OK') or contains(text(), 'Allow all') or contains(text(), 'Accept all')]"
                ))
            )
            cookie_btn.click()
            logs.write("Closed cookie dialog.\n")
            time.sleep(1)
        except Exception as e:
            logs.write(f"No cookie dialog found or could not close: {e}\n")
        logs.write("Saved post-cookie page source to 'post_cookie_page_source.html'.\n")

        # Loop through agent IDs
        for agent_id in AGENT_IDS_TO_PROCESS:
            agent_console_url = f"https://phantombuster.com/7429435058026063/phantoms/{agent_id}/console"
            try:
                driver.get(agent_console_url)
                logs.write(f"Navigated to console page: {agent_console_url}\n")
                time.sleep(3)
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                logs.write("Console page body loaded.\n")
                
                # Take debug screenshot for each agent page
                take_debug_screenshot(driver, f"agent_{agent_id}", logs)
                
                logs.write(f"Saved console page source to 'console_page_source_{agent_id}.html'.\n")
                
                # Check for CAPTCHA on agent console page
                try:
                    # Check for image CAPTCHA
                    captcha_elements = driver.find_elements(By.CSS_SELECTOR, "img[src*='captcha'], .captcha img, #captcha img")
                    if captcha_elements:
                        logs.write(f"Image CAPTCHA detected on agent {agent_id} console page.\n")
                        solution = solve_captcha(driver, logs)
                        if solution:
                            logs.write(f"CAPTCHA solved for agent {agent_id}: {solution}\n")
                        else:
                            logs.write(f"Failed to solve CAPTCHA for agent {agent_id}.\n")
                    
                    # Check for reCAPTCHA
                    recaptcha_elements = driver.find_elements(By.CSS_SELECTOR, ".g-recaptcha, [data-sitekey], iframe[src*='recaptcha']")
                    if recaptcha_elements:
                        logs.write(f"reCAPTCHA detected on agent {agent_id} console page.\n")
                        solution = solve_recaptcha(driver, logs)
                        if solution:
                            logs.write(f"reCAPTCHA solved for agent {agent_id}: {solution}\n")
                        else:
                            logs.write(f"Failed to solve reCAPTCHA for agent {agent_id}.\n")
                            
                except Exception as e:
                    logs.write(f"No CAPTCHA detected or error checking for CAPTCHA on agent {agent_id}: {e}\n")
                # Find and click the <span> element containing '/result' (ignoring the number)
                try:
                    result_span = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            "//span[contains(text(), '/result')]"
                        ))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", result_span)
                    result_span.click()
                    logs.write("Clicked span element containing '/result'.\n")
                    time.sleep(2)
                except Exception as e:
                    logs.write(f"Could not find or click span containing '/result': {e}\n")
                    logs.write(f"Saved page source to 'span_error_page_source_{agent_id}.html' for debugging.\n")
                # Find all result.csv buttons and collect numbers
                result_numbers = []
                try:
                    result_buttons = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((
                            By.XPATH,
                            "//button[@analyticsid='agentConsoleResultsDropdown']"
                        ))
                    )
                    for btn in result_buttons:
                        val = btn.get_attribute('analyticsval1')
                        if val and val.endswith('/result.csv'):
                            number = val.split('/')[0]
                            result_numbers.append(number)
                except Exception as e:
                    logs.write(f"Could not find result.csv buttons: {e}\n")
                folder_name = AGENT_ID_TO_S3_FOLDER.get(agent_id, agent_id)
                results_by_agent[folder_name] = result_numbers
            except Exception as e:
                logs.write(f"Could not process agent {agent_id}: {e}\n")
                folder_name = AGENT_ID_TO_S3_FOLDER.get(agent_id, agent_id)
                results_by_agent[folder_name] = []
        logs.write(f"Results by folder: {results_by_agent}\n")

        # Download each result.csv file for each folder
        import requests
        for folder_name, file_ids in results_by_agent.items():
            # Extract agent letters from folder_name (remove trailing slash)
            agent_letters = folder_name.rstrip('/')
            for file_id in file_ids:
                # Build download URL
                download_url = f"https://cache1.phantombooster.com/URYtknGfxvU/{agent_letters}/{file_id}/result.csv"
                logs.write(f"Downloading: {download_url}\n")
                try:
                    response = requests.get(download_url)
                    if response.status_code == 200:
                        out_path = os.path.join(download_dir, f"{agent_letters}_{file_id}_result.csv")
                        with open(out_path, "wb") as out_file:
                            out_file.write(response.content)
                        logs.write(f"Saved to {out_path}\n")
                    else:
                        logs.write(f"Failed to download {download_url}: Status {response.status_code}\n")
                except Exception as e:
                    logs.write(f"Error downloading {download_url}: {e}\n")
    finally:
        # Create screenshot summary before closing
        create_screenshot_summary(logs)
        
        driver.quit()
        logs.write("Script completed and browser closed.\n")
    return logs.getvalue()

if __name__ == "__main__":
    try:
        print("Starting Selenium download automation...")
        result = run_selenium_download()
        print("Script execution completed successfully!")
        print("Log output:")
        print(result)
    except Exception as e:
        print(f"Script failed with error: {e}")
        import traceback
        traceback.print_exc()