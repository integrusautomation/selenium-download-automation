from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import io
from datetime import datetime

try:
    import chromedriver_autoinstaller
    chromedriver_autoinstaller.install()
except ImportError:
    pass

def take_debug_screenshot(driver, description, logs):
    try:
        debug_dir = "debug_screenshots"
        os.makedirs(debug_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_file = os.path.join(debug_dir, f"{description}_{timestamp}.png")
        driver.save_screenshot(screenshot_file)
        logs.write(f"[{datetime.now()}] Debug screenshot saved: {screenshot_file}\n")
    except Exception as e:
        logs.write(f"[{datetime.now()}] Error taking screenshot: {str(e)}\n")

def run_cleanup_via_results_dropdown():
    logs = io.StringIO()
    logs.write(f"[{datetime.now()}] Starting cleanup: Using 'View all files' from results dropdown\n")

    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')

    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        logs.write("Chrome WebDriver started\n")
        take_debug_screenshot(driver, "webdriver_test", logs)

        # === LOGIN ===
        driver.get('https://phantombuster.com/login')
        logs.write("On login page\n")
        time.sleep(3)
        take_debug_screenshot(driver, "login_page", logs)

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'email')))

        driver.find_element(By.NAME, 'email').send_keys('integrusautomation@gmail.com')
        driver.find_element(By.NAME, 'password').send_keys('Integrus123!')
        driver.find_element(By.XPATH, "//button[@analyticsid='loginLoginBtn']").click()
        logs.write("Login submitted\n")

        time.sleep(10)
        take_debug_screenshot(driver, "after_login", logs)

        # Handle cookie consent
        try:
            cookie_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Allow all')]"))
            )
            cookie_btn.click()
            logs.write("Cookie consent accepted\n")
        except:
            logs.write("No cookie consent\n")

        # === GO TO AGENT CONSOLE ===
        AGENT_ID = '8379942987033743'  # Agent with many results
        agent_url = f"https://phantombuster.com/7429435058026063/phantoms/{AGENT_ID}/console"
        driver.get(agent_url)
        logs.write(f"Navigated to agent console: {agent_url}\n")

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(8)
        take_debug_screenshot(driver, "agent_console_loaded", logs)

        # === CLICK THE DROPDOWN ARROW NEXT TO "xxxxx/result" ===
        # This is the <span> with class "text-heading-highlight" and "cursor-pointer" that contains a span with text like "000000060/result"
        try:
            # Find the outer span that has both text-heading-highlight and cursor-pointer classes and contains a child span with "/result"
            results_dropdown = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'text-heading-highlight') and contains(@class, 'cursor-pointer') and .//span[contains(text(), '/result')]]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", results_dropdown)
            time.sleep(1)
            results_dropdown.click()
            logs.write("Clicked the results dropdown (span containing '/result')\n")
            time.sleep(3)
            take_debug_screenshot(driver, "results_dropdown_opened", logs)
        except Exception as e:
            logs.write(f"Could not click results dropdown: {e}\n")
            take_debug_screenshot(driver, "error_results_dropdown", logs)
            raise

        # === CLICK "View all files" IN THE DROPDOWN ===
        try:
            view_all_files_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[analyticsid='agentConsoleViewAllFiles']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_all_files_btn)
            time.sleep(1)
            view_all_files_btn.click()
            logs.write("Clicked 'View all files' button\n")
            time.sleep(10)  # Give time for file browser to load (may open in new tab or same)
            take_debug_screenshot(driver, "after_view_all_files_click", logs)
        except Exception as e:
            logs.write(f"Could not find/click View all files button: {e}\n")
            take_debug_screenshot(driver, "error_view_all_files", logs)
            raise

        # === HANDLE POSSIBLE NEW TAB ===
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            logs.write("Switched to new tab (file browser opened in new tab)\n")
            time.sleep(8)
            take_debug_screenshot(driver, "file_browser_new_tab", logs)
        else:
            logs.write("File browser loaded in same tab\n")
            time.sleep(5)

        # === NOW IN FILE BROWSER: DELETE OLD FILES ===
        # Optional: Click into the agent's folder if needed
        try:
            folder_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-prefix='URYtknGfxvU/'][data-bucket='phantombuster']"))
            )
            folder_link.click()
            logs.write("Clicked into agent folder\n")
            time.sleep(5)
            take_debug_screenshot(driver, "inside_agent_folder", logs)
        except:
            logs.write("Already inside folder or not needed\n")

        # Select all
        select_all = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "select-all"))
        )
        select_all.click()
        logs.write("Selected all files\n")
        time.sleep(3)
        take_debug_screenshot(driver, "all_files_selected", logs)

        # Click trash icon
        trash_icon = driver.find_element(By.ID, "bucket-trash")
        trash_icon.click()
        logs.write("Clicked trash icon\n")
        time.sleep(3)

        # Confirm delete
        delete_confirm = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "trash-btn-delete"))
        )
        delete_confirm.click()
        logs.write("Confirmed deletion - old files deleted!\n")
        time.sleep(15)
        take_debug_screenshot(driver, "deletion_complete", logs)

        logs.write("Cleanup finished successfully!\n")

    except Exception as e:
        logs.write(f"ERROR: {str(e)}\n")
        import traceback
        logs.write(traceback.format_exc() + "\n")
        if driver:
            take_debug_screenshot(driver, "final_error", logs)

    finally:
        if driver:
            driver.quit()
            logs.write("Browser closed\n")

    return logs.getvalue()


if __name__ == "__main__":
    print("Starting Phantombuster old files cleanup (via results dropdown)...")
    log_output = run_cleanup_via_results_dropdown()
    print("\n=== FULL LOG ===\n")
    print(log_output)
    print("=== DONE ===\nCheck debug_screenshots/ for step-by-step visuals!")
