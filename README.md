# Recon
```markdown
# 🦅 Recon Eagle - Advanced Reconnaissance & Intelligence Engine

**Author:** ARWA NOOR

## 📝 Overview
Recon Eagle is an automated, Python-based reconnaissance tool designed to help security testers and penetration testers seamlessly collect vital information about a target domain. Instead of performing multiple manual checks, Recon Eagle automates the initial information-gathering phase of a security assessment and compiles all findings into a structured, easy-to-read report.

## 🚀 Features
* **IP Discovery:** Automatically resolves the target domain to its IPv4 address.
* **WHOIS Lookup:** Retrieves domain registration details, creation dates, and registrar information.
* **DNS Enumeration:** Extracts essential DNS records including A, MX, and NS records.
* **Subdomain Discovery:** Queries `crt.sh` to uncover potential subdomains via certificate transparency logs.
* **Port Scanning:** Checks common and critical ports (e.g., 21, 22, 80, 443, 8080) to identify listening services.
* **Technology Detection:** Integrates with WhatWeb to identify web servers, frameworks, and HTTP headers.
* **Automated Reporting:** Generates a clean, timestamped text report containing all reconnaissance data.

## 🛠️ Tech Stack
* **Language:** Python 3
* **Network Queries:** `socket`, `whois`, `dnspython` 
* **Web Requests:** `requests` 
* **External Tools:** `WhatWeb`

## ⚙️ Installation & Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/laeeq-haseeb/Recon.git](https://github.com/laeeq-haseeb/Recon.git)
   cd Recon

```

2. Install the required Python dependencies:
```bash
pip install -r requirements.txt

```


3. Ensure `WhatWeb` is installed on your system (pre-installed on Kali Linux):
```bash
sudo apt-get install whatweb

```



## 💻 Usage

Run the script using Python 3:

```bash
python3 recon.py

```

When prompted, enter the target domain (e.g., `google.com`). Recon Eagle will execute its scanning sequence and output a comprehensive text file in the `reports/` directory.

## ⚠️ Disclaimer

Recon Eagle is designed for authorized security testing, educational purposes, and defensive analysis only. The author is not responsible for any misuse of this tool. Always ensure you have explicit permission before scanning or performing reconnaissance on any target.

