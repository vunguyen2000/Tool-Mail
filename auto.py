import subprocess
import time
import os
import signal
import sys

first_run = True  # Biến cờ để theo dõi lần đầu tiên chạy

def remove_duplicates_from_mail():
    # Đọc nội dung của file success.txt và fail.txt
    success_lines = set()
    fail_lines = set()

    if os.path.exists("success.txt"):
        with open("success.txt", "r") as success_file:
            success_lines = set(success_file.readlines())

    if os.path.exists("fail.txt"):
        with open("fail.txt", "r") as fail_file:
            fail_lines = set(fail_file.readlines())

    # Đọc nội dung của file mail.txt
    with open("mail.txt", "r") as mail_file:
        mail_lines = mail_file.readlines()

    # Loại bỏ các dòng trong mail.txt mà đã xuất hiện trong success.txt hoặc fail.txt
    unique_mail_lines = [line for line in mail_lines if line not in success_lines and line not in fail_lines]

    # Ghi lại nội dung đã lọc vào file mail.txt
    with open("mail.txt", "w") as mail_file:
        mail_file.writelines(unique_mail_lines)

def run_auto_vote():
    print("Bắt đầu chạy autoVote.py")
    global first_run  # Sử dụng biến global
    if first_run:
        first_run = False
    else:
        remove_duplicates_from_mail()
    auto_vote_process = subprocess.Popen(["python", "autoVote.py"])
    time.sleep(10)
    auto_vote_process.wait() 
    print("autoVote.py đã kết thúc")

def main():
    while True:
        print("Bắt đầu một chu kỳ mới")
        # Thực hiện autoVote.py trong tiến trình con
        run_auto_vote()
        time.sleep(15)
        # Kết thúc tiến trình chính
        python = sys.executable
        subprocess.run([python, __file__])

if __name__ == "__main__":
    main()
