import requests
from requests.exceptions import ProxyError, ConnectTimeout, ReadTimeout

def check_proxy(proxy):
    proxies = {
        'http': f'socks5h://{proxy}',
        'https': f'socks5h://{proxy}'
    }
    try:
        response = requests.get('http://www.google.com', proxies=proxies, timeout=10)
        if response.status_code == 200:
            return True
    except (ProxyError, ConnectTimeout, ReadTimeout):
        return False
    return False

def read_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = file.readlines()
    return [proxy.strip() for proxy in proxies]

def write_proxy(file_path, proxy):
    with open(file_path, 'a') as file:
        file.write(f'socks5h://{proxy}\n')

if __name__ == '__main__':
    input_file = 'proxies.txt'
    output_file = 'working_proxies.txt'

    proxies = read_proxies(input_file)

    for proxy in proxies:
        try:
            if check_proxy(proxy):
                print(f"Proxy {proxy} is working.")
                write_proxy(output_file, proxy)
            else:
                print(f"Proxy {proxy} failed.")
        except Exception as e:
            print(f"An error occurred with proxy {proxy}: {e}")

    print(f"Working proxies are being saved to {output_file} as they are found.")
