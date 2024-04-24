import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep  


name = 'benjones665j@gmail.com'
passW = 'gdhjgjgu67'

# name = '18521671@gm.uit.edu.vn'
# passW = '1260446392'

driverVote = webdriver.Chrome()
# #Open bài vote
driverVote.get('https://vnba.com.vn/net-dep-banker/bai-du-thi/3575')
driverVote.find_element(By.XPATH, '/html/body/main/div[3]/div[1]/div[2]/div/button').click()

WebDriverWait(driverVote, 10).until(EC.presence_of_element_located((By.ID, 'email')))
driverVote.find_element(By.ID, 'email').send_keys(name)
driverVote.find_element(By.XPATH, '/html/body/main/div[3]/div/div/div/form/div[2]/button').click()
sleep(1)
# # Khởi tạo trình duyệt và mở Gmail
options = webdriver.ChromeOptions() 
options.add_argument("--lang=en-us")
options = uc.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = uc.Chrome(options=options)
# #Nhập mail
# #######
driver.get('https://accounts.google.com/v3/signin/identifier?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=AccountChooser&ec=asw-gmail-globalnav-signin&theme=mn&ddm=0')

# Chờ cho trang tải hoàn toàn
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'identifierId')))

# Điền thông tin đăng nhập
email_field = driver.find_element(By.ID, 'identifierId')  
email_field.send_keys(name)
email_field.send_keys(Keys.ENTER)
# Chờ cho trang tải hoàn toàn
sleep(3)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'Passwd')))
# Điền mật khẩu và đăng nhập
driver.find_element(By.NAME, 'Passwd').send_keys(passW)
driver.find_element(By.ID, 'passwordNext').click()
sleep(3)
# Chờ để đảm bảo đăng nhập hoàn tất
WebDriverWait(driver, 10).until(EC.url_contains("mail.google.com"))
print("Đăng nhập thành công!")

# Chờ cho trang Gmail tải hoàn toàn
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="main"]')))

# Tìm và nhấp vào email gần nhất
latest_emails = driver.find_elements(By.CSS_SELECTOR, '[role="main"] .zA')

# Duyệt qua 2 email mới nhất để tìm email từ người gửi B
code = None
for email in latest_emails[:2]:  # Chỉ lấy 2 email mới nhất
    sender = email.find_element(By.CSS_SELECTOR, '.zF').get_attribute('email')
    if sender == 'info@vnba.com.vn':
        email.click()
        # Lấy tiêu đề của email từ người gửi B
        email_title_element = driver.find_element(By.CSS_SELECTOR, 'h2[class="hP"]')
        code = email_title_element.text.split(":")[-1].strip()
        # Lưu tiêu đề vào danh sách
        break 
if code:
    print("Code", code)
else:
    print("Không tìm thấy Code mới nhất.")
#######
#Nhập code
driverVote.find_element(By.XPATH, '/html/body/main/div[3]/div/div/div[1]/form/div[1]/div/input').send_keys(code)
sleep(1)
driverVote.find_element(By.XPATH, '/html/body/main/div[3]/div/div/div[1]/form/div[2]/button').click()
print("SUCCESS")
# Bình chọn
sleep(2)
driverVote.find_element(By.XPATH, '/html/body/main/div[3]/div[1]/div[2]/div/button').click()
print("DONE")
# Sau khi đăng nhập, bạn có thể thực hiện các thao tác khác ở đây
driverVote.quit()
driver.quit()