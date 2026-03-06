# HTB - Appointment

**Difficulty:** Very Easy  
**Category:** SQL Injection  
**Date:** 2026  
**Status:** ✅ Completed

---

## Summary

Appointment is a Linux machine running a web application with a login form vulnerable to SQL Injection. By injecting a SQL comment into the username field, it is possible to bypass authentication and login as admin without knowing the password.

---

## Enumeration

### Nmap Scan

```bash
nmap -sV -sC -p- --min-rate 5000 10.129.x.x
```

**Open Ports:**
| Port | Service | Version |
|------|---------|---------|
| 80 | http | Apache httpd 2.4.38 |

Port **80** is open, meaning there is a web application running.

---

## Exploitation

### Step 1 - Access the Web Application

Opened the machine IP in a browser:

```
http://10.129.x.x
```

Found a login page asking for username and password.

### Step 2 - Test for SQL Injection

The login form was not sanitizing user input. By injecting a SQL comment character into the username field, the password check in the SQL query can be bypassed.

The SQL query behind the login looks something like this:

```sql
SELECT * FROM users WHERE username='INPUT' AND password='INPUT'
```

By injecting `admin'#` as the username, the query becomes:

```sql
SELECT * FROM users WHERE username='admin'#' AND password='anything'
```

Everything after `#` is treated as a comment and ignored by the database, so the password check is completely bypassed.

**Username:**
```
admin'#
```
**Password:**
```
anything
```

### Step 3 - Retrieve the Flag

After logging in successfully as admin, the flag was displayed on the page.

---



---

## What I Learned

- What SQL Injection is and how it works
- How SQL comment characters (`--` and `#`) can be used to bypass authentication
- How unsanitized user input leads to critical vulnerabilities
- The importance of disabling browser shields/extensions when testing web applications
- Why developers should always use **prepared statements** to prevent SQL Injection

---

## References

- [SQL Injection - OWASP](https://owasp.org/www-community/attacks/SQL_Injection)
- [SQLi Authentication Bypass - HackTricks](https://book.hacktricks.xyz/pentesting-web/login-bypass/sql-login-bypass)
