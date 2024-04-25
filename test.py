import time
import time
import os
import signal
import sys

def remove_duplicates_from_mail():
    # Đọc nội dung của file success.txt và fail.txt
   with open("mail.txt", "r") as mail_file:
    mail_lines = mail_file.readlines()
# Kiểm tra và đọc nội dung của file success.txt (nếu tồn tại)
    if os.path.exists("success.txt"):
        with open("success.txt", "r") as success_file:
            success_lines = set(success_file.readlines())
    else:
        success_lines = set()

    # Kiểm tra và đọc nội dung của file fail.txt (nếu tồn tại)
    if os.path.exists("fail.txt"):
        with open("fail.txt", "r") as fail_file:
            fail_lines = set(fail_file.readlines())
    else:
        fail_lines = set()

    # Loại bỏ các dòng trong mail.txt mà đã xuất hiện trong success.txt hoặc fail.txt
    unique_mail_lines = [line for line in mail_lines if line.strip() not in success_lines and line.strip() not in fail_lines]

    # Ghi lại nội dung đã lọc vào file mail.txt
    with open("mail.txt", "w") as mail_file:
        mail_file.writelines(unique_mail_lines)


def run_auto_vote():
    print("Bắt đầu chạy autoVote.py")
    remove_duplicates_from_mail()
    print("remove succes")

def main():
    run_auto_vote()

if __name__ == "__main__":
    main()
