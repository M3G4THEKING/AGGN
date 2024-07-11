
# api_key = '7sEafeeK98qtzPBd4G2DsJzvUDsiQVdwI8nIeSrT2Jargb4f5Iv1nFjM13W6KLCl'

import requests
import json
import time
import undetected_chromedriver as uc
import binascii

# from ninjemail.utils.webdriver_utils import create_driver

def get_fingerprint(api_key):
    url = f"https://fingerprints.bablosoft.com/prepare?key={api_key}"
    attempts = 0
    while attempts < 15:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                fingerprint_data = response.json()
                if 'trylater' not in fingerprint_data:
                    print("Fingerprint retrieved successfully")
                    return fingerprint_data
                else:
                    print("Server asks to try later, waiting...")
            except json.JSONDecodeError:
                print("Failed to decode JSON response")
        else:
            print(f"Request failed with status code {response.status_code}")
        attempts += 1
        time.sleep(20)
    raise Exception("Failed to get a valid fingerprint after several attempts")

def apply_fingerprint(driver, fingerprint):
    fingerprint_json = fingerprint.get('attr', {})
    user_agent = fingerprint.get('ua', '')
    payload = fingerprint.get('payload', '')
    print(payload)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": f"{payload}\nconsole.log('Fingerprint payload applied');"
        })



    # Применение остальных отпечатков
    if user_agent:
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
    
    # # Установка экрана
    # if 'screen' in fingerprint_json:
    #     screen = fingerprint_json['screen']
    #     if 'width' in screen and 'height' in screen:
    #         width = screen['width']
    #         height = screen['height']
    #         driver.set_window_size(width, height)

 






def create_driver(fingerprint):
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en-us'})

    driver = uc.Chrome(options=options, headless=False, use_subprocess=False)

    apply_fingerprint(driver, fingerprint)

    return driver


def test_fingerprint_application(api_key):
    fingerprint = get_fingerprint(api_key)
    print('new userAgent', fingerprint['attr']['navigator.userAgent'])
    print('new platform', fingerprint['attr']['navigator.platform'])
  

    driver = create_driver(fingerprint)
    # driver.get('https://www.deviceinfo.me/')
    driver.get('https://browserleaks.com/canvas')

    browser_user_agent = driver.execute_script("return navigator.userAgent;")
    print("User-Agent from Browser:", browser_user_agent)
    browser_user_platform = driver.execute_script("return navigator.platform;")
    print("Platform from Browser:", browser_user_platform)

    # Проверка консольных логов браузера
    browser_logs = driver.get_log("browser")
    for log in browser_logs:
        print(log)

    # canvas_data = driver.execute_script("return document.createElement('canvas').toDataURL();")
    # print("Canvas Data:", canvas_data)



    # Увеличим время ожидания для анализа страницы
    time.sleep(160)  # Можно настроить время по вашему усмотрению

    driver.quit()


if __name__ == '__main__':
    api_key = '7sEafeeK98qtzPBd4G2DsJzvUDsiQVdwI8nIeSrT2Jargb4f5Iv1nFjM13W6KLCl'
    test_fingerprint_application(api_key)

