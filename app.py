import time
import os
from datetime import datetime

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADRESS = os.getenv("APP_FXMG_EMAIL")
PASSWORD = os.getenv("APP_FXMG_PASS")

TOKEN = os.getenv("APP_TG_TOKEN")
CHAT_ID = os.getenv("APP_CHAT_ID")

def send_message(msg):
    base_url = f"https://api.telegram.org/bot{TOKEN}/"
    url = f"{base_url}sendMessage?chat_id={CHAT_ID}&text={msg}&parse_mode=Markdown"
    if msg is not None:
        requests.get(url)

def write_to_txt(type, msg):
    if type == "msg":
        with open("latest_msg.txt", "w") as f:
            f.write(msg)
    elif type == "time":
        with open("latest_status_check.txt", "w") as f:
            f.write(msg)


def read_from_txt(type):
    if type == "msg":
        with open("latest_msg.txt", "r") as f:
            msg = f.read()
            return msg
    elif type == "time":
        with open("latest_status_check.txt", "r") as f:
            msg = f.read()
            return msg


def scroll_down(driver, count):
    for i in range(count):
        WebDriverWait(driver, 1)

        # Scroll down to the bottom of the page using JavaScript
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        WebDriverWait(driver, 1)

def daily_status_check():
    now = datetime.now()

    curr_date = now.date()
    formatted_curr_date = curr_date.strftime("%Y-%m-%d")

    curr_time = now.time()
    formatted_curr_time = curr_time.strftime("%H:%M")

    target_time = datetime.strptime("08:00", "%H:%M")
    formatted_target_time = target_time.strftime("%H:%M")

    last_status_check = read_from_txt("time")

    if formatted_curr_time == formatted_target_time and formatted_curr_date != last_status_check:
        print("Daily check successful!")
        send_message("Daily check successful!")
        write_to_txt("time", formatted_curr_date)

def hourly_refresh(driver):
    curr_time = datetime.now().time()

    if curr_time.minute == 0 and (curr_time.second >= 0 and curr_time.second <= 10):
        driver.refresh()
        print("Successful refresh!")
        WebDriverWait(driver, 3)
        time.sleep(3)


def main():
    try:
        url = "https://forexamg.com/login"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--profile-directory=Default')
        chrome_options.add_argument("--disable-notifications")

        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()

        driver.get(url)

        WebDriverWait(driver, 1)
        time.sleep(1)

        email_inputs = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.NAME, "email")))
        email_inputs[0].click()
        email_inputs[0].clear()
        time.sleep(1)
        email_inputs[0].send_keys(EMAIL_ADRESS)
        time.sleep(1)

        WebDriverWait(driver, 1)
        time.sleep(1)

        password_input = driver.find_element(By.NAME, "password")
        password_input.click()
        password_input.clear()
        time.sleep(1)
        password_input.send_keys(PASSWORD)
        time.sleep(1)

        WebDriverWait(driver, 1)
        time.sleep(1)

        password_input.send_keys(Keys.ENTER)
        time.sleep(1)

        WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "left_side_download_app")))

        scroll_down(driver, 3)

        latest_msg = {}
        latest_msg_txt = read_from_txt("msg")

        WebDriverWait(driver, 1)
        time.sleep(1)

        while True:
            daily_status_check()
            hourly_refresh(driver)

            cards = driver.find_elements(By.CLASS_NAME, "signals_content_blog")

            if cards:
                last_card = cards[-1]

                a_tag = last_card.find_element(By.CLASS_NAME, "fancybox")
                link = a_tag.get_attribute("href")

                pre_tag = last_card.find_element(By.TAG_NAME, "pre")
                span_tag = pre_tag.find_element(By.TAG_NAME, "span")
                text = span_tag.text

                h5_tag = last_card.find_element(By.TAG_NAME, "h5")
                time_txt = h5_tag.text

                message = f"""**{text}** \n\n*{link}* \n\n{time_txt}"""

                if message != latest_msg and message != latest_msg_txt:
                    latest_msg = message
                    print(latest_msg)
                    send_message(latest_msg)
                    write_to_txt("msg", latest_msg)
                    scroll_down(driver, 3)

                time.sleep(2)

    except Exception as err:
        print(f"Error: {err}")


if __name__ == '__main__':
    main()
