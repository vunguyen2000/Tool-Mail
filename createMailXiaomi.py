import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service
import os
import logging
from time import sleep

# Cấu hình logging
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "logXiaomi.txt")
logging.basicConfig(filename=desktop_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def create_password(email):
    # Tạo mật khẩu theo định dạng: loại bỏ dấu . và thêm 123
    base_name = email.split('@')[0].replace('.', '')
    return f'{base_name}123'

def process_account():
    options = webdriver.ChromeOptions()
    options = uc.ChromeOptions()
    options.add_argument('--port=9516')
    options.add_argument("--lang=en-us")
    options.add_argument('--start-minimized')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-popup-blocking")
    options.headless = True  
    options.add_argument("--disable-notifications")
    service = Service('path/to/chromedriver')
    driver = uc.Chrome(service=service, options=options)
    driver.get('https://mail9092.maychuemail.com:1000/')
    
    # Đăng nhập
    user = driver.find_element(By.ID, "user")
    user.send_keys("xiaomiag@xiaomi-agari.com.vn")
    passWord = driver.find_element(By.ID, "password")
    passWord.send_keys("rEFm4eNt723S")
    sleep(2)
    driver.find_element(By.NAME, 'form_login').click()
    sleep(2)

    # Đọc email từ file trên Desktop
    emails_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "emailsXiaomi.txt")
    with open(emails_file_path, 'r') as file:
        emails = file.readlines()[1:] #Bỏ dòng đầu
    
    for email in emails:
        email = email.strip()  
        driver.get('https://mail9092.maychuemail.com:1000/admin/create/user/xiaomi-agari.com.vn')
        account = email.split('@')[0]
        sleep(2)
        
        while True:  # Vòng lặp bên trong để xử lý lỗi
            try:
                # Nhập thông tin vào các trường
                print(f"\nTạo email mới: {email}")
                new_password = create_password(email)
                user_name = driver.find_element(By.NAME, "username")
                user_name.clear()
                user_name.send_keys(account)
                new_pass = driver.find_element(By.NAME, "newpw")
                new_pass.clear()
                new_pass.send_keys(new_password)
                confirm_pass = driver.find_element(By.NAME, "confirmpw")
                confirm_pass.clear()
                confirm_pass.send_keys(new_password)
                display_name = driver.find_element(By.NAME, "cn")
                display_name.clear()
                display_name.send_keys(account)
                quota = driver.find_element(By.NAME, "mailQuota")
                quota.clear()
                quota.send_keys(500)
                element = driver.find_element(By.NAME, 'submit_add_user')
                element.click()
                # Kiểm tra URL để xác định xem tạo email có thành công hay không
                sleep(2)  # Đợi một chút cho trang chuyển hướng
                current_url = driver.current_url
                if "?msg=CREATED" in current_url:
                    print(f"Tạo email {email} thành công.")
                    logging.info(f'{email}@xiaomi-agari.com.vn - {new_password}')
                    # Mở tab mới với URL tạo email
                    driver.execute_script("window.open('https://mail9092.maychuemail.com:1000/admin/create/user/xiaomi-agari.com.vn', '_blank');")
                    sleep(2)  # Đợi một chút để tab mới được mở
                    driver.close()  # Đóng tab cũ
                    driver.switch_to.window(driver.window_handles[0])  # Chuyển đến tab mới
                    sleep(2)  # Đợi một chút trước khi tiếp tục
                    break  # Thoát khỏi vòng lặp bên trong nếu thành công
                else:
                    print("Mail đã tồn tại hoặc có lỗi. Vui lòng kiểm tra lại.")
                    logging.error(f'Email {email}')
                    sleep(2)
                    break  # Thoát khỏi vòng lặp bên trong nếu có lỗi không thể khắc phục
            except Exception as e:
                print(f"Có lỗi xảy ra: {e}")
                logging.error(f'Lỗi khi tạo email {email}')
                sleep(2)
                break  # Thoát khỏi vòng lặp bên trong nếu có lỗi xảy ra
    driver.service.stop()
    driver.quit()

def main():
    print(f"---------------------------CREATE ACCOUNT IN emailsXiaomi.txt...---------------------------")
    print(f"-----------------------------------STARTING...-----------------------------------")
    process_account()
    print(f"-------------------------------------END-----------------------------------------")

if __name__ == '__main__':
    main()
