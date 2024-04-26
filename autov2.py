import subprocess
import time
import os
import signal
import sys
from time import sleep  
import datetime

now = datetime.datetime.now()

def remove_duplicates_from_mail():
    with open("success.txt", "r") as success_file:
        success_lines = success_file.readlines()

    with open("fail.txt", "r") as fail_file:
        fail_lines = fail_file.readlines()

    # Lấy email cần xoá từ dòng cuối cùng của fail.txt
    email_to_remove_fail = fail_lines[-1].strip()

    # Lấy email cần xoá từ dòng cuối cùng của success.txt
    email_to_remove_success = success_lines[-1].strip()

    # Đọc nội dung của file mail.txt
    with open("mail.txt", "r") as mail_file:
        mail_lines = mail_file.readlines()

    # Tìm và xoá dòng cần xoá trong mail.txt
    for i, line in enumerate(mail_lines):
        if email_to_remove_success in line:
            del mail_lines[i:]
        if email_to_remove_fail in line:
            del mail_lines[i:]

    # Ghi lại nội dung đã chỉnh sửa vào mail.txt
    with open("mail.txt", "w") as mail_file:
        mail_file.writelines(mail_lines)

first_run = True 

def run_auto_vote():
    print("Running remove lines")
    global first_run  # Sử dụng biến global
    if first_run:
        first_run = False
    else:
        print("Running remove lines success")
        remove_duplicates_from_mail()

while True:
    # Chạy file a.py
    run_auto_vote()
    print("Running autoVote.py")
    sleep(3)
    subprocess.run(["python", "autoVote.py"])
    print("autoVote.py terminated. Restarting...",now)