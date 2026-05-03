# Cybersecurity Portfolio – Adam Zasiński

## 📌 Overview

A collection of hands-on cybersecurity projects built in a home lab environment (Hyper-V & Microsoft 365 Cloud). The projects form a coherent whole — from hybrid identity management and log analysis to network segmentation and active intrusion detection.

| Area | Projects |
|------|---------|
| Identity & Access Management | Microsoft 365 & Entra ID, Active Directory Lab |
| Log Analysis & Detection | Python Security Tools, pfSense Security Lab |
| Network Security | pfSense Security Lab |
| Offensive Security (controlled) | pfSense Security Lab (Kali + Nmap) |

---

## 🚀 Projects

---

### ☁️ Microsoft 365 & Entra ID Security Lab *(new)*

A cloud-based security environment focusing on Modern Identity Management and Zero Trust architecture.

**Scope:**
- **Identity & Access Management (IAM):** User lifecycle management, group hierarchies, and license optimization in M365 Admin Center.
- **Zero Trust Implementation:** Configuring **Conditional Access Policies** to enforce MFA based on trusted "Named Locations" (IP-based filtering).
- **Security Operations:** Monitoring sign-in logs in **Microsoft Entra ID** and managing secure offboarding procedures (session revocation, account freezing).
- **Exchange Online:** Administration of Shared Mailboxes and delegated permissions for secure corporate communication.

**Technologies:** Microsoft 365 Business Premium, Entra ID (Azure AD), Exchange Online, Conditional Access.

📁 [View project →](./m365-security-lab/)

---

### 🏢 Active Directory Security Lab

A virtual corporate environment built on Windows Server with a Domain Controller and a domain-joined workstation.

**Scope:**
- Windows Server (Domain Controller) + Windows 10 (domain client).
- User, group, and GPO management in Active Directory.
- Advanced Audit Policy configuration (logon events, credential validation).
- Authentication log analysis: Event ID 4624 (successful logon) and 4625 (failed logon).
- Brute-force pattern detection based on event sequences.

**Technologies:** Windows Server, Active Directory, Group Policy, Event Viewer, Hyper-V.

📁 [View project →](./active-directory-lab/)

---

### 🐍 Python Security & Log Analysis Tools

A suite of automation scripts for threat detection and log parsing, typical of SOC environments.

**Features:**
- **suricata_analyzer.py:** Parses complex `eve.json` IDS logs, categorizing alerts by severity and identifying top attack signatures[cite: 5].
- **log_analyzer.py:** Detects SSH brute-force patterns in Linux `auth.log` using configurable thresholds and regex[cite: 5].
- **Automated Triage:** Extracts IP addresses and counts occurrences to prioritize incident response[cite: 5].

**Technologies:** Python 3, `json` parsing, `re` (Regex), `collections.Counter`, error handling.

📁 [View project →](./log-analysis-python/)

---

### 🔥 pfSense Network Security Lab

A complete network environment with a pfSense firewall, DMZ zone, and Suricata intrusion prevention system (IPS). 

**Scope:**
- Three-zone topology: WAN / LAN `192.168.x.0/24` (AD Lab) / DMZ `10.10.10.0/24`.
- Firewall rules: LAN→DMZ access, DMZ→LAN block, outbound traffic control.
- Suricata IPS with ETOpen rules (scan, exploit, web-server, DoS categories).
- Simulated attacks from Kali Linux (Nmap) and detection verification via Python analysis tools.

**Technologies:** pfSense CE, Suricata, Hyper-V, Kali Linux, Ubuntu Server, Python 3.

📁 [View project →](./pfsense-security-lab/)

---

## 🎯 TryHackMe

Active skills development on TryHackMe — 105+ completed labs, 19 badges, Top 5% of users.

Completed paths: **Pre Security**, **Cyber Security 101**
In progress: **SOC Level 1**

Profile: [tryhackme.com/p/arnie21layne](https://tryhackme.com/p/arnie21layne)

---

## 🧰 Technical Skills

**Systems & Infrastructure**
Microsoft 365 Administration · Entra ID (Azure AD) · Windows Server · Active Directory · Linux (CLI) · pfSense · Hyper-V · TCP/IP

**Cybersecurity**
Log analysis (Entra Sign-in logs, Win Event Logs, Linux auth.log, Suricata JSON) · Zero Trust · Conditional Access · MFA Enforcement · SIEM · IDS/IPS · IAM · Network segmentation

**Tools**
Microsoft Admin Center · Entra ID · Exchange Admin Center · Wireshark · Nmap · Splunk · Suricata

**Programming**
Python (automation, log analysis, JSON parsing) · Bash (scripting)

---

## 📫 Contact

- **GitHub:** [github.com/arnielayne](https://github.com/arnielayne)
- **TryHackMe:** [tryhackme.com/p/arnie21layne](https://tryhackme.com/p/arnie21layne)
