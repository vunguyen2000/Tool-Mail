import xml.etree.ElementTree as ET
import requests

def get_auth_token(admin_url, admin_user, admin_password):
    headers = {'Content-Type': 'application/soap+xml'}
    token_xml = '''<?xml version="1.0" ?><soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
    <soap:Header><context xmlns="urn:zimbra"><format type="xml"/></context></soap:Header>
    <soap:Body><AuthRequest xmlns="urn:zimbraAdmin">
    <name>%s</name><password>%s</password></AuthRequest></soap:Body></soap:Envelope>''' % (admin_user, admin_password)

    r = requests.post(admin_url, data=token_xml, headers=headers)
    if r.status_code == 200:
        return ET.fromstring(r.content).find('.//{urn:zimbraAdmin}authToken').text
    else:
        print(f'Không thể lấy authToken. Lỗi: {r.content}')
        return None

def get_account_id_by_email(admin_url, auth_token, email):
    headers = {'Content-Type': 'application/soap+xml'}
    all_accounts_xml = '''<?xml version="1.0" ?><soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
    <soap:Header><context xmlns="urn:zimbra"><authToken>%s</authToken></context></soap:Header>
    <soap:Body><GetAllAccountsRequest xmlns="urn:zimbraAdmin"/></soap:Body></soap:Envelope>''' % auth_token

    r = requests.post(admin_url, data=all_accounts_xml, headers=headers)
    root = ET.fromstring(r.content)
    for account in root.findall('.//{urn:zimbraAdmin}account'):
        name = account.get('name')
        account_id = account.get('id')
        if name == email:
            return account_id

    return None

def change_password(admin_url, auth_token, account_id, new_password):
    headers = {'Content-Type': 'application/soap+xml'}
    set_password_xml = '''<?xml version="1.0" ?><soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
    <soap:Header><context xmlns="urn:zimbra"><authToken>%s</authToken></context></soap:Header>
    <soap:Body><SetPasswordRequest xmlns="urn:zimbraAdmin">
    <id>%s</id><newPassword>%s</newPassword></SetPasswordRequest></soap:Body></soap:Envelope>''' % (auth_token, account_id, new_password)

    r = requests.post(admin_url, data=set_password_xml, headers=headers)
    if r.status_code == 200:
        print(f'Mật khẩu của tài khoản với ID {account_id} đã được thay đổi thành công.')
    else:
        print(f'Có lỗi xảy ra khi thay đổi mật khẩu: {r.content}')

def escape_xml_chars(text):
    """Thay thế các ký tự đặc biệt trong XML để đảm bảo tính hợp lệ của XML."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')

def create_zimbra_account(admin_url, auth_token, new_account_email, new_account_password):
    headers = {'Content-Type': 'application/soap+xml'}
    email_prefix = escape_xml_chars(new_account_email.split('@')[0])
    first_name = email_prefix
    last_name = email_prefix
    display_name = email_prefix

    create_account_xml = '''<?xml version="1.0" encoding="UTF-8"?>
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
        <soap:Header>
            <context xmlns="urn:zimbra">
                <authToken>%s</authToken>
            </context>
        </soap:Header>
        <soap:Body>
            <CreateAccountRequest xmlns="urn:zimbraAdmin">
                <name>%s</name>
                <password>%s</password>
                <a n="givenName">%s</a>
                <a n="sn">%s</a>
                <a n="displayName">%s</a>
            </CreateAccountRequest>
        </soap:Body>
    </soap:Envelope>''' % (escape_xml_chars(auth_token), escape_xml_chars(new_account_email), new_account_password, first_name, last_name, display_name)

    try:
        r = requests.post(admin_url, data=create_account_xml, headers=headers)
        r.raise_for_status()  # Raise an error for bad HTTP status codes
        print(f'Tài khoản {new_account_email} đã được tạo thành công.')
    except requests.exceptions.HTTPError as err:
        print(f'HTTP Error: {err}')
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')

def delete_zimbra_account(admin_url, auth_token, account_id):
    headers = {'Content-Type': 'application/soap+xml'}
    delete_account_xml = '''<?xml version="1.0" ?><soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
    <soap:Header><context xmlns="urn:zimbra"><authToken>%s</authToken></context></soap:Header>
    <soap:Body><DeleteAccountRequest xmlns="urn:zimbraAdmin">
    <id>%s</id></DeleteAccountRequest></soap:Body></soap:Envelope>''' % (auth_token, account_id)

    r = requests.post(admin_url, data=delete_account_xml, headers=headers)
    if r.status_code == 200:
        print(f'Tài khoản với ID {account_id} đã được xóa thành công.')
    else:
        print(f'Có lỗi xảy ra khi xóa tài khoản: {r.content}')

def is_email_exists(admin_url, auth_token, email):
    headers = {'Content-Type': 'application/soap+xml'}
    get_account_xml = '''<?xml version="1.0" ?><soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
    <soap:Header><context xmlns="urn:zimbra"><authToken>%s</authToken></context></soap:Header>
    <soap:Body><GetAccountRequest xmlns="urn:zimbraAdmin">
    <account by="name">%s</account></GetAccountRequest></soap:Body></soap:Envelope>''' % (auth_token, email)

    r = requests.post(admin_url, data=get_account_xml, headers=headers)
    if r.status_code == 200:
        account_id = ET.fromstring(r.content).find('.//{urn:zimbraAdmin}account').get('id')
        return True if account_id else False
    else:
        return False

def main():
    # Giá trị mặc định
    admin_url = 'https://mail.agari.com.vn:7071/service/admin/soap'
    admin_user = 'admin@agari.com.vn'
    admin_password = 'Ag@ri2019'

    # Lấy authToken
    auth_token = get_auth_token(admin_url, admin_user, admin_password)
    if not auth_token:
        return
    options = [
    "Đổi mật khẩu",
    "Tạo tài khoản mới",
    "Xóa tài khoản",
    "Kiểm tra tài khoản",
    "Thoát"
    ]
    while True:
        for i, option in enumerate(options, start=1):
             print(f"{i}. {option}")
        choice = input("Nhập số lựa chọn (1/2/3/4/5): ")

        if choice == '1':
            email = input("Nhập địa chỉ email của tài khoản: ")
            new_password = input("Nhập mật khẩu mới: ")
            account_id = get_account_id_by_email(admin_url, auth_token, email)
            if account_id:
                change_password(admin_url, auth_token, account_id, new_password)
            else:
                print(f'Không tìm thấy tài khoản với địa chỉ email: {email}')
        elif choice == '2':
            new_account_email = input("Nhập mail(Exp:vu.nguyen@agari.com.vn): ")
            new_account_password = input("Nhập mật khẩu của tài khoản mới (>6 kí tự): ")
            create_zimbra_account(admin_url, auth_token, new_account_email, new_account_password)
        elif choice == '3':
            email = input("Nhập địa chỉ email của tài khoản cần xóa: ")
            account_id = get_account_id_by_email(admin_url, auth_token, email)
            if account_id:
                delete_zimbra_account(admin_url, auth_token, account_id)
            else:
                print(f'Không tìm thấy tài khoản với địa chỉ email: {email}')
        elif choice == '4':
            email = input("Nhập email của tài khoản cần kiểm tra: ")
            if is_email_exists(admin_url, auth_token, email):
               print(f"Mail ${email} đã tồn tại")
            else:
               print(f'Không tìm thấy tài khoản với địa chỉ email: {email}')
        elif choice == '5':
            print("Đang thoát...")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

if __name__ == '__main__':
    main()
