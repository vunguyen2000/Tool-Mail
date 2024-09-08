import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service
import math
from selenium.webdriver.support import expected_conditions as EC
import re
from time import sleep  
import os
import logging

# Kiểm tra xem thư mục OneDrive có tồn tại không
desktop_path = os.path.expanduser("~/Desktop")

# Đường dẫn tới file log.txt
log_file_path = os.path.join(desktop_path, "log.txt")

# Ensure the directory exists
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

def process_account():
    logging.info('------------ START ------------')
    options = webdriver.ChromeOptions() 
    options = uc.ChromeOptions()
    options.add_argument('--port=9516')
    options.add_argument("--lang=en-us")
    options.add_argument('--start-minimized')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-popup-blocking")  # Tắt chặn pop-up
    options.add_argument("--disable-notifications")    # Tắt thông báo
    service = Service('path/to/chromedriver')
    options.headless = True                             # Không mở trình duyệt
    driver = uc.Chrome(service=service, options=options)
    driver.get('https://mail9092.maychuemail.com:1000/')
    user = driver.find_element(By.ID, "user")
    user.send_keys("xiaomiag@xiaomi-agari.com.vn")
    passWord = driver.find_element(By.ID, "password")
    passWord.send_keys("rEFm4eNt723S")
    sleep(2)
    driver.find_element(By.NAME, 'form_login').click()
    driver.get('https://mail9092.maychuemail.com:1000/admin/users/xiaomi-agari.com.vn?order_name=quota&order_by=desc')
    sleep(2)
    rows = driver.find_elements(By.CSS_SELECTOR, 'table.style1 tbody tr')
    for index, row in enumerate(rows[:10]):
        try:
            email_element = row.find_element(By.CSS_SELECTOR, 'td:nth-of-type(3) span strong')
            email = email_element.text if email_element else 'Không có'
            quota_element = row.find_element(By.CSS_SELECTOR, 'td:nth-of-type(5)')
            quota_text = quota_element.text.strip()
            match = re.search(r'(\d+)%', quota_text)
            if match:
                percentage = float(match.group(1))
            else:
                percentage = 0
            
            # Nếu tài khoản đầu tiên có percentage dưới 85%, dừng lại không cần kiểm tra các tài khoản khác
            if index == 0 and percentage < 85:
                logging.info(f'Quota max: {percentage}%, Stop...')
                break
            
            # Ghi thông tin vào log và xử lý nếu percentage > 85%
            if percentage >= 85:
                logging.info(f'{email} - {percentage}')
                new_url = f'https://mail9092.maychuemail.com:1000/admin/profile/user/general/{email}@xiaomi-agari.com.vn'
                driver.execute_script(f"window.open('{new_url}', '_blank');")
                driver.switch_to.window(driver.window_handles[-1])
                sleep(3)
                try:
                    input_element = driver.find_element(By.CSS_SELECTOR, 'input[name="mailQuota"]')
                    value = float(input_element.get_attribute('value'))
                    input_element.clear()
                    new_percentage = 80
                    # Số cần thêm vào quota hiện tại
                    new_total_quota = value * (percentage / 100) / (new_percentage / 100)
                    new_total_quota = math.ceil(new_total_quota)
                    # Nếu số cần thêm là số lẻ, tăng lên 1 để thành số chẵn
                    if new_total_quota % 2 != 0:
                        new_total_quota += 1
                    input_element.send_keys(new_total_quota)
                    submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Save changes"]')
                    submit_button.click()
                    logging.info(f'{email}-----SUCCESS')
                except Exception as e:
                    logging.error(f'Không tìm thấy thẻ input: {e}')
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
        except Exception as e:
            logging.error('Lỗi: %s', e)
    
    logging.info('------------- END -------------')
    driver.service.stop()
    driver.quit()

def main():
    print(f"-----------------------------------START JOB-----------------------------------")
    process_account()
    print(f"--------------------------------------END--------------------------------------")

if __name__ == '__main__':
    main()
