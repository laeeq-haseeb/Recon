import os
import sys
import time
import socket
import subprocess
import requests
import whois
from colorama import init, Fore, Style

init(autoreset=True)

class ReconEagle:
    def __init__(self):
        self.target = ""
        self.ip = ""
        self.results = {}

    def banner(self):
        banner_path = os.path.join(os.path.dirname(__file__), "eagle_banner.txt")
        if os.path.exists(banner_path):
            try:
                with open(banner_path, "r", encoding="utf-8") as f:
                    print(Fore.CYAN + f.read() + Style.RESET_ALL)
                return
            except Exception:
                pass

        print(Fore.CYAN + r"""
🦅 R E C O N   E A G L E 🦅
Lightweight Reconnaissance & Intelligence Engine
------------------------------------------------
""" + Style.RESET_ALL)

    def get_target(self):
        domain = input(Fore.YELLOW + "[?] Enter target domain (e.g. example.com): " + Style.RESET_ALL).strip()
        domain = domain.replace("https://", "").replace("http://", "").split("/")[0]
        self.target = domain
        try:
            self.ip = socket.gethostbyname(self.target)
            print(Fore.GREEN + f"[+] Target IP: {self.ip}\n" + Style.RESET_ALL)
            self.results["IP"] = self.ip
        except socket.gaierror:
            print(Fore.RED + "[-] Could not resolve domain host. Exiting..." + Style.RESET_ALL)
            sys.exit(1)

    def whois_lookup(self):
        print(Fore.BLUE + "[*] Performing WHOIS Lookup..." + Style.RESET_ALL)
        try:
            w = whois.whois(self.target)
            whois_data = f"Registrar: {w.registrar}\nCreation Date: {w.creation_date}\nExpiration Date: {w.expiration_date}"
            self.results["WHOIS"] = whois_data
            print(Fore.GREEN + f"    Registrar: {w.registrar}")
            print(Fore.GREEN + f"    Creation Date: {w.creation_date}\n")
        except Exception as e:
            print(Fore.RED + f"[-] WHOIS Lookup Failed: {e}\n" + Style.RESET_ALL)
            self.results["WHOIS"] = "Failed"

    def dns_enum(self):
        print(Fore.BLUE + "[*] Enumerating DNS Records..." + Style.RESET_ALL)
        records = ["A", "MX", "NS"]
        dns_data = []
        for rec in records:
            try:
                res = subprocess.check_output(["dig", "+short", rec, self.target], text=True).strip()
                if res:
                    dns_data.append(f"{rec} Records:\n{res}")
                    print(Fore.GREEN + f"    [{rec}] {res.replace(chr(10), ', ')}")
            except Exception:
                pass
        self.results["DNS"] = "\n".join(dns_data) if dns_data else "No records found"
        print()

    def subdomain_enum(self):
        print(Fore.BLUE + "[*] Discovering Subdomains (crt.sh)..." + Style.RESET_ALL)
        try:
            url = f"https://crt.sh/?q=%.{self.target}&output=json"
            res = requests.get(url, timeout=10)
            if res.status_code == 200 and res.text.strip():
                data = res.json()
                subdomains = sorted(list(set(entry["name_value"] for entry in data)))[:20]
                self.results["Subdomains"] = subdomains
                for sub in subdomains:
                    print(Fore.GREEN + f"    [+] {sub}")
            else:
                print(Fore.YELLOW + "    [-] No subdomains found.")
                self.results["Subdomains"] = []
        except Exception as e:
            print(Fore.RED + f"[-] Subdomain Discovery Failed: {e}" + Style.RESET_ALL)
            self.results["Subdomains"] = []
        print()

    def port_scan(self):
        print(Fore.BLUE + "[*] Scanning Ports (21, 22, 80, 443, 8080)..." + Style.RESET_ALL)
        ports = [21, 22, 80, 443, 8080]
        open_ports = []
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((self.ip, port))
            if result == 0:
                open_ports.append(port)
                print(Fore.GREEN + f"    [+] Port {port} is OPEN")
            s.close()
        self.results["Open Ports"] = open_ports
        print()

    def tech_detect(self):
        print(Fore.BLUE + "[*] Detecting Web Technologies (WhatWeb)..." + Style.RESET_ALL)
        try:
            output = subprocess.check_output(["whatweb", self.target], text=True).strip()
            self.results["Technologies"] = output
            print(Fore.GREEN + f"    {output}\n")
        except Exception:
            print(Fore.YELLOW + "    [-] WhatWeb not available or scan failed.\n")
            self.results["Technologies"] = "N/A"

    def generate_report(self):
        os.makedirs("reports", exist_ok=True)
        timestamp = int(time.time())
        filename = f"reports/recon_report_{self.target}_{timestamp}.txt"
        
        with open(filename, "w") as f:
            f.write(f"=== RECON EAGLE REPORT FOR {self.target} ===\n\n")
            f.write(f"IP Address: {self.results.get('IP')}\n\n")
            f.write(f"--- WHOIS ---\n{self.results.get('WHOIS')}\n\n")
            f.write(f"--- DNS RECORDS ---\n{self.results.get('DNS')}\n\n")
            f.write("--- SUBDOMAINS ---\n" + "\n".join(self.results.get("Subdomains", [])) + "\n\n")
            f.write(f"--- OPEN PORTS ---\n{self.results.get('Open Ports')}\n\n")
            f.write(f"--- TECHNOLOGIES ---\n{self.results.get('Technologies')}\n")

        print(Fore.MAGENTA + f"[✔] Report generated successfully: {filename}" + Style.RESET_ALL)

    def run(self):
        self.banner()
        self.get_target()
        self.whois_lookup()
        self.dns_enum()
        self.subdomain_enum()
        self.port_scan()
        self.tech_detect()
        self.generate_report()

if __name__ == "__main__":
    ReconEagle().run()
