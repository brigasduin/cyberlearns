#  WRITE-UP: PYTHON PORT SCANNER DEVELOPMENT

**Author:** Igor (eu)   
**Objective:** School Project - Network Fundamentals & Security  
**Date:** April 2 2026

---

## 1. PROJECT CONCEPT
The primary goal of this script is to identify open TCP ports on a specific target, which can be an **IP address** or a **Hostname**. Unlike complex tools like Nmap, this scanner focuses on simplicity and the core mechanics of the **TCP Connect** protocol.

### How it Works (The Logic)
The scanner utilizes the standard **TCP Three-Way Handshake**:
1. **SYN:** The script sends a connection request to a specific port.
2. **SYN-ACK:** If the port is open, the target responds, accepting the connection.
3. **ACK/RST:** The script acknowledges the response and immediately closes the connection to release system resources.



---

## 2. CODE STRUCTURE (DISSECTION)

### A. Core Libraries
* `socket`: The fundamental library for low-level network communication. It allows Python to interface directly with the Operating System's network stack.
* `sys`: Used for system-specific parameters and clean termination of the script.

### B. Service Mapping (Dictionary)
A **Dictionary (Key: Value)** structure was implemented to map well-known ports to their respective services.
* **Example:** `80: "HTTP (Web)"`
* This feature ensures that the output is human-readable, identifying which service is likely running (based on IANA standards).

### C. Connection Handling (`connect_ex`)
Instead of the standard `connect()` method, I used `connect_ex()`.
* **Return 0:** The connection was successful (**Port Open**).
* **Other values (e.g., 11, 111):** The connection failed (**Port Closed** or Filtered by a Firewall).

---

## 3. SECURITY & PERFORMANCE FEATURES
* **Timeout Mechanism (`settimeout(1)`):** This is crucial for stability. It prevents the program from hanging indefinitely if a target is offline or protected by a "stealth" firewall.
* **Resource Cleanup (`client.close()`):** Vital for system health. Every socket opened is explicitly destroyed, preventing memory leaks and ensuring the Kali Linux environment remains fast.

---

## 4. EXECUTION STEPS
1. Save the code as `scansc.py`.
2. Open the terminal and execute:  
   `python3 scansc.py`
3. Input the target IP (e.g., `127.0.0.1` or `google.com`) when prompted.

    Or run in the Vs code

---

## 5. FINAL CONCLUSION
This project demonstrates Python's power in cybersecurity automation. By building this tool from scratch, I gained a deep understanding of **DNS resolution**, **TCP connectivity**, and how network services interact at a packet level.