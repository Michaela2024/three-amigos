import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ── Load pre-saved demo data ──
with open("demo_data/pm.json") as f:
    pm_data = json.load(f)
with open("demo_data/eng.json") as f:
    eng_data = json.load(f)
with open("demo_data/synthesis.json") as f:
    synthesis_data = json.load(f)
with open("demo_data/assumptions.json") as f:
    assumption_data = json.load(f)
with open("demo_data/risks.json") as f:
    risk_data = json.load(f)

print("Demo data loaded.")

os.makedirs("screenshots", exist_ok=True)

# ── Setup Chrome ──
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("http://localhost:8501")

wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
time.sleep(2)

def screenshot(name):
    path = f"screenshots/{name}.png"
    time.sleep(1.5)
    driver.save_screenshot(path)
    print(f"Screenshot saved: {path}")
    return path

def js_click(element):
    driver.execute_script("arguments[0].click();", element)
    time.sleep(1.5)

def scroll_top():
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.5)

def type_slowly(element, text):
    for word in text.split():
        element.send_keys(word + " ")
        time.sleep(0.15)

# ── SCREENSHOT 1: Landing page ──
scroll_top()
screenshot("01_landing")

# ── SCREENSHOT 2: Feature brief entered ──
textarea = driver.find_element(By.TAG_NAME, "textarea")
textarea.click()
time.sleep(0.5)
type_slowly(textarea, "Add a manual time logging field to individual issues so engineers can record hours spent")
time.sleep(2)
scroll_top()
screenshot("02_feature_entered")

# ── Open context expander ──
expander = driver.find_element(By.XPATH, "//summary[contains(., 'Build product context')]")
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", expander)
time.sleep(1.0)
js_click(expander)
time.sleep(1.5)

# ── Fill in context questions ──
inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
answers = [
    "Software engineers and engineering managers tracking work across sprints",
    "Linear is a fast keyboard-driven issue tracker with issues cycles projects and roadmaps",
    "Existing data model built around issues cycles and projects. Speed and simplicity is core philosophy",
    "If engineers have to manually log time adoption will be near zero",
]

for i, answer in enumerate(answers[:len(inputs)]):
    inputs[i].click()
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", inputs[i])
    time.sleep(0.5)
    type_slowly(inputs[i], answer)
    time.sleep(1.0)

# ── SCREENSHOT 3: Context filled ──
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(1.0)
screenshot("03_context_filled")

# ── Scroll to and click Generate Spec button ──
time.sleep(1.5)
generate_btn = driver.find_element(By.XPATH, "//button[contains(., 'Generate Spec')]")
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", generate_btn)
time.sleep(1.5)
driver.execute_script("arguments[0].click();", generate_btn)
print("Generate Spec clicked.")
time.sleep(3.0)

# ── SCREENSHOT 4: After clicking ──
scroll_top()
screenshot("04_generating")

print("\nAll UI screenshots saved.")

# ── Save payload for build_deck.js ──
demo_payload = {
    "pm": pm_data,
    "eng": eng_data,
    "synthesis": synthesis_data,
    "assumptions": assumption_data,
    "risks": risk_data,
    "screenshots": {
        "landing": "screenshots/01_landing.png",
        "feature": "screenshots/02_feature_entered.png",
        "context": "screenshots/03_context_filled.png",
        "generating": "screenshots/04_generating.png",
    }
}

with open("demo_data/payload.json", "w") as f:
    json.dump(demo_payload, f, indent=2)

print("Payload saved.")
input("Press Enter to close browser...")
driver.quit()