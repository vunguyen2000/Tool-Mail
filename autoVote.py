import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep  
from selenium.common.exceptions import TimeoutException
import psutil
import os
from selenium.common.exceptions import NoSuchElementException

def mailProcess(driver,driverVote,line):
    print("Process mail...")
    try : 
         latest_emails = driver.find_elements(By.CSS_SELECTOR, '[role="main"] .zA')
         for email in latest_emails[:5]:
             sender = driver.execute_script("""
    var emailElement = arguments[0];
    return emailElement.querySelector('.zF').getAttribute('email');
""", email)
             print("sender",sender)
             if sender == 'info@vnba.com.vn':
                 email.click()
                 email_title_element = driver.find_element(By.CSS_SELECTOR, 'h2[class="hP"]')
                 code = email_title_element.text.split(":")[-1].strip()
                 break
             else:
                with open('fail.txt', 'a') as process_file:
                    process_file.write("{}\n".format(line))
                kill_chrome_processes(driverVote,driver)
                return
         if code:
             print("Code", code)
         else:
            with open('fail.txt', 'a') as process_file:
              process_file.write("{}\n".format(line))
              kill_chrome_processes(driverVote,driver)
    except:
         print("CAN'T CLICK CODE 5 MINUE")
        #  driver.service.stop()
        #  driver.quit()
         kill_chrome_processes(driverVote,driver)
         return

def kill_chrome_processes(driverVote,driver):
    driverVote.service.stop()
    driverVote.quit()
    driver.service.stop()
    driver.quit()
    # os.system("taskkill /f /im geckodriver.exe /T")
    # os.system("taskkill /f /im chromedriver.exe /T")
    # os.system("taskkill /f /im IEDriverServer.exe /T")
    # for proc in psutil.process_iter():
    #     try:
    #         # Kiểm tra xem tên của quy trình có phải là "chrome.exe" không
    #         if "chrome.exe" in proc.name():
    #             # Tắt quy trình
    #             proc.kill()
    #     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
    #         pass

