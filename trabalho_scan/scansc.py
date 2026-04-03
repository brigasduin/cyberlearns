import socket 
import sys
def start_scansc():
    print ("=" * 40)
    print ("                PORT SCANNER")
    print ("=" * 40)

    target = input("Type the ip or hostname: ")


    services = {
        21: "FTP (Archives)",
        22: "SSH (Remote access)",
        23: "Telnet",
        25: "SMTP (E-mail)",
        53: "DNS ",
        80: "HTTP (Web)",
        443: "HTTPS (Secure web)",
        3306: "MySQL (Database)",
        8080: "HTTP-Proxy"
    }

    try:

        target_ip = socket.gethostbyname(target)
    except socket.gaierror:

        print("\n[ERROR] We cannot find this hostname")
        return
    print(f"\nScanning Target: {target_ip}")
    print("-" * 40)

    for port in services.keys():
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(1)
        result = client .connect_ex((target_ip, port))
        if result == 0:
            service_name = services.get(port, "Unknown service")
            print(f"Port {port:5} : OPEN {service_name}")
        else:
            print(f"Port {port:5} : CLOSED")
        client.close
    print("-" * 40 )
    print("Scan finished")
start_scansc()