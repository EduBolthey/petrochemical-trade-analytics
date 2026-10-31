"""
Capture High-Resolution Screenshots of Remaining Dashboard Modules
"""
import time
import os
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

def capture_screens():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    
    driver = webdriver.Edge(options=options)
    try:
        print("Navigating to http://localhost:8501...")
        driver.get("http://localhost:8501")
        time.sleep(6)  # Wait for Streamlit to hydrate

        modes = [
            ("🤖 Predictive AI & Stress Simulator", "outputs/screenshots/06_predictive_ai_simulator.png"),
            ("💾 SQL Analytics Terminal", "outputs/screenshots/07_sql_analytics_terminal.png"),
            ("📑 LMS Submission Deliverables", "outputs/screenshots/08_lms_deliverables_hub.png"),
        ]

        for label_text, out_path in modes:
            print(f"Selecting '{label_text}'...")
            try:
                # Find the radio button element with this text
                labels = driver.find_elements(By.TAG_NAME, "label")
                clicked = False
                for l in labels:
                    if label_text in l.text:
                        l.click()
                        clicked = True
                        break
                if clicked:
                    time.sleep(3)
                    driver.save_screenshot(out_path)
                    print(f"Saved: {out_path} ({os.path.getsize(out_path)} bytes)")
                else:
                    print(f"Could not find label for {label_text}")
            except Exception as e:
                print(f"Error capturing {label_text}: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    capture_screens()