def process_account(line,name, passW):
    optionsOne = webdriver.ChromeOptions() 
    optionsOne.add_argument('--port=9515')
    optionsOne.add_argument('--start-minimized')
    driverVote = webdriver.Chrome(options=optionsOne)
    # #Open bài vote
    driverVote.get('https://vnba.com.vn/net-dep-banker/bai-du-thi/3575')
    driverVote.find_element(By.XPATH, '/html/body/main/div[3]/div[1]/div[2]/div/button').click()

    WebDriverWait(driverVote, 10).until(EC.presence_of_element_located((By.ID, 'email')))
    driverVote.find_element(By.ID, 'email').send_keys(name)
    driverVote.find_element(By.XPATH, '/html/body/main/div[3]/div/div/div/form/div[2]/button').click()
    sleep(1)
    # # Khởi tạo trình duyệt và mở Gmail
    options = webdriver.ChromeOptions() 
    options = uc.ChromeOptions()
    options.add_argument('--port=9516')
    options.add_argument("--lang=en-us")
    options.add_argument('--start-minimized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = uc.Chrome(options=options)
    # #Nhập mail
    # #######
    driver.get('https://accounts.google.com/v3/signin/identifier?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=AccountChooser&ec=asw-gmail-globalnav-signin&theme=mn&ddm=0')

    # Chờ cho trang tải hoàn toàn
    WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.ID, 'identifierId')))

    # Điền thông tin đăng nhập
    email_field = driver.find_element(By.ID, 'identifierId')  
    email_field.send_keys(name)
    email_field.send_keys(Keys.ENTER)
    # Chờ cho trang tải hoàn toàn
    try:
        WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.NAME, 'Passwd')))
        sleep(2)
        driver.find_element(By.NAME, 'Passwd').send_keys(passW)
        # current_window = driver.current_window_handle
        driver.find_element(By.ID, 'passwordNext').click()
        # WebDriverWait(driver, 5).until(EC.new_window_is_opened(current_window))
        # if len(driver.window_handles) > 1:
        #      pass
        # else:
        #      with open('fail.txt', 'a') as process_file:
        #         process_file.write("{}\n".format(line))
        #         driverVote.service.stop()
        #         driverVote.quit()
        #         driver.service.stop()
        #         driver.quit()
        #         kill_chrome_processes()
        #      return
        try:
            js_script = 'document.querySelector(".VfPpkd-RLmnJb").click();'
            driver.execute_script(js_script)
        except:
            pass
    except TimeoutException:
        with open('fail.txt', 'a') as process_file:
              process_file.write("{}\n".format(line))
            #   driverVote.service.stop()
            #   driverVote.quit()
            #   driver.service.stop()
            #   driver.quit()
              kill_chrome_processes(driverVote,driver)
        return
    WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.NAME, 'Passwd')))
    # Điền mật khẩu và đăng nhập
    try:
            sleep(5)
            js_script = 'document.querySelector(".VfPpkd-RLmnJb").click();'
            driver.execute_script(js_script)
            try:
                sleep(1)
                element_exists = driver.execute_script("return document.querySelector('.ahr:first-of-type') !== null;")
                sleep(2)
                if element_exists:
                    driver.execute_script("document.querySelector('.ahr:first-of-type').click()")
                    sleep(1)
                    driver.execute_script("document.querySelector('button[name=data_consent_dialog_next]').click()")
                    sleep(1)
                    driver.execute_script("document.querySelectorAll('.ahr')[2].click();")
                    sleep(1)
                    driver.execute_script("document.querySelector('button[name=data_consent_dialog_done]').click()")
                    sleep(4)
                    driver.execute_script("document.querySelector('button[name=r]').click()")
            except:
                pass
    except:
           try:
                sleep(1)
                element_exists = driver.execute_script("return document.querySelector('.ahr:first-of-type') !== null;")
                sleep(2)
                if element_exists:
                    driver.execute_script("document.querySelector('.ahr:first-of-type').click()")
                    sleep(1)
                    driver.execute_script("document.querySelector('button[name=data_consent_dialog_next]').click()")
                    sleep(1)
                    driver.execute_script("document.querySelectorAll('.ahr')[2].click();")
                    sleep(1)
                    driver.execute_script("document.querySelector('button[name=data_consent_dialog_done]').click()")
                    sleep(4)
                    driver.execute_script("document.querySelector('button[name=r]').click()")
           except:
               pass
           try:
            sleep(2)
            WebDriverWait(driver, 10).until(EC.url_contains("mail.google.com"))
            # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="main"]')))
           except:
                #  driver.service.stop()
                #  driver.quit()
                 kill_chrome_processes(driverVote,driver)
                 return
    try : 
         sleep(3)
         latest =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="main"] .zA')))
        #  latest_emails = driver.find_elements(By.CSS_SELECTOR, '[role="main"] .zA')
         latest_emails = driver.execute_script("return document.querySelectorAll('[role=\"main\"] .zA')")
         code = None
        #  flag = True
         for email in latest_emails[:3]:
             sender = driver.execute_script("""
    var emailElement = arguments[0];
    return emailElement.querySelector('.zF').getAttribute('email');
    return emailElement.querySelector('.zF').getAttribute('email');
""", email)
             if sender == 'info@vnba.com.vn':
                 email.click()
                 email_title_element = driver.find_element(By.CSS_SELECTOR, 'h2[class="hP"]')
                 code = email_title_element.text.split(":")[-1].strip()
                 break
            #  elif sender != 'info@vnba.com.vn' and flag:
            #      print("Waiting...")
            #      sleep(60)
            #      return mailProcess(driver,driverVote,line)
         if code:
             print("Code", code)
         else:
            with open('fail.txt', 'a') as process_file:
              process_file.write("{}\n".format(line))
              kill_chrome_processes(driverVote,driver)
    except:
         print("CAN'T CLICK CODE")
         with open('fail.txt', 'a') as process_file:
            process_file.write("{}\n".format(line))
         kill_chrome_processes(driverVote,driver)
         return
    #Nhập code
    driverVote.find_element(By.XPATH, '/html/body/main/div[3]/div/div/div[1]/form/div[1]/div/input').send_keys(code)
    sleep(1)
    driverVote.find_element(By.XPATH, '/html/body/main/div[3]/div/div/div[1]/form/div[2]/button').click()
    # Bình chọn
    # driverVote.find_element(By.XPATH, '/html/body/main/div[3]/div[1]/div[2]/div/button').click()
    try:
        sleep(1)
        button_element = driverVote.find_element(By.XPATH, '/html/body/main/div[3]/div[1]/div[2]/div/button')
        button_element.click()
        print(name,"SUCCESS")
    except:
        with open('fail.txt', 'a') as process_file:
              process_file.write("{}\n".format(line))
              kill_chrome_processes(driverVote,driver)
        return
    # Sau khi đăng nhập, bạn có thể thực hiện các thao tác khác ở đây
    # driverVote.service.stop()
    # driverVote.quit()
    # driver.service.stop()
    # driver.quit()
    kill_chrome_processes(driverVote,driver)
    with open('success.txt', 'a') as process_file:
        process_file.write("{}\n".format(line))
    with open('successCopy.txt', 'a') as process_file:
        process_file.write("{}\n".format(line))

with open('mail.txt', 'r', encoding='utf-8') as file:
    data = file.read()
lines = data.split('\n')
accounts = []
for line in reversed(lines):
    if line.strip():  # Bỏ qua các dòng trống
        if line.startswith("Good|"):  # Kiểm tra xem dòng có bắt đầu bằng "Good|" hay không
            parts = line.split(':')
            if len(parts) == 3:  # Đảm bảo rằng mỗi dòng có đúng 3 phần
                account = parts[0].split('|')[1]
                password = parts[1]
                accounts.append({'account': account, 'password': password})
                print("account : ",account)
                process_account(line,account, password)