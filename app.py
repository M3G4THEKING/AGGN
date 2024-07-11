from ninjemail import Ninjemail

def get_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = file.readlines()
    return [proxy.strip() for proxy in proxies]


if __name__ == '__main__':
    working_proxies = get_proxies('working_proxies.txt')

    print('######## init ##########')
    ninja = Ninjemail(
        browser="chrome",
        captcha_keys={"capsolver":"CAP-3B5921360B2858E989C79C5B773E069F"},
        sms_keys={"smspool": {"token": "pwC2M0S5QJlLh01vMtYdqqhws0WkXxY2"}},
        proxies=working_proxies,
        # auto_proxy=True

    )

    print('######## create ##########')
    # Создание Gmail аккаунта
    try:
        email, password = ninja.create_gmail_account(
            username="vantuz755643277", 
            password="paganizondar", 
            first_name="John", 
            last_name="Doe", 
            birthdate="01-01-1990",
            use_proxy=True
        )

        print(f"Email: {email}")
        print(f"Password: {password}")
    except Exception as e:
        print(f"Failed to create Gmail account: {e}")

