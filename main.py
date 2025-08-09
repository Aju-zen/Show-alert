import time
import requests
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

BOT_TOKEN = "8239634152:AAHB23IElJeo5xx9pSHTmdAMiI_DZiOHQbc"
GROUP_CHAT_ID = "-4815643825"
BOT_TOKENN = "8331233397:AAEtzcIcsrelXG9tsKTAbtqz_vxelvKdI54"
GROUP_CHAT_IDD = "-4839187924"

def send_telegram_message(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": GROUP_CHAT_ID, "text": text}
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram error:", e)
       
def send_telegram_messagerunning(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKENN}/sendMessage"
        payload = {"chat_id": GROUP_CHAT_IDD, "text": text}
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram error:", e)        

def match_template_multiscale(page_img, target_img_path, threshold=0.9, scales=[1.0, 0.9, 0.8, 0.7, 0.6]):
    page_cv = cv2.cvtColor(np.array(page_img), cv2.COLOR_RGB2BGR)
    target_cv_orig = cv2.imread(target_img_path)

    if target_cv_orig is None:
        print(f"❌ Error: Target image '{target_img_path}' not found or unreadable.")
        return False

    for scale in scales:
        width = int(target_cv_orig.shape[1] * scale)
        height = int(target_cv_orig.shape[0] * scale)
        if width < 10 or height < 10:
            continue

        if width > page_cv.shape[1] or height > page_cv.shape[0]:
            continue

        target_cv = cv2.resize(target_cv_orig, (width, height), interpolation=cv2.INTER_AREA)
        res = cv2.matchTemplate(page_cv, target_cv, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        if len(loc[0]) > 0:
            return True
    return False

def check_link(url, target_img, scroll=False):
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1200,800")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)  # Wait for page load

    if scroll:
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(3)

    png = driver.get_screenshot_as_png()
    page_img = Image.open(BytesIO(png))
    driver.quit()

    found = match_template_multiscale(page_img, target_img, threshold=0.9)

    if found:
        print(f"✅ Image found on {url}")
        send_telegram_messagerunning(f"Code is running")
    else:
        print(f"❌ Image NOT found on {url}")
        send_telegram_message(f"New Shows are open")
        send_telegram_message(f"New Shows are open")
        send_telegram_message(f"New Shows are open")
        send_telegram_message(f"New Shows are open")
        send_telegram_message(f"New Shows are open on: {url}")

def main():
    link1 = "https://in.bookmyshow.com/cinemas/coimbatore/kg-cinemas-coimbatore/buytickets/KGCM/20250814"
    link2 = "https://in.bookmyshow.com/cinemas/coimbatore/karpagam-theatres-4k-dolby-atmos-coimbatore/buytickets/KARP/20250814"

    while True:
        check_link(link1, "ss1.png", scroll=True)
        check_link(link2, "ss2.png", scroll=False)
        time.sleep(120)  # Wait 2 minute before next check

if __name__ == "__main__":
    main()
