# Cybersecurity Portfolio – Adam Zasiński

## 📌 Overview

A collection of hands-on cybersecurity projects built in a home lab environment (Hyper-V). The projects form a coherent whole — from identity management and log analysis to network segmentation and active intrusion detection.

| Area | Projects |
|------|---------|
| Identity & Access Management | Active Directory Lab |
| Log Analysis & Detection | Python Log Analysis Tool, pfSense Security Lab |
| Network Security | pfSense Security Lab |
| Offensive Security (controlled) | pfSense Security Lab (Kali + Nmap) |

---

## 🚀 Projects

---

### 🏢 Active Directory Security Lab

A virtual corporate environment built on Windows Server with a Domain Controller and a domain-joined workstation.

**Scope:**
- Windows Server (Domain Controller) + Windows 10 (domain client)
- User, group, and GPO management in Active Directory
- Advanced Audit Policy configuration (logon events, credential validation)
- Authentication log analysis: Event ID 4624 (successful logon) and 4625 (failed logon)
- Brute-force pattern detection based on event sequences

**Technologies:** Windows Server, Active Directory, Group Policy, Event Viewer, Hyper-V

📁 [View project →](./active-directory-lab/)

---

### 🐍 Python Log Analysis Tool

A script detecting repeated failed login attempts in auth.log files — automating analysis typical of SOC environments.

**Features:**
- Parses `auth.log` (Linux) and Windows Event Log files
- Extracts IP addresses from failed login attempts
- Counts and ranks sources of suspicious activity
- Detects brute-force patterns based on configurable attempt thresholds

**Technologies:** Python 3, `collections.Counter`, log analysis

📁 [View project →](./log-analysis-python/)

---

### 🔥 pfSense Network Security Lab *(new)*

A complete network environment with a pfSense firewall, DMZ zone, and Suricata intrusion prevention system (IPS). The project combines network segmentation, default-deny firewall rules, and active alert analysis.

The lab reuses the Active Directory environment — the Windows 10 workstation and Domain Controller sit in the protected LAN behind pfSense, creating a realistic enterprise topology.

**Scope:**
- Three-zone topology: WAN / LAN `192.168.x.0/24` (AD Lab) / DMZ `10.10.10.0/24`
- Firewall rules: LAN→DMZ access, DMZ→LAN block, outbound traffic control
- Suricata IPS with ETOpen rules (scan, exploit, web-server, DoS categories)
- Simulated attacks from Kali Linux (Nmap) and detection verification
- Python script analyzing `eve.json` — alerts, source IPs, signatures, severity levels

**Technologies:** pfSense CE, Suricata, Hyper-V, Kali Linux, Ubuntu Server, Python 3

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
Windows Server · Active Directory · Linux (CLI) · pfSense · KVM / Hyper-V / VirtualBox · TCP/IP · DNS

**Cybersecurity**
Log analysis (Windows Event Logs, Linux auth.log, Suricata eve.json) · SIEM · IDS/IPS · Incident Response · IAM · Patch management · Network segmentation

**Tools**
Wireshark · Nmap · Splunk · Suricata · Metasploit (lab)

**Programming**
Python (automation, log analysis) · Bash (scripting)

---

## 📫 Contact

- **GitHub:** [github.com/arnielayne](https://github.com/arnielayne)
- **TryHackMe:** [tryhackme.com/p/arnie21layne](https://tryhackme.com/p/arnie21layne)
