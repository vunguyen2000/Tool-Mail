import time
import subprocess
import datetime

now = datetime.datetime.now()

def kill_chrome_background_processes():
    print("KILL time: ",now)
    subprocess.call("TASKKILL /f /im chrome.exe", shell=True)
    subprocess.call("TASKKILL /f /im chromedriver.exe", shell=True)

# Hàm này sẽ chạy mã để tắt tiến trình Chrome sau mỗi 10 phút
def main():
    while True:
        kill_chrome_background_processes() # Gọi hàm để tắt tiến trình Chrome
        time.sleep(595)  # Chờ 10 phút (600 giây) trước khi thực hiện lại

if __name__ == "__main__":
    main()
